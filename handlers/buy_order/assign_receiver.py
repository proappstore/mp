async def assign_receiver(update, context):
    await update.callback_query.message.reply_text(
        "Receiver assigned."
    )
