from telegram import InlineKeyboardButton, InlineKeyboardMarkup

MAIN_MENU = InlineKeyboardMarkup([
    [InlineKeyboardButton("Help", callback_data="help")],
    [InlineKeyboardButton("Buy Orders", callback_data="buy")],
    [InlineKeyboardButton("Orders History", callback_data="history")],
    [InlineKeyboardButton("Wallet", callback_data="wallet")],
    [InlineKeyboardButton("UPI ID Setup", callback_data="upi")]
])
