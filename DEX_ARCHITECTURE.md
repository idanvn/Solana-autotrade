# 🔄 DEX Architecture - How Trading Works

## 📊 Current Setup (Important!)

### 🎯 **Price Discovery vs Trade Execution**

הבוט מפריד בין **2 תהליכים שונים**:

---

## 1️⃣ **Price Discovery (קבלת מחירים) - Binance/CoinGecko/Coinbase**

### מה קורה:
הבוט מושך **מחירי שוק חיים** של SOL מבורסות מרכזיות:

```python
# backend/core/dynamic_price_feed.py
sources = [
    Binance API,      # Primary - fastest
    CoinGecko API,    # Backup 1
    Coinbase API,     # Backup 2
]
```

### למה לא מהDEX?
- ✅ **מהירות**: Binance מעדכן כל שנייה
- ✅ **דיוק**: נזילות עצומה = מחיר אמיתי
- ✅ **עצמאות**: לא תלוי בנזילות של הפול ב-Solana
- ✅ **Fallback**: אם מקור אחד נופל, יש גיבוי

### הוכחה:
```
📊 Check #1:
✅ Live price from Binance: $186.47
   (לא מ-Orca, לא מ-Jupiter!)
```

---

## 2️⃣ **Trade Execution (ביצוע עסקאות) - Orca DEX**

### מה קורה (כשנפעיל מסחר אמיתי):
כשהבוט **מחליט** לקנות/למכור, הוא ישלח טרנזקציה ל-**Orca DEX**:

```python
# backend/core/dynamic_price_feed.py - LivePriceOrcaClient
def swap_sol_to_usdc(amount):
    # 1. Get live price from Binance
    market_price = self.price_feed.get_live_sol_price()
    
    # 2. Calculate expected output
    expected_usdc = amount * market_price
    
    # 3. Execute swap on Orca DEX
    # TODO: Real swap implementation
```

### למה Orca?
- ✅ **נזילות טובה** ב-Solana
- ✅ **עמלות נמוכות** (~0.25%)
- ✅ **מהיר** - טרנזקציות ב-Solana
- ⚠️ **אבל**: כרגע לא מחובר (SIMULATION MODE)

---

## 🔄 **Flow מלא:**

```
1. [Binance API] → Get live SOL price: $186.47
                              ↓
2. [Bot Logic] → Detect 2% dip: Buy signal!
                              ↓
3. [Orca DEX] → Execute: Swap 5 USDC → SOL
                              ↓
4. [Wallet] → Receive SOL
```

---

## ⚙️ **Configuration (.env)**

```bash
# Price sources (currently active)
PRICE_SOURCE_BINANCE=https://api.binance.com      # ✅ In use
PRICE_SOURCE_COINGECKO=https://api.coingecko.com  # ✅ Backup
PRICE_SOURCE_COINBASE=https://api.coinbase.com    # ✅ Backup

# DEX for execution (ready, not active yet)
ORCA_BASE_URL=https://api.orca.so                 # ⏳ For future swaps

# Legacy (not used)
JUPITER_BASE_URL=https://quote-api.jup.ag         # ❌ Had DNS issues
```

---

## 🚀 **Future: Jupiter Integration**

### Why Jupiter would be better:
```python
# Jupiter = DEX Aggregator
# It finds the BEST price across:
- Orca
- Raydium  
- Serum
- Phoenix
- And 10+ more DEXs!
```

### Example:
```
Orca:    1 SOL → 185.20 USDC
Raydium: 1 SOL → 185.50 USDC
Phoenix: 1 SOL → 185.80 USDC
           ↓
Jupiter: Uses Phoenix! → 185.80 USDC (best price!)
```

**We'll add this when Jupiter DNS is fixed** 🔧

---

## 📋 **Summary Table**

| Component | Service | Purpose | Status |
|-----------|---------|---------|--------|
| **Price Feed** | Binance/CoinGecko/Coinbase | Real-time SOL price | ✅ Active |
| **Trade Execution** | Orca DEX | Swap SOL ↔ USDC | ⏳ Ready (simulation) |
| **Future Upgrade** | Jupiter Aggregator | Best price across all DEXs | 📅 Planned |

---

## 💡 **Why This Architecture?**

### Before (Wrong):
```
❌ Get price from DEX pool
❌ Pool might have low liquidity
❌ Price could be manipulated
❌ One source of failure
```

### Now (Correct):
```
✅ Get price from major exchanges (Binance)
✅ Massive liquidity = real market price
✅ Multiple fallbacks
✅ Execute on best available DEX
```

---

## 🔍 **Verify It Yourself**

Run the bot and watch:
```
📊 Check #1 - 11:34:50
   ✅ Live price from Binance: $186.47
   📊 Using LIVE price: $186.47 from Binance
```

**See?** Price from **Binance**, not Orca! 🎯

---

**Questions?** Read `SETUP.md` or check the code in `backend/core/dynamic_price_feed.py`
