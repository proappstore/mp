from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_db, save_db
from utils.calculator import calc_target
from utils.matcher import find_earliest_open_order
import time
import uuid

async def enter_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Enter amount between 0 and 10000 (coins). Example: 492")
    return 0  # ENTER_AMOUNT state

async def receive_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)
    text = update.message.text.strip()
    try:
        amt = int(text)
    except:
        await update.message.reply_text("Please enter a valid integer amount.")
        return 0
    if not (0 < amt <= 10000):
        await update.message.reply_text("Amount must be between 0 and 10,000.")
        return 0

    db = load_db()

    # Create user's new order
    order_id = f"ORD{int(time.time())}{str(uuid.uuid4())[:6]}"
    target = calc_target(amt)
    new_order = {
        "order_id": order_id,
        "owner": uid,
        "amount": amt,
        "target": target,
        "received": 0,
        "status": "open",
        "contributors": []
    }
    db["orders"].append(new_order)
    # link to user
    user_entry = db["users"].setdefault(uid, {"name": user.full_name, "upi": "", "wallet": 0, "orders": []})
    user_entry["orders"].append(order_id)
    save_db(db)

    # find earliest open order (exclude the newly created one)
    receiver_order = find_earliest_open_order(db, exclude_order_id=order_id)
    if not receiver_order:
        await update.message.reply_text(
            "No existing open orders to pay right now. Your order is created and waiting for contributors."
        )
        return ConversationHandler.END

    # Store state in context to continue flow
    context.user_data["buy_flow"] = {
        "amount": amt,
        "my_order_id": order_id,
        "assigned_receiver_order_id": receiver_order["order_id"],
    }

    # Show pay details (receiver UPI)
    receiver_owner = receiver_order["owner"]
    receiver_upi = db["users"].get(receiver_owner, {}).get("upi", "(not set)")
    await update.message.reply_text(
        f"Please pay the receiver.\nReceiver UPI: {receiver_upi}\n\nAfter paying, send the Transaction ID (text). Then you will send a screenshot (photo)."
    )
    return 1  # TXN_ID state