from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime, timedelta

def scrape_pilot_jobs_last_day(keyword):
    # Scrape up to 50 jobs posted in the last 24 hours with 'pilot' in the title
    jobs = scrape_jobs(
        site_name=["linkedin"],
        search_term=keyword,
        # location="worldwide",
        results_wanted=200,
        hours_old=4,
        # linkedin_fetch_description=True,
        company_industry=["Airlines/Aviation", "Aviation & Aerospace"],
    )
    print(f"Total jobs scraped: {len(jobs)}")
    print(f"Jobs DataFrame:\n{jobs.iloc[0].to_dict()}")
    # Filter: must contain 'pilot' in the job title (case-insensitive)
    jobs = jobs[jobs['title'].str.lower().str.contains(keyword, na=False)]

    return jobs


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
def get_latest_pilot_jobs():
    # Keywords to search for pilot jobs
    keywords = ["pilot", "airline pilot", "commercial pilot", "private pilot", "flight instructor"]
    all_jobs = []

    for keyword in keywords:
        print(f"Scraping jobs for keyword: {keyword}")
        jobs_df = scrape_pilot_jobs_last_day(keyword)
        all_jobs.append(jobs_df)
    if all_jobs:
        combined_df = pd.concat(all_jobs, ignore_index=True).drop_duplicates(subset="job_url")
        discord_message = format_jobs_for_discord(combined_df)
        return discord_message
