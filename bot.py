import discord
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("FLYCLIM_API")  # e.g. https://demo.flyclim.com/api/bot/check-fpl

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Bot is live as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("/fpl "):
        fpl = message.content[5:].strip()
        await message.channel.send("🛫 Processing FPL...\nPlease wait...")

        try:
            payload = {
                "fpl": fpl,
                "departure_time": datetime.now(timezone.utc).isoformat()
            }

            res = requests.post(API_URL, json=payload)
            if res.ok:
                data = res.json()
                storm_hits = data.get("collisions", [])
                storm_detected = data.get("storm_detected", False)

                if storm_detected and storm_hits:
                    segments = "\n".join(
                        f"• `{hit['segment_label']}` at {hit['timestamp']} UTC"
                        for hit in storm_hits
                    )
                    msg = f"""
⚠️ **Storms detected along route**
{segments}
"""
                else:
                    msg = "✅ No storm impact detected along the route."

                await message.channel.send(msg.strip())
            else:
                await message.channel.send("❌ API error while checking FPL.")
        except Exception as e:
            await message.channel.send(f"🚨 Exception occurred: {e}")

client.run(DISCORD_TOKEN)