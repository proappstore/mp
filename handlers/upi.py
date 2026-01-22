from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from utils.storage import load_db, save_db
UPI_INPUT = 0

async def upi_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Send your UPI ID (example: user@upi). It is stored only as an identifier.")
    return UPI_INPUT

async def receive_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    upi = update.message.text.strip()
    db = load_db()
    if uid not in db["users"]:
        db["users"][uid] = {"name": user.full_name, "upi": upi, "wallet": 0, "orders": []}
    else:
        db["users"][uid]["upi"] = upi
    save_db(db)
    await update.message.reply_text(f"Your UPI ID has been set to: {upi}")
    return ConversationHandler.END

UPI_CONV = ConversationHandler(
    entry_points=[CallbackQueryHandler(upi_entry, pattern="^menu:upi$")],
    states={UPI_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_upi)]},
    fallbacks=[],
    per_user=True,
    per_chat=True,
)