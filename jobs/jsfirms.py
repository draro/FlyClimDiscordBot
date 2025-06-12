import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

BASE_URL = "https://www.jsfirm.com"
SEARCH_URL = f"{BASE_URL}/search-aviation-jobs"

def scrape_jsfirm_last_24h():
    print("🔍 Scraping JSFirm...")
    try:
        res = requests.get(SEARCH_URL, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    jobs = []

    rows = soup.select("div.welljob")

    for job_div in rows:
        try:
            title_tag = job_div.select_one("a.u[href*='jobID']")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            job_href = title_tag["href"]
            link = BASE_URL + job_href

            company_tag = job_div.select_one("a.u.company")
            company = company_tag.get_text(strip=True) if company_tag else "Unknown"

            location_tag = job_div.select_one("div.col-xs-8").contents[-1]
            location = location_tag.strip() if isinstance(location_tag, str) else "Unknown"

            posted_date_tag = job_div.select_one("div.col-xs-4 span.text-muted")
            posted_str = posted_date_tag.get_text(strip=True)
            posted_dt = datetime.strptime(posted_str, "%m/%d/%Y")

            if datetime.utcnow() - posted_dt > timedelta(days=1):
                continue  # Skip jobs older than 24 hours

            description_tag = job_div.select_one("div.col-xs-12 span.grayjob")
            desc = description_tag.get_text(strip=True)[:180] + "..." if description_tag else ""

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "url": link,
                "date": posted_str,
                "description": desc
            })
        except Exception as err:
            print("⚠️ Parse error:", err)
            continue

    return jobs


if __name__ == "__main__":
    jobs = scrape_jsfirm_last_24h()
    if jobs:
        print(f"Found {len(jobs)} jobs in the last 24 hours:")
        for job in jobs:
            print(f"- {job['title']} at {job['company']} ({job['location']}) - {job['date']}")
            print(f"  URL: {job['url']}")
            print(f"  Description: {job['description']}\n")
    else:
        print("No new jobs found in the last 24 hours.")