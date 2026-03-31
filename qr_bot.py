import logging
import qrcode
from io import BytesIO
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

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
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("qr", generate_qr))

    print("Bot Running...")
    app.run_polling()

if name == "main":
    main()
