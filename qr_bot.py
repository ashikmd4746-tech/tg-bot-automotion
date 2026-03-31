import logging
import qrcode
from io import BytesIO
import os
from flask import Flask

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ===== TOKEN =====
TOKEN = os.getenv("TOKEN")

# ===== LOG =====
logging.basicConfig(level=logging.INFO)

# ===== FLASK SERVER (Render keep alive) =====
app_web = Flask(name)

@app_web.route('/')
def home():
    return "Bot is running!"

# ===== TELEGRAM BOT =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 QR Bot Live!\n\n"
        "/qr <text> → Generate QR Code"
    )

async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Use: /qr Hello")
        return

    text = " ".join(context.args)

    qr = qrcode.make(text)
    bio = BytesIO()
    bio.name = "qr.png"
    qr.save(bio, "PNG")
    bio.seek(0)

    await update.message.reply_photo(
        photo=bio,
        caption=f"✅ QR Generated:\n{text}"
    )

# ===== MAIN BOT =====
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("qr", generate_qr))

    print("🚀 Bot Running...")
    app.run_polling()

# ===== RUN BOTH =====
if name == "main":
    import threading

    # bot thread
    threading.Thread(target=run_bot).start()

    # web server (Render needs this)
    app_web.run(host="0.0.0.0", port=10000)
