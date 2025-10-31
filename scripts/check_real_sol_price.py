"""
Get REAL SOL price from multiple sources
"""

import requests
import json

def get_real_sol_price():
    """Get current SOL/USD price from real market data"""
    
    sources = []
    
    # Source 1: CoinGecko
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        data = r.json()
        price = data["solana"]["usd"]
        sources.append(("CoinGecko", price))
        print(f"CoinGecko: ${price:.2f}")
    except Exception as e:
        print(f"CoinGecko failed: {e}")
    
    # Source 2: Binance
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
        r = requests.get(url, timeout=10)
        data = r.json()
        price = float(data["price"])
        sources.append(("Binance", price))
        print(f"Binance: ${price:.2f}")
    except Exception as e:
        print(f"Binance failed: {e}")
    
    # Source 3: Coinbase
    try:
        url = "https://api.coinbase.com/v2/exchange-rates?currency=SOL"
        r = requests.get(url, timeout=10)
        data = r.json()
        price = float(data["data"]["rates"]["USD"])
        sources.append(("Coinbase", price))
        print(f"Coinbase: ${price:.2f}")
    except Exception as e:
        print(f"Coinbase failed: {e}")
    
    if not sources:
        print("❌ All price sources failed!")
        return None
    
    # Calculate average
    avg_price = sum(price for _, price in sources) / len(sources)
    print(f"\n📊 Average SOL Price: ${avg_price:.2f}")
    
    # Show differences
    max_price = max(price for _, price in sources)
    min_price = min(price for _, price in sources)
    spread = ((max_price - min_price) / avg_price) * 100
    print(f"📈 Highest: ${max_price:.2f}")
    print(f"📉 Lowest: ${min_price:.2f}")
    print(f"📊 Spread: {spread:.1f}%")
    
    return avg_price

if __name__ == "__main__":
    print("🔍 Fetching REAL SOL price from multiple sources...")
    print("=" * 50)
    
    real_price = get_real_sol_price()
    
    if real_price:
        mock_price = 139.30  # What the bot was showing
        error_pct = ((mock_price - real_price) / real_price) * 100
        
        print(f"\n🎯 COMPARISON:")
        print(f"   Bot mock price: ${mock_price:.2f}")
        print(f"   Real market price: ${real_price:.2f}")
        print(f"   Error: {error_pct:+.1f}%")
        
        if abs(error_pct) > 5:
            print("🚨 CRITICAL: Bot price is significantly wrong!")
            print("   This could cause massive trading errors!")
        else:
            print("✅ Bot price is reasonably accurate")
    else:
        print("❌ Could not fetch real price")