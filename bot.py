import discord
from discord import app_commands
import os

TOKEN = os.environ.get('TOKEN')  # Lấy từ biến môi trường
CLIENT_ID = os.environ.get('CLIENT_ID')

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="b", description="Bot sẽ nhắn lại nội dung bạn gửi")
@app_commands.describe(text="Nội dung muốn gửi")
async def b_command(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(text)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Bot đang chạy: {client.user}")

client.run(TOKEN)