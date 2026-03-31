import logging
import qrcode
from io import BytesIO
import os
from flask import Flask

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

# ====== Flask keep alive ======
app_web = Flask(name)

@app_web.route('/')
def home():
    return "Bot is running!"

# ====== Telegram Bot ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 QR Bot\n\n"
        "/qr <text> → Generate QR"
    )

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /qr Hello")
        return

    text = " ".join(context.args)

    qr = qrcode.make(text)
    bio = BytesIO()
    bio.name = "qr.png"
    qr.save(bio, "PNG")
    bio.seek(0)

    await update.message.reply_photo(photo=bio)

def main():
    bot = ApplicationBuilder().token(TOKEN).build()

    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("qr", generate_qr))

    print("Bot Running...")
    bot.run_polling()

# ====== Run both ======
if name == "main":
    import threading
    threading.Thread(target=main).start()
    app_web.run(host="0.0.0.0", port=10000)
