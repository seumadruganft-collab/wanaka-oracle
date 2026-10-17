import os
import json
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1375407665827680326
BOSS_CHANNEL_ID = 1560459894568525834
CHAT_CHANNEL_ID = 1498671478999220224

ALLOWED_ROLES = ["Líder", "Staff"]

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

BOSSES = {
    "T1Fungus1": 60,
    "T1Fungus2": 60,
    "T1Fungus3": 60,
    "T1Fungus4": 60,
    "T1Fungus5": 60,
    "T1Fungus6": 60,

    "T1Slime1": 180,
    "T1Slime2": 180,
    "T1Slime3": 180,

    "T2Druid1": 60,
    "T2Druid2": 60,
    "T2Druid3": 60,
    "T2Druid4": 60,
    "T2Druid5": 60,
    "T2Druid6": 60,

    "T2Thor": 180,

    "T3Venom1": 60,
    "T3Venom2": 60,
    "T3Venom3": 60,
    "T3Venom4": 60,
    "T3Venom5": 60,
    "T3Venom6": 60,

    "T3Beholder": 180,

    "T4Sentinel1": 60,
    "T4Sentinel2": 60,
    "T4Sentinel3": 60,
    "T4Sentinel4": 60,
    "T4Sentinel5": 60,
    "T4Sentinel6": 60,

    "T4Demon": 180,
    "T4Necro": 180,

    "T4Stalker1": 60,
    "T4Stalker2": 60,
    "T4Stalker3": 60,
    "T4Stalker4": 60,
    "T4Stalker5": 60,
    "T4Stalker6": 60,

    "T4Golem": 180,

    "T5Bone1": 60,
    "T5Bone2": 60,
    "T5Bone3": 60,
    "T5Bone4": 60,
    "T5Bone5": 60,
    "T5Bone6": 60,

    "T5Abyssal": 180,
    "T5Void": 180
}

@bot.event
async def on_ready():
    print(f"{bot.user} online!")
    print("Wanaka Oracle iniciado.")

bot.run(TOKEN)
