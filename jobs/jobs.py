from jobspy import scrape_jobs
import pandas as pd
from datetime import datetime, timedelta
import time
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
                    hours_old=1,
                    linkedin_fetch_description=True,
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
                    hours_old=1,
                    country_indeed="worldwide",  # 'worldwide' is valid for Indeed
                    company_industry="aviation"
                )
                print(f"Indeed scraped {len(jobs)} jobs.")
            else:
                try:
                    print(f"Scraping {site}...")
                    jobs = scrape_jobs(
                        site_name=[site],
                        search_term=keyword,
                        results_wanted=25,
                        hours_old=1,
                        # linkedin_fetch_description=True,
                        # country="united states",  # Must be a valid JobSpy country
                        # google_search_term=keyword,  # Optional for Google search
                        # location="united states",  # Optional for location-based search
                        # is_remote=True,  # Optional for remote jobs
                        # job_type="full_time",  # Optional for job type filtering
                        # easy_apply=True,  # Optional for easy apply jobs
                        # description_format="html",  # Optional for description format
                        # linkedin_company_ids=None,  # Optional for specific company IDs
                        # offset=0,  # Optional for pagination
                        # enforce_annual_salary=True,  # Optional for annual salary enforcement
                        # proxies=None,  # Optional for proxy support
                        # ca_cert=None,  # Optional for CA certificate
                        # verbose=1,  # Optional for verbosity level
                        # country_indeed="worldwide",  # 'worldwide' is valid for Indeed
                        company_industry="aviation"
                    )
                    print(f"{site.capitalize()} scraped {len(jobs)} jobs.")
                except Exception as e:
                    print(f"⚠️ Error scraping {site}: {e}")
                    # Fallback to Indeed if site is unknown
                    print("Falling back to Indeed for this keyword...")
                    print("Scraping Indeed as fallback...")
                
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
        print(row)
        time.sleep(2)  # Sleep to avoid rate limiting
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
    keywords = ["Flight Dispatcher"]

    latest_jobs = get_latest_pilot_jobs(keywords, site_name=[ "indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "bayt", "naukri"])
    if not latest_jobs.empty:
        print(format_jobs_for_discord(latest_jobs))
    else:
        print("No new pilot jobs found in the last 24 hours.")