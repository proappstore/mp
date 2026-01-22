from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import load_db

async def history_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = str(query.from_user.id)
    db = load_db()
    user = db["users"].get(uid)
    if not user:
        await query.edit_message_text("User not found. Send /start")
        return
    lines = []
    for oid in user.get("orders", []):
        order = next((o for o in db["orders"] if o["order_id"] == oid), None)
        if not order:
            continue
        contributors = ", ".join([f'{c["from"]}:{c["amount"]}' for c in order.get("contributors", [])]) or "None"
        lines.append(
            f'Order {order["order_id"]}: amount={order["amount"]}, target={order["target"]}, received={order["received"]}, status={order["status"]}, contributors={contributors}'
        )
    if not lines:
        text = "You have no orders."
    else:
        text = "Your orders:\n" + "\n\n".join(lines)
    await query.edit_message_text(text)