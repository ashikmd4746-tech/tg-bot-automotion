import logging
import qrcode
from io import BytesIO
from PIL import Image
from pyzbar.pyzbar import decode
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# ================= TOKEN =================
TOKEN = os.getenv("TOKEN")

# ================= LOGGING =================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Advanced QR Bot\n\n"
        "📌 Commands:\n"
        "/qr <text> → Generate QR Code\n"
        "📷 Send QR Image → Scan QR Code"
    )

# ================= QR GENERATE =================
async def generate_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Example:\n/qr Hello World")
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

# ================= QR SCAN =================
async def scan_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        photo = update.message.photo[-1]
        file = await photo.get_file()

        path = "scan.png"
        await file.download_to_drive(path)

        img = Image.open(path)
        result = decode(img)

        if result:
            data = result[0].data.decode("utf-8")
            await update.message.reply_text(f"🔍 Result:\n{data}")
        else:
            await update.message.reply_text("❌ No QR found")

    except:
        await update.message.reply_text("❌ Error scanning QR")

# ================= MAIN =================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("qr", generate_qr))
    app.add_handler(MessageHandler(filters.PHOTO, scan_qr))

    print("🚀 Bot Running...")
    app.run_polling()

if name == "main":
    main()