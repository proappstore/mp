#!/usr/bin/env python3
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, CommandHandler,
    ContextTypes, ConversationHandler, MessageHandler, filters
)
import config
from handlers import start as start_h
from handlers import help as help_h
from handlers import wallet as wallet_h
from handlers import history as history_h
from handlers import upi as upi_h
from handlers.buy_order import enter_amount as bo_enter
from handlers.buy_order import assign_receiver as bo_assign
from handlers.buy_order import txn_id as bo_txn
from handlers.buy_order import screenshot as bo_ss

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Buy order conversation states
ENTER_AMOUNT, ASSIGN_RECEIVER, TXN_ID, SCREENSHOT = range(4)


async def main():
    if config.BOT_TOKEN is None or config.BOT_TOKEN == "REPLACE_WITH_YOUR_TOKEN":
        print("Please set the BOT_TOKEN in config.py or export BOT_TOKEN env var.")
        return

    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Command /start
    application.add_handler(CommandHandler("start", start_h.start))

    # CallbackQuery menu handler
    application.add_handler(CallbackQueryHandler(start_h.menu_handler, pattern="^menu:"))

    # Help, Wallet, History, UPI handlers (callback)
    application.add_handler(CallbackQueryHandler(help_h.help_handler, pattern="^menu:help$"))
    application.add_handler(CallbackQueryHandler(wallet_h.wallet_handler, pattern="^menu:wallet$"))
    application.add_handler(CallbackQueryHandler(history_h.history_handler, pattern="^menu:history$"))
    application.add_handler(CallbackQueryHandler(upi_h.upi_entry, pattern="^menu:upi$"))

    # UPI conversation
    application.add_handler(upi_h.UPI_CONV)

    # Buy order conversation
    buy_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(bo_enter.enter_amount, pattern="^menu:buy$")],
        states={
            ENTER_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bo_enter.receive_amount)],
            TXN_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, bo_txn.receive_txn)],
            SCREENSHOT: [MessageHandler(filters.PHOTO, bo_ss.receive_screenshot)],
        },
        fallbacks=[CommandHandler("start", start_h.start)],
        per_user=True,
        per_chat=True,
    )
    application.add_handler(buy_conv)

    # Start the bot
    print("Bot starting...")
    await application.run_polling()


if __name__ == "__main__":
    asyncio.run(main())