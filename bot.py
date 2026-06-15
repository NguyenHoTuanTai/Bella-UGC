
from flask import Flask, request, jsonify
import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from threading import Thread
import os
import asyncio

app = Flask(__name__)

# =========================
# CONFIG
# =========================

TOKEN = os.environ.get("TOKEN")

# Thay bằng channel ID Discord của bạn
CHANNEL_ID = 1516082510050754693


# =========================
# FLASK
# =========================

@app.route('/')
def home():
    return "Bot online!"


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
            description=f"**{player_name}** vừa mua item!",
            color=0x00ff00
        )

        embed.add_field(
            name="👤 Player",
            value=player_name,
            inline=True
        )

        embed.add_field(
            name="🎁 Item",
            value=item_name,
            inline=True
        )

        embed.add_field(
            name="💰 Price",
            value=f"{item_price} Robux",
            inline=True
        )

        embed.add_field(
            name="🆔 Asset ID",
            value=asset_id,
            inline=False
        )

        if image_url:
            embed.set_thumbnail(url=image_url)

        embed.set_footer(text="Bella UGC Purchase")

        await channel.send(embed=embed)

    bot.loop.create_task(send_purchase_message())

    return jsonify({
        "success": True,
        "message": "Purchase received"
    })


def run_flask():
    app.run(
        host='0.0.0.0',
        port=8080
    )


Thread(
    target=run_flask,
    daemon=True
).start()


# =========================
# DISCORD BOT
# =========================

intents = nextcord.Intents.default()

bot = commands.Bot(
    intents=intents
)


@bot.slash_command(
    name="b",
    description="Bot nhắn lại nội dung bạn gửi"
)
async def b_command(
    interaction: nextcord.Interaction,
    text: str = SlashOption(
        description="Nội dung"
    )
):
    await interaction.response.send_message(text)


@bot.event
async def on_ready():
    print(f"✅ Bot đang chạy: {bot.user}")


bot.run(TOKEN)

