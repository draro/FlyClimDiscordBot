import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import pandas as pd
import asyncio
from jobs.jobs import get_latest_pilot_jobs

load_dotenv()

DISCORD_TOKEN = os.getenv("ENG_JOBS")
CHANNEL_ID = 1382825652071305287  # Your Discord channel ID

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
@client.event
async def on_ready():
    print(f"🚀 Logged in as {client.user}")
    if not post_pilot_jobs.is_running():
        post_pilot_jobs.start()

@tasks.loop(hours=1)  # Run every 6 hours
async def post_pilot_jobs():
    print("🔍 Searching for pilot job openings...")
    channel = client.get_channel(CHANNEL_ID)
    keywords = ["Flight Engineer", "Aerospace Engineer", "Flight Operations", "Avionics Engineer",  "Flight Test Engineer", "Aircraft Systems Engineer", "Air Traffic Manager", "Flight Safety Engineer", "Flight Operations Engineer", "Flight Planning Engineer", "Flight Control Systems Engineer", "Flight Simulation Engineer", "Flight Operations Analyst", "Flight Operations Specialist", "Flight Operations Manager", "Flight Operations Coordinator"]

    jobs = await asyncio.to_thread(get_latest_pilot_jobs, keywords=keywords, site_name=[ "indeed", "linkedin", "zip_recruiter", "glassdoor", "google", "bayt", "naukri"])

    if jobs.empty:
        # await channel.send("❌ No new pilot jobs found in the last 24 hours.")
        return

    for _, row in jobs.iterrows():
        embed = discord.Embed(
            title=row.get('title', 'Engineering Job'),
            url=row.get('job_url') or row.get('job_url_direct'),
            description = (
    row['description'][:300] + '...' if isinstance(row.get('description'), str)
    else "No description available."),
            color=discord.Color.blue()
        )

        embed.set_author(name=row.get('company', 'Unknown Company'))

        if row.get('company_logo'):
            embed.set_thumbnail(url=row['company_logo'])

        embed.add_field(name="📍 Location", value=row.get('location', 'Unknown'), inline=True)
        embed.add_field(name="🏢 Company", value=row.get('company', 'Unknown'), inline=True)
        embed.add_field(name="💼 Job Type", value=row.get('job_type', 'Not specified'), inline=True)

        if pd.notnull(row.get('date_posted')):
            embed.add_field(name="🕒 Date Posted", value=row['date_posted'].strftime('%Y-%m-%d'), inline=True)

        if row.get('is_remote') is not None:
            embed.add_field(name="🏠 Remote", value="Yes" if row['is_remote'] else "No", inline=True)

        await channel.send(embed=embed)

client.run(DISCORD_TOKEN)