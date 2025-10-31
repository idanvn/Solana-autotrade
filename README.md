# 🚀 Solana SOL Trading Bot (2025)

**Automated Solana trading bot** with live pricing, buy-low-sell-high strategy, and Docker support.

## ⚡ Quick Start

### Option 1: Standard Run
```powershell
# 1. Setup .env
Copy-Item .env.example .env
# Edit .env with your QuickNode RPC + Solflare wallet

# 2. Run
python .\scripts\run_live_bot.py
```

### Option 2: Docker (Recommended) 🐋
```powershell
# 1. Ensure Docker Desktop is running
# 2. Run
.\docker_start.ps1
```

📖 **For detailed guide:** See [SETUP.md](SETUP.md) or [DOCKER_README.md](DOCKER_README.md)

---

## 📦 What's Included

### 🎯 **Core Code:**
- `backend/core/wallet_manager.py` — Solflare wallet management + transaction signing
- `backend/core/dynamic_price_feed.py` — **Live prices** from Binance/CoinGecko (no caching!)
- `backend/core/orca_client.py` — Orca DEX integration
- `backend/core/price_monitor.py` — Signal detection (volume spikes, momentum)
- `scripts/run_live_bot.py` — **Main bot** - checks every 20 seconds

### 🐋 **Docker:**
- `Dockerfile` — Container definition
- `docker-compose.yml` — Orchestration
- `docker_start.ps1` / `docker_stop.ps1` — Management scripts

### 📚 **Documentation:**
- `SETUP.md` — QuickNode + Solflare setup
- `DOCKER_README.md` — Quick Docker guide
- `DOCKER_GUIDE.md` — Advanced Docker
- `HOW_TO_RUN.md` — All run methods
- `CRITICAL_FIXES_2025.md` — Important solana-py 2025 fixes

### ⚙️ **Configuration:**
- `.env.example` — Configuration template (copy to `.env`)
- `requirements.txt` — Python dependencies
- `.gitignore` — Protects secrets from Git

---

## 🎯 How It Works

The bot runs a simple but effective strategy:

```
1. 🔄 Fetches live SOL price every 20 seconds
2. 📊 Compares with recent prices (30 minutes)
3. 📉 Buy: If price drops 2% from recent high
4. 📈 Sell: If price rises 2% from entry
5. 🛑 Stop Loss: If price drops 5% from entry
```

### 💡 **Example:**
```
Recent high: $200
Current price: $196 (2% drop)
→ 🟢 Buy 1 SOL at $196

Price rises to $200 (2% gain)
→ 🔴 Sell 1 SOL at $200

Profit: $4 💰
```

---

## 📊 Parameters

Customizable in `scripts/run_live_bot.py`:

```python
self.buy_dip_pct = 2.0           # Buy on 2% dip
self.sell_rise_pct = 2.0         # Sell on 2% rise  
self.stop_loss_pct = 5.0         # Stop loss at 5%
self.position_size_usd = 5.0     # Trade size ($5)
self.max_daily_trades = 10       # Max trades per day
```

Check interval:
```python
time.sleep(20)  # Every 20 seconds (change to 30, 60, etc.)
```

---

## ⚠️ Important Warnings!

### 🔴 **Bot is Currently in SIMULATION MODE**
- Does **NOT execute real trades**
- Only **shows** what it would do
- Safe for learning and testing

### 🔐 **Security:**
- ✅ **Use TEST wallet ONLY** - not your main wallet!
- ✅ Backup your Recovery Phrase in a safe place
- ✅ **NEVER share** your `.env` file
- ✅ Verify `.env` is in `.gitignore` before commits

### 💰 **Risks:**
- Crypto trading is risky - you can lose money
- Start with **very small amounts** ($1-5)
- Check logs **daily**
- Don't invest what you can't afford to lose

---

## 🛠️ Troubleshooting

### Bot won't start:
```powershell
# Check Python version
python --version  # Need 3.10+

# Check dependencies
pip list

# Verify .env exists
Test-Path .env
```

### RPC error:
- Verify QuickNode endpoint is correct
- Try accessing it in a browser (should return JSON)

### Wallet error:
- Check WALLET_PRIVATE_KEY_JSON has 64 numbers
- Ensure no spaces or weird characters

### Docker not working:
```powershell
# Check Docker is running
docker version

# Check logs
docker-compose logs
```

---

## 📚 Additional Documentation

| File | Description |
|------|-------------|
| [SETUP.md](SETUP.md) | QuickNode + Solflare setup (step-by-step) |
| [DOCKER_README.md](DOCKER_README.md) | Docker quick start guide |
| [DOCKER_GUIDE.md](DOCKER_GUIDE.md) | Advanced Docker - all commands |
| [HOW_TO_RUN.md](HOW_TO_RUN.md) | All run methods (manual, background, Task Scheduler) |
| [CRITICAL_FIXES_2025.md](CRITICAL_FIXES_2025.md) | Important solana-py 2025 fixes |
| [DEX_ARCHITECTURE.md](DEX_ARCHITECTURE.md) | How price feeds and DEX execution work |

---

## 🎯 Roadmap

- [x] Dynamic real-time pricing
- [x] Buy-low-sell-high strategy
- [x] Docker support
- [x] Automatic health checks
- [ ] Real trade execution (requires manual activation)
- [ ] Multiple pairs support (SOL/USDC, SOL/USDT)
- [ ] Telegram notifications
- [ ] Web dashboard

---

## 🤝 Contributing

Want to improve? Pull Requests are welcome!

1. Fork the project
2. Create a new branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📄 License

MIT License - Use at your own risk.

---

## ⚡ Quick Start Commands

```powershell
# Clone
git clone https://github.com/idanvn/Solana-autotrade.git
cd Solana-autotrade

# Setup
Copy-Item .env.example .env
# Edit .env with your credentials

# Run
python .\scripts\run_live_bot.py

# Or with Docker
.\docker_start.ps1
```

---

**Happy trading! 🚀💰**

> ⚠️ **Disclaimer:** This project is for educational purposes only. Crypto trading is risky and you are responsible for your actions. Always do your own research (DYOR).
