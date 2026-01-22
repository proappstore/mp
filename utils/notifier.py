from telegram import InputMediaPhoto

async def notify_receiver(db, receiver_order, contrib, bot):
    owner_id = int(receiver_order["owner"])
    sender_id = int(contrib["from"])
    amount = contrib["amount"]
    txn = contrib.get("txn_id", "")
    screenshot_file_id = contrib.get("screenshot")
    # Build message
    text = f"You have received a payment notification.\nFrom user: {sender_id}\nAmount: {amount}\nTransaction ID: {txn}\nOrder ID: {receiver_order['order_id']}"
    try:
        # Send text first
        await bot.send_message(chat_id=owner_id, text=text)
        # Send screenshot if available
        if screenshot_file_id:
            await bot.send_photo(chat_id=owner_id, photo=screenshot_file_id, caption="Payment screenshot (for record)")
    except Exception as e:
        # best-effort notify; ignore exceptions
        print("notify_receiver error:", e)