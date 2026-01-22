from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.storage import load_db, save_db
from utils.notifier import notify_receiver
import logging

logger = logging.getLogger(__name__)

async def receive_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    bf = context.user_data.get("buy_flow")
    if not bf:
        await update.message.reply_text("No active buy flow. Use the Buy Orders menu.")
        return ConversationHandler.END

    if not update.message.photo:
        await update.message.reply_text("Please send a photo as screenshot.")
        return 2

    file_id = update.message.photo[-1].file_id
    amt = bf["amount"]
    txn = bf.get("txn_id", "")
    assigned_order_id = bf["assigned_receiver_order_id"]

    db = load_db()
    # find receiver order
    rorder = next((o for o in db["orders"] if o["order_id"] == assigned_order_id), None)
    if not rorder:
        await update.message.reply_text("Receiver order not found. Aborting.")
        return ConversationHandler.END

    # append contributor
    contrib = {"from": uid, "amount": amt, "txn_id": txn, "screenshot": file_id}
    rorder.setdefault("contributors", []).append(contrib)
    rorder["received"] = int(rorder.get("received", 0)) + int(amt)

    # If completed, mark and credit wallet
    if int(rorder["received"]) >= int(rorder["target"]):
        rorder["status"] = "completed"
        # credit wallet of owner
        owner = rorder["owner"]
        db["users"].setdefault(owner, {"name": "", "upi": "", "wallet": 0, "orders": []})
        db["users"][owner]["wallet"] = int(db["users"][owner].get("wallet", 0)) + int(rorder["target"])
        
        # Also notify the owner that their order is completed and wallet credited
        try:
            await context.bot.send_message(
                chat_id=owner,
                text=f"✅ Your order {rorder['order_id']} has been fully completed!\nAmount received: {rorder['received']}\nYour wallet has been credited with {rorder['target']} coins (includes 3% extra)."
            )
        except Exception as e:
            logger.error(f"Failed to notify owner {owner}: {e}")

    save_db(db)

    # notify receiver
    await notify_receiver(db, rorder, contrib, context.bot)

    await update.message.reply_text("Payment recorded and receiver has been notified. Your order remains open to receive coins.")
    context.user_data.pop("buy_flow", None)
    return ConversationHandler.END
