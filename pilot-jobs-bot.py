import discord
from discord.ext import tasks
import os
import requests
from dotenv import load_dotenv
import pandas as pd

from jobs.jobs import get_latest_pilot_jobs
load_dotenv()

DISCORD_TOKEN = os.getenv("JOB_TOKEN")
CHANNEL_ID = 1382633883882885232  # Your channel ID
print("DISCORD_TOKEN:", DISCORD_TOKEN)
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"🚀 Logged in as {client.user}")
    post_pilot_jobs.start()

@tasks.loop(hours=6)  # Run every 6 hours
async def post_pilot_jobs():
    print("🔍 Searching for pilot job openings...")
    channel = client.get_channel(CHANNEL_ID)

    # Placeholder for actual job search logic (e.g., web scraping, API call)
    jobs = await get_latest_pilot_jobs()

    for _, row in jobs.iterrows():
        title = row['title']
        company = row['company']
        location = ", ".join(filter(None, [row['location']]))
        url = row['job_url']
        # posted = row['date_posted'].strftime("%Y-%m-%d") if pd.notnull(row['date_posted']) else "N/A"

        await channel.send(
            f"📌 **{title}**\n🏢 {company}\n📍 {location or 'Unknown'}\n🔗 {url}\n"
        )

client.run(DISCORD_TOKEN)