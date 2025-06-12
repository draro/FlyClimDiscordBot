from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.query import Query, QueryOptions
from linkedin_jobs_scraper.events import Events
from datetime import datetime, timedelta

job_results = []

def on_data(data):
    # Manual filtering based on posting time (some data sources provide relative time in string)
    posted_time = data.date
    if posted_time and isinstance(posted_time, datetime):
        if datetime.utcnow() - posted_time <= timedelta(days=1):
            if "pilot" in data.title.lower():
                job_results.append({
                    "title": data.title,
                    "company": data.company,
                    "location": data.place,
                    "date": posted_time,
                    "link": data.link
                })

def scrape_linkedin_pilot_jobs():
    global job_results
    job_results = []

    scraper = LinkedinScraper(
        chrome_executable_path="/usr/bin/chromium-browser",  # Update for your system
        chrome_driver_path="/usr/local/bin/chromedriver",    # Update for your system
        headless=True,
        max_workers=1,
        slow_mo=1.0,
    )

    scraper.on(Events.DATA, on_data)

    scraper.run([
        Query(
            query="pilot",
            options=QueryOptions(locations=["Worldwide"])
        )
    ])

    return job_results

if __name__ == "__main__":
    results = scrape_linkedin_pilot_jobs()
    for job in results:
        print(f"Title: {job['title']}, Company: {job['company']}, Location: {job['location']}, Date: {job['date']}, Link: {job['link']}")