from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime, timedelta

def scrape_pilot_jobs_last_day(keyword: str, site_names=["indeed", "linkedin"]) -> pd.DataFrame:
    all_jobs = []

    for site in site_names:
        print(f"🔍 Scraping {site} for '{keyword}' jobs...")
        try:
            if site == "linkedin":
                print("Scraping LinkedIn...")
                jobs = scrape_jobs(
                    site_name=["linkedin"],
                    search_term=keyword,
                    results_wanted=1000,
                    hours_old=24,
                    # linkedin_fetch_description=True,
                    # country="united states",  # Must be a valid JobSpy country
                    company_industry="Airlines/Aviation",
                )
                print(f"LinkedIn scraped {len(jobs)} jobs.")
            elif site == "indeed":
                print("Scraping Indeed...")
                jobs = scrape_jobs(
                    site_name=["indeed"],
                    search_term=keyword,
                    results_wanted=1000,
                    hours_old=24,
                    country_indeed="worldwide",  # 'worldwide' is valid for Indeed
                    company_industry="aviation"
                )
                print(f"Indeed scraped {len(jobs)} jobs.")
            else:
                print(f"⚠️ Unknown site: {site}")
                continue

            if isinstance(jobs, pd.DataFrame) and not jobs.empty:
                all_jobs.append(jobs)
        except Exception as e:
            print(f"❌ Error scraping {site}: {e}")

    # Combine all jobs
    if not all_jobs:
        return pd.DataFrame()

    jobs_df = pd.concat(all_jobs, ignore_index=True)

    # Filter for keyword in title
    jobs_df = jobs_df[jobs_df['title'].str.lower().str.contains(keyword.lower(), na=False)]

    print(f"✅ Total '{keyword}' jobs scraped across sources: {len(jobs_df)}")
    return jobs_df
def format_jobs_for_discord(jobs_df: pd.DataFrame) -> str:
    if jobs_df.empty:
        return "❌ No new pilot jobs found in the last 24 hours."

    lines = ["**✈️ Latest Pilot Jobs  in LinkedIn (Last 2h)**\n"]

    for _, row in jobs_df.iterrows():
        title = row['title']
        company = row['company']
        location = ", ".join(filter(None, [row['location']]))
        url = row['job_url']
        posted = row['date_posted'].strftime("%Y-%m-%d") if pd.notnull(row['date_posted']) else "N/A"

        lines.append(
            f"📌 **{title}**\n🏢 {company}\n📍 {location or 'Unknown'}\n🕒 {posted}\n🔗 {url}\n"
        )

    return "\n".join(lines)


# if __name__ == "__main__":
def get_latest_pilot_jobs(keywords,site_name=["indeed"]):
    # Keywords to search for pilot jobs
    all_jobs = []

    for keyword in keywords:
        print(f"Scraping jobs for keyword: {keyword}")
        jobs_df = scrape_pilot_jobs_last_day(keyword, site_names=site_name)
        all_jobs.append(jobs_df)
    if all_jobs:
        combined_df = pd.concat(all_jobs, ignore_index=True).drop_duplicates(subset="job_url")
        # discord_message = format_jobs_for_discord(combined_df)
        return combined_df

if __name__ == "__main__":
    keywords = ["Flight Dispatcher", "Flight Operations Officer", "Flight Operations Controller", "Flight Operations Specialist"]

    latest_jobs = get_latest_pilot_jobs(keywords, site_name=[ "linkedin"])
    if not latest_jobs.empty:
        print(format_jobs_for_discord(latest_jobs))
    else:
        print("No new pilot jobs found in the last 24 hours.")