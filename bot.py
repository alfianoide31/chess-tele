import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from game import ChessGame

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = os.getenv("TELEGRAM_TOKEN")
games = {}  # user_id -> ChessGame instance

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Selamat datang di Chess Tele! Ketik /help untuk petunjuk.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Mulai bot\n"
        "/help - Tampilkan bantuan\n"
        "/newgame - Mulai game baru\n"
        "/move e2e4 - Melakukan langkah (contoh)\n"
        "/board - Tampilkan papan saat ini\n"
        "/resign - Menyerah"
    )

async def newgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    games[user_id] = ChessGame()
    await update.message.reply_text(
        "Game baru dimulai! Putih jalan dulu.\n"
        "Ketik /board untuk melihat papan.\n"
        "Ketik /move <langkah> (misal: /move e2e4) untuk melangkah."
    )

async def move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in games:
        await update.message.reply_text("Kamu belum mulai game. Ketik /newgame untuk mulai main!")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Format: /move e2e4")
        return
    move_uci = context.args[0]
    game = games[user_id]
    success, error = game.move(move_uci)
    if success:
        board_text = game.get_board_text()
        msg = f"{board_text}\nGiliran: {game.get_turn()}"
        if game.is_game_over():
            msg += f"\nPermainan selesai! {game.get_result()}"
            del games[user_id]
        await update.message.reply_text(msg)
    else:
        await update.message.reply_text(error)

async def board(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in games:
        await update.message.reply_text("Kamu belum mulai game. Ketik /newgame untuk mulai main!")
        return
    game = games[user_id]
    await update.message.reply_text(game.get_board_text())

async def resign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in games:
        await update.message.reply_text("Kamu belum mulai game.")
        return
    color = game.get_turn()
    msg = games[user_id].resign(color)
    del games[user_id]
    await update.message.reply_text(msg)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("newgame", newgame))
    app.add_handler(CommandHandler("move", move))
    app.add_handler(CommandHandler("board", board))
    app.add_handler(CommandHandler("resign", resign))
    app.run_polling()