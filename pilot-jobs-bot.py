import discord
from discord.ext import tasks
import os
import requests
from dotenv import load_dotenv
load_dotenv()

DISCORD_TOKEN = os.getenv("JOB_TOKEN")
CHANNEL_ID = int(1382633883882885232)  # Your channel ID
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
    jobs = [
        {"title": "First Officer - A320", "company": "Lufthansa", "url": "https://example.com/job1"},
        {"title": "Captain - B737", "company": "Ryanair", "url": "https://example.com/job2"}
    ]

    for job in jobs:
        msg = f"📌 **{job['title']}** at **{job['company']}**\n🔗 {job['url']}"
        await channel.send(msg)

client.run(DISCORD_TOKEN)