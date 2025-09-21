import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selamat datang di Chess Tele! Ketik /help untuk petunjuk.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Perintah yang tersedia:\n"
        "/start - Mulai bot\n"
        "/help - Tampilkan bantuan\n"
        "/newgame - Mulai game baru\n"
        "/move e2e4 - Melakukan langkah (contoh)\n"
        "/board - Tampilkan papan saat ini\n"
        "/resign - Menyerah\n"
    )
    await update.message.reply_text(help_text)

def main():
    import os
    token = os.getenv("TELEGRAM_TOKEN", "PASTE_TOKEN_BOT_MU_DI_SINI")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling()

if __name__ == "__main__":
    main()