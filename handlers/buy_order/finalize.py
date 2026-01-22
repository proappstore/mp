async def finalize_order(update, context):
    await update.message.reply_text(
        "Order finalized."
    )
