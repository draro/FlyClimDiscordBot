import discord
from discord import app_commands
from discord.ext import commands
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("FLYCLIM_API")

class FlyClimBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="/", intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash commands synced.")

bot = FlyClimBot()

@bot.tree.command(name="fpl", description="Check storm risk for an ICAO flight plan")
@app_commands.describe(fpl_string="Paste the full FPL string")
async def fpl_command(interaction: discord.Interaction, fpl_string: str):
    await interaction.response.defer(thinking=True)

    try:
        payload = {
            "fpl": fpl_string,
            "departure_time": datetime.now(timezone.utc).isoformat()
        }
        res = requests.post(API_URL, json=payload)
        if res.ok:
            data = res.json()
            storm_hits = data.get("collisions", [])
            if storm_hits:
                segments = "\n".join(
                    f"• `{hit['segment_label']}` at {hit['timestamp']} UTC"
                    for hit in storm_hits
                )
                msg = f"⚠️ **Storms detected:**\n{segments}"
            else:
                msg = "✅ No storm impact detected along the route."
            await interaction.followup.send(msg)
        else:
            await interaction.followup.send("❌ API error.")
    except Exception as e:
        await interaction.followup.send(f"🚨 Error: {e}")

bot.run(TOKEN)