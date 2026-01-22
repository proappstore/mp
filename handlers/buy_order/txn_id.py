from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_db, save_db

async def receive_txn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    txt = update.message.text.strip()
    bf = context.user_data.get("buy_flow")
    if not bf:
        await update.message.reply_text("No active buy flow. Use the Buy Orders menu.")
        return ConversationHandler.END
    bf["txn_id"] = txt
    await update.message.reply_text("Got the Transaction ID. Now please send a screenshot (photo) of the transaction.")
    return 2  # SCREENSHOT state