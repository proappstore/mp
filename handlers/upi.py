from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from utils.storage import load_db, save_db

# Helper to build the menu locally or import it to avoid circular imports
def build_menu():
    kb = [
        [InlineKeyboardButton("Help", callback_data="menu:help")],
        [InlineKeyboardButton("Buy Orders", callback_data="menu:buy")],
        [InlineKeyboardButton("Orders History", callback_data="menu:history")],
        [InlineKeyboardButton("Wallet", callback_data="menu:wallet")],
        [InlineKeyboardButton("UPI ID Setup", callback_data="menu:upi")],
    ]
    return InlineKeyboardMarkup(kb)

UPI_INPUT = 0

async def upi_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Send your UPI ID (example: user@upi). It is stored only as an identifier.")
    return UPI_INPUT

async def receive_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    upi_id = update.message.text.strip()
    
    # Simple validation
    if "@" not in upi_id:
        await update.message.reply_text("❌ Invalid UPI ID format. Please try again.")
        return UPI_INPUT
    
    db = load_db()
    if uid not in db["users"]:
        db["users"][uid] = {"name": user.full_name, "upi": upi_id, "wallet": 0, "orders": []}
    else:
        db["users"][uid]["upi"] = upi_id
    save_db(db)
    
    await update.message.reply_text(
        f"✅ UPI ID updated to: {upi_id}\n\nYour account is now fully set up and ready for buy orders!",
        reply_markup=build_menu()
    )
    return ConversationHandler.END

UPI_CONV = ConversationHandler(
    entry_points=[CallbackQueryHandler(upi_entry, pattern="^menu:upi$")],
    states={UPI_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_upi)]},
    fallbacks=[],
    per_user=True,
    per_chat=True,
)
