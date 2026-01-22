WELCOME = "Welcome, {name}!\nThis bot runs a virtual coin order system. Use the menu below."
HELP_TEXT = (
    "Help — how this bot works:\n\n"
    "- Buy Orders: create an order. The bot will match your new order to the earliest existing open order and you will pay that receiver.\n"
    "- Wallet: shows your coin balance. Wallet is credited only when an order is fully completed (received >= target).\n"
    "- Orders are virtual coin transfers. No real money verification is done.\n"
    "- UPI ID: stored only as an identifier to show the receiver where to be paid.\n"
    "- Transaction ID and screenshot: these are records only — the bot does NOT verify real payments.\n\n"
    "Matching and calculation:\n- target = ceil(amount * 1.03)\n- Orders may be partially fulfilled by multiple contributors until target is reached.\n"
)
WALLET_TEXT = "Your wallet balance: {balance} coins"