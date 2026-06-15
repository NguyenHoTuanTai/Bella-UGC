import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from flask import Flask
from threading import Thread
import os

# Flask keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot online!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# Bot
TOKEN = os.environ.get('TOKEN')

bot = commands.Bot()

@bot.slash_command(name="b", description="Bot nhắn lại nội dung bạn gửi")
async def b_command(interaction: nextcord.Interaction, text: str = SlashOption(description="Nội dung")):
    await interaction.response.send_message(text)

@bot.event
async def on_ready():
    print(f"✅ Bot đang chạy: {bot.user}")

bot.run(TOKEN)