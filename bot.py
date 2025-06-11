import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
FLYCLIM_API = os.getenv("FLYCLIM_API")  # e.g., https://demo.flyclim.com/api/bot/check-fpl

# Create the bot
class FlyClimBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="/", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands synced with Discord.")

# Instantiate the bot
bot = FlyClimBot()

# Register a slash command
@bot.tree.command(name="fpl", description="Check storm risk for a flight plan (ICAO format)")
@app_commands.describe(fpl_string="Paste the full FPL string")
async def fpl_command(interaction: discord.Interaction, fpl_string: str):
    await interaction.response.defer(thinking=True)

    try:
        payload = {
            "fpl": fpl_string,
            # "departure_time": datetime.now(timezone.utc).isoformat()
        }
        res = requests.post(FLYCLIM_API, json=payload)

        if res.ok:
            data = res.json()
            print(f"Received data: {data}")
            storm_hits = data.get("collisions", [])
            if storm_hits:
                segments = "\n".join(
                    f"• `{hit['segment_label']}` at {hit['timestamp']} UTC"
                    for hit in storm_hits
                )
                msg = f"⚠️ **Storms detected on your route:**\n{segments}"
            else:
                msg = "✅ No storm impact detected along your flight plan."
            await interaction.followup.send(msg)
        else:
            await interaction.followup.send(f"❌ API error: {res.status_code} {res.text}")

    except Exception as e:
        await interaction.followup.send(f"🚨 Error: {str(e)}")

# Run the bot
bot.run(DISCORD_TOKEN)