```markdown
# Telegram Coin-Based Order Matching Bot (JSON Storage)

This bot runs a virtual coin order system with JSON storage. Everything is local and virtual — no real money verification.

Quick Termux setup (recommended flow):

1. Install Python & pip in Termux (if not already):
   pkg update && pkg upgrade
   pkg install python git

2. Clone the project or copy files into a directory `coin_order_bot`.

3. Change to the project directory:
   cd coin_order_bot

4. (Optional) Create a virtual environment:
   python -m venv venv
   source venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Provide your Bot token:
   - Option A (recommended): export BOT_TOKEN="123456:ABC..."
   - Option B: Edit `config.py` and replace the placeholder.

7. Run the bot:
   python main.py

Notes for Termux:
- Termux is a mobile environment that supports Python well. The instructions above are normal pip installs.
- Keep the session alive or use tools like Termux:Boot, Termux:Widget, or a terminal multiplexer (tmux) if needed.

Project structure:
- main.py
- config.py
- requirements.txt
- data/db.json  (created automatically on first run)
- handlers/
- utils/
- constants/

Everything is stored in data/db.json.

Security and behavior:
- This bot does NOT validate any payment. Transaction IDs and screenshots are only records.
- Wallet balances are incremented only when orders are completed (received >= target).
- The matching logic assigns new orders to the oldest outstanding orders (FIFO).

If you run into permission issues writing data in Termux, ensure the working directory is accessible and create a `data` folder manually:
mkdir -p data && echo '{"users": {}, "orders": []}' > data/db.json
```