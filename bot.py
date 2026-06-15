from flask import Flask, request, jsonify
import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from threading import Thread
import os

app = Flask(__name__)

# Trang chủ
@app.route('/')
def home():
    return "Bot online!"

# API purchase
@app.route('/purchase', methods=['POST'])
def purchase():
    data = request.json

    player_name = data.get("playerName")
    item_name = data.get("itemName")
    item_price = data.get("itemPrice")
    image_url = data.get("imageUrl")
    asset_id = data.get("assetId")

    print(f"🛒 {player_name} mua {item_name} ({item_price})")

    return jsonify({
        "success": True,
        "message": "Purchase received",
        "data": {
            "playerName": player_name,
            "itemName": item_name,
            "itemPrice": item_price,
            "imageUrl": image_url,
            "assetId": asset_id
        }
    })

def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# Discord Bot
TOKEN = os.environ.get('TOKEN')

bot = commands.Bot()

@bot.slash_command(
    name="b",
    description="Bot nhắn lại nội dung bạn gửi"
)
async def b_command(
    interaction: nextcord.Interaction,
    text: str = SlashOption(description="Nội dung")
):
    await interaction.response.send_message(text)

@bot.event
async def on_ready():
    print(f"✅ Bot đang chạy: {bot.user}")

bot.run(TOKEN)