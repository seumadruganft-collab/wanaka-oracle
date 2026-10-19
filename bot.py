import os
import json
from datetime import datetime, timedelta
from discord import app_commands
import discord
from discord.ext import commands, tasks

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = 1375407665827680326
BOSS_CHANNEL_ID = 1560459894568525834
CHAT_CHANNEL_ID = 1498671478999220224
MAPAS = {
    "T1": "Bosque dos Aprendizes (T1)",
    "T2": "Floresta Grande (T2)",
    "T3": "Pântano (T3)",
    "T4": "Deserto / Neve (T4)",
    "T5": "Cemitério (T5)"
}

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

async def boss_autocomplete(
    interaction: discord.Interaction,
    current: str
):
    return [
        app_commands.Choice(
            name=boss,
            value=boss
        )
        for boss in BOSSES.keys()
        if current.lower() in boss.lower()
    ][:25]

def load_data():
    try:
        with open("bosses.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open("bosses.json", "w") as f:
        json.dump(data, f, indent=4)

boss_data = load_data()

def has_permission(member):
    return any(role.name in ALLOWED_ROLES for role in member.roles)
@bot.event
async def on_ready():

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos sincronizados")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")

    print(f"{bot.user} online!")
    print("Wanaka Oracle iniciado.")
    
@bot.tree.command(
    name="respawns",
    description="Mostra todos os respawns registrados"
)
async def respawns(interaction: discord.Interaction):

    if not boss_data:
        await interaction.response.send_message(
            "Nenhum boss registrado."
        )
        return

    mensagem = ""

    lista = sorted(
        boss_data.items(),
        key=lambda item: item[1]["respawn"]
    )

    for boss, dados in lista:
        mensagem += f"➤ {boss}: {dados['respawn']}\n"

    await interaction.response.send_message(mensagem)
@bot.tree.command(
    name="kill",
    description="Registra a morte de um boss"
)
@app_commands.autocomplete(
    boss=boss_autocomplete
)
async def kill(
    interaction: discord.Interaction,
    boss: str
):

    if not has_permission(interaction.user):
        await interaction.response.send_message(
            "Sem permissão para usar este comando.",
            ephemeral=True
        )
        return

    if boss not in BOSSES:
        await interaction.response.send_message(
            "Boss inválido."
        )
        return

    agora = datetime.now() - timedelta(hours=3)

    proximo = agora + timedelta(
        minutes=BOSSES[boss]
    )

    boss_data[boss] = {
        "respawn": proximo.strftime("%H:%M"),
        "alerta5": False,
        "alerta0": False
    }

    save_data(boss_data)

    await interaction.response.send_message(
        f"✅ {boss} registrado\n\n"
        f"🕒 Próximo respawn: {proximo.strftime('%H:%M')}"
    )
@bot.tree.command(
    name="edit",
    description="Edita o horário de um boss"
)
@app_commands.autocomplete(
    boss=boss_autocomplete
)
async def edit(
    interaction: discord.Interaction,
    boss: str,
    horario: str
):

    if not has_permission(interaction.user):
        await interaction.response.send_message(
            "Sem permissão para usar este comando.",
            ephemeral=True
        )
        return

    boss_data[boss] = {
        "respawn": horario,
        "alerta5": False,
        "alerta0": False
    }

    save_data(boss_data)

    await interaction.response.send_message(
        f"✅ {boss} atualizado\n\n"
        f"🕒 Novo respawn: {horario}"
    )
@bot.tree.command(
    name="remove",
    description="Remove um boss dos registros"
)
@app_commands.autocomplete(
    boss=boss_autocomplete
)
async def remove(
    interaction: discord.Interaction,
    boss: str
):

    if not has_permission(interaction.user):
        await interaction.response.send_message(
            "Sem permissão para usar este comando.",
            ephemeral=True
        )
        return

    if boss not in boss_data:
        await interaction.response.send_message(
            "Boss não encontrado nos registros."
        )
        return

    del boss_data[boss]

    save_data(boss_data)

await interaction.response.send_message(
    f"✅ {boss} removido dos registros."
)

bot.run(TOKEN)
