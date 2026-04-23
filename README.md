# 🤖 Binance Futures Testnet Trading Bot

A command-line trading bot that places **Market** and **Limit** orders on the **Binance Futures Testnet** using the `python-binance` SDK, with a polished CLI powered by **Typer** and **Rich**.

---

## 📋 Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.10+   |
| pip         | latest  |
| Git         | latest  |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone <repo-url>
cd ordex
```

### 2. Create & activate a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.example .env        # Linux / macOS
copy .env.example .env       # Windows
```

Open `.env` and replace the placeholder values with your **Binance Futures Testnet** credentials.

---

## 🔑 Getting Binance Futures Testnet API Keys

1. Navigate to **[https://testnet.binancefuture.com/](https://testnet.binancefuture.com/)**.
2. Click **Log In** and authenticate with your **GitHub** account.
3. Go to **API Key** section in the dashboard.
4. Generate a new API key pair.
5. Copy the **API Key** and **Secret Key** into your `.env` file.

> ⚠️ These are **testnet-only** keys — they work with fake funds and carry no financial risk.

---

## 🚀 Usage

### Place a MARKET BUY order

```bash
python cli.py place-order --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

### Place a LIMIT SELL order

```bash
python cli.py place-order --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.5 --price 1800.00
```

### View help

```bash
python cli.py --help
python cli.py place-order --help
```

---

## 📸 Sample Output

### Successful MARKET order

```
🚀 Binance Futures Testnet Trading Bot  v1.0.0

📋 Order Request
┌──────────────────────────────────┐
│  Symbol:     BTCUSDT             │
│  Side:       BUY                 │
│  Type:       MARKET              │
│  Quantity:   0.01                │
└──────────────────────────────────┘

✅ Order Placed Successfully
┌────────────┬──────────────┐
│ Field      │ Value        │
├────────────┼──────────────┤
│ orderId    │ 123456789    │
│ symbol     │ BTCUSDT      │
│ side       │ BUY          │
│ type       │ MARKET       │
│ status     │ FILLED       │
│ executedQty│ 0.01         │
│ avgPrice   │ 27350.50     │
└────────────┴──────────────┘
```

### Validation error

```
🚀 Binance Futures Testnet Trading Bot  v1.0.0

[ERROR] Validation failed: Invalid symbol 'BTC'. Symbol must end with 'USDT' (e.g. 'BTCUSDT').
```

---

## 📂 Log Files

| Detail        | Value                           |
|---------------|---------------------------------|
| Location      | `logs/ordex.log`          |
| Level (file)  | `DEBUG`                         |
| Level (console)| `INFO`                         |
| Max size      | 5 MB per file                   |
| Backups       | 3 rotated files                 |
| Format        | `%(asctime)s \| %(levelname)s \| %(module)s \| %(message)s` |

Logs are created automatically at runtime. The `logs/` directory is git-ignored.

---

## 📌 Assumptions

1. **Testnet only** — the bot is hard-coded to use `https://testnet.binancefuture.com`; it will **never** interact with real funds.
2. **Futures symbols** — all symbols must end with `USDT` (e.g. `BTCUSDT`, `ETHUSDT`).
3. **Order types** — only `MARKET` and `LIMIT` orders are supported; advanced types (STOP, TAKE_PROFIT, etc.) are out of scope.
4. **Time-in-Force** — LIMIT orders default to `GTC` (Good Till Cancelled).
5. **No portfolio management** — the bot places individual orders; it does not track positions or balances.
6. **Python 3.10+** — union type hints (`X | None`) require Python ≥ 3.10.

---

## 🗂️ Project Structure

```
ordex/
├── bot/
│   ├── __init__.py           # Package init
│   ├── client.py             # Binance client wrapper (testnet)
│   ├── orders.py             # Order placement logic
│   ├── validators.py         # Input validation
│   └── logging_config.py     # Dual-handler logging setup
├── cli.py                    # Typer CLI entry point
├── .env.example              # Template for API credentials
├── .gitignore                # Ignored files & dirs
├── logs/                     # Auto-created at runtime
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

---

## 📄 License

This project is provided for educational / internship assessment purposes.
