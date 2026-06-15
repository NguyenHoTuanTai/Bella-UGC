import discord
from discord import app_commands
import os
from flask import Flask
from threading import Thread

# ── Flask keep-alive (chạy trước) ──
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot online!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()  # Chạy Flask ở background

# ── Discord Bot ──
TOKEN = os.environ.get('TOKEN')

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
    print(f"✅ Bot đang chạy: {client.user}")

client.run(TOKEN)  # Chạy bot ở cuối cùng