from flask import Flask, request, jsonify
import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from threading import Thread
import os
import asyncio
import requests

app = Flask(__name__)

# CONFIG
TOKEN = os.environ.get("TOKEN")
CHANNEL_ID = 1516082510050754693

# FLASK
@app.route('/')
def home():
    return "Bot online!"

# ✅ Route mới: check bundle info từ Roblox catalog
@app.route('/check-bundle', methods=['GET'])
def check_bundle():
    item_id = request.args.get("id")
    if not item_id:
        return jsonify({"isBundle": False}), 200
    try:
        res = requests.get(
            f"https://catalog.roblox.com/v1/bundles/{item_id}/details",
            timeout=5
        )
        if res.status_code == 200:
            data = res.json()
            creator = data.get("creator", {})
            product = data.get("product", {})
            return jsonify({
                "isBundle": True,
                "id": data.get("id"),
                "name": data.get("name"),
                "creator": { "name": creator.get("name", "Roblox") },
                "product": { "priceInRobux": product.get("priceInRobux") }
            }), 200
        else:
            return jsonify({"isBundle": False}), 200
    except Exception as e:
        print("❌ Error checking bundle:", e)
        return jsonify({"isBundle": False}), 200

@app.route('/purchase', methods=['POST'])
def purchase():
    data = request.json
    player_name = data.get("playerName")
    item_name = data.get("itemName")
    item_price = data.get("itemPrice")
    image_url = data.get("imageUrl")
    asset_id = data.get("assetId")

    print(f"🛒 {player_name} mua {item_name} ({item_price})")

    async def send_purchase_message():
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            print("❌ Không tìm thấy channel")
            return

        embed = nextcord.Embed(
            title="🛒 New Purchase",
            description=f"**{player_name}** just buy item!",
            color=0x00ff00
        )
        embed.add_field(name="👤 Player", value=player_name, inline=True)
        embed.add_field(name="🎁 Item", value=item_name, inline=True)
        embed.add_field(name="💰 Price", value=f"{item_price} Robux", inline=True)
        embed.add_field(name="🆔 Asset ID", value=asset_id, inline=False)
        if image_url:
            embed.set_thumbnail(url=image_url)
        embed.set_footer(text="Bella UGC Purchase")
        await channel.send(embed=embed)

    bot.loop.create_task(send_purchase_message())
    return jsonify({"success": True, "message": "Purchase received"})


def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# DISCORD BOT
intents = nextcord.Intents.default()
bot = commands.Bot(intents=intents)

@bot.slash_command(name="b", description="Bot text what u text")
async def b_command(
    interaction: nextcord.Interaction,
    text: str = SlashOption(description="words")
):
    await interaction.response.send_message(text)

@bot.event
async def on_ready():
    print(f"✅ Bot đang chạy: {bot.user}")

bot.run(TOKEN)