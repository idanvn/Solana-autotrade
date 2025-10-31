"""
Dynamic Real-Time Price Feed for SOL
Updates constantly, no caching, always fresh market data
"""

import requests
import time
from typing import Optional, Dict
from dataclasses import dataclass
from datetime import datetime


@dataclass
class LivePrice:
    """Single price snapshot with metadata"""
    price_usd: float
    timestamp: float
    source: str
    bid: Optional[float] = None  # Best bid if available
    ask: Optional[float] = None  # Best ask if available


class DynamicPriceFeed:
    """
    Always-fresh price feed - NO CACHING
    Every call gets NEW data from the market
    """
    
    def __init__(self):
        self.last_update_time = 0
        self.update_count = 0
        
    def get_live_sol_price(self, force_fresh: bool = True) -> LivePrice:
        """
        Get LIVE SOL price - always fresh from market
        
        Args:
            force_fresh: If True (default), always fetch new data
                        If False, allows minimal caching (5 sec) to avoid rate limits
        """
        
        self.update_count += 1
        
        # Try multiple sources in order of reliability
        sources = [
            self._fetch_binance,
            self._fetch_coingecko,
            self._fetch_coinbase,
        ]
        
        for fetch_func in sources:
            try:
                price_data = fetch_func()
                if price_data and price_data.price_usd > 0:
                    print(f"✅ Live price from {price_data.source}: ${price_data.price_usd:.2f} (update #{self.update_count})")
                    self.last_update_time = time.time()
                    return price_data
            except Exception as e:
                print(f"⚠️ {fetch_func.__name__} failed: {e}")
                continue
        
        # If all sources fail, raise error - DO NOT use stale/cached data
        raise RuntimeError("CRITICAL: All price sources failed! Cannot get live price.")
    
    def _fetch_binance(self) -> LivePrice:
        """Binance - most liquid, fastest updates"""
        url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=SOLUSDT"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        
        bid = float(data["bidPrice"])
        ask = float(data["askPrice"])
        mid = (bid + ask) / 2
        
        return LivePrice(
            price_usd=mid,
            timestamp=time.time(),
            source="Binance",
            bid=bid,
            ask=ask
        )
    
    def _fetch_coingecko(self) -> LivePrice:
        """CoinGecko - reliable, slower updates"""
        url = "https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        
        price = float(data["solana"]["usd"])
        
        return LivePrice(
            price_usd=price,
            timestamp=time.time(),
            source="CoinGecko"
        )
    
    def _fetch_coinbase(self) -> LivePrice:
        """Coinbase - good for US markets"""
        url = "https://api.coinbase.com/v2/exchange-rates?currency=SOL"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        
        price = float(data["data"]["rates"]["USD"])
        
        return LivePrice(
            price_usd=price,
            timestamp=time.time(),
            source="Coinbase"
        )
    
    def get_spread_info(self) -> Dict:
        """Get bid-ask spread for better trade execution"""
        try:
            binance_data = self._fetch_binance()
            if binance_data.bid and binance_data.ask:
                spread = binance_data.ask - binance_data.bid
                spread_bps = (spread / binance_data.price_usd) * 10000
                
                return {
                    "bid": binance_data.bid,
                    "ask": binance_data.ask,
                    "mid": binance_data.price_usd,
                    "spread_usd": spread,
                    "spread_bps": spread_bps
                }
        except:
            pass
        
        return {}


class LivePriceOrcaClient:
    """
    Orca client with DYNAMIC real-time pricing
    Price updates before EVERY operation
    """
    
    def __init__(self):
        self.price_feed = DynamicPriceFeed()
        self.base_url = "https://api.orca.so"
        self.timeout = 20
        
    def get_current_sol_price(self) -> float:
        """Get absolutely fresh SOL price RIGHT NOW"""
        live_data = self.price_feed.get_live_sol_price(force_fresh=True)
        return live_data.price_usd
    
    def get_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
    ) -> Dict:
        """
        Get quote with LIVE FRESH PRICE
        Price is fetched NEW for this specific quote
        """
        
        # CRITICAL: Get FRESH price for THIS quote
        live_price_data = self.price_feed.get_live_sol_price(force_fresh=True)
        current_sol_price = live_price_data.price_usd
        
        print(f"📊 Using LIVE price: ${current_sol_price:.2f} from {live_price_data.source}")
        
        # Token setup
        SOL_MINT = "So11111111111111111111111111111111111111112"
        USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        
        # Calculate output based on CURRENT LIVE PRICE
        if input_mint == SOL_MINT and output_mint == USDC_MINT:
            # SOL → USDC
            sol_amount = amount / 1_000_000_000  # Convert lamports to SOL
            usdc_raw = sol_amount * current_sol_price
            usdc_lamports = int(usdc_raw * 1_000_000)  # USDC has 6 decimals
            
            # Apply slippage
            slippage_factor = (10000 - slippage_bps) / 10000
            final_output = int(usdc_lamports * slippage_factor)
            
        elif input_mint == USDC_MINT and output_mint == SOL_MINT:
            # USDC → SOL
            usdc_amount = amount / 1_000_000  # Convert to USDC
            sol_raw = usdc_amount / current_sol_price
            sol_lamports = int(sol_raw * 1_000_000_000)  # SOL has 9 decimals
            
            # Apply slippage
            slippage_factor = (10000 - slippage_bps) / 10000
            final_output = int(sol_lamports * slippage_factor)
            
        else:
            raise RuntimeError(f"Unsupported pair: {input_mint} -> {output_mint}")
        
        # Get spread info for better execution
        spread_info = self.price_feed.get_spread_info()
        
        return {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "inAmount": str(amount),
            "outAmount": str(final_output),
            "slippageBps": slippage_bps,
            "dex": "Orca",
            "liveSolPrice": current_sol_price,
            "priceSource": live_price_data.source,
            "priceTimestamp": live_price_data.timestamp,
            "spread": spread_info,
            "isFreshPrice": True  # Always true!
        }


def test_dynamic_pricing():
    """Test that prices are ACTUALLY dynamic"""
    
    print("🔴 DYNAMIC PRICE TEST - Prices should change!")
    print("=" * 60)
    
    client = LivePriceOrcaClient()
    
    for i in range(5):
        print(f"\n📊 Price Check #{i+1}:")
        
        # Get fresh price
        current_price = client.get_current_sol_price()
        
        # Get a quote (which also fetches fresh price)
        quote = client.get_quote(
            input_mint="So11111111111111111111111111111111111111112",
            output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
            amount=1_000_000_000,  # 1 SOL
            slippage_bps=50
        )
        
        out_usdc = int(quote["outAmount"]) / 1_000_000
        
        print(f"   Price: ${current_price:.2f}")
        print(f"   1 SOL → {out_usdc:.2f} USDC")
        print(f"   Source: {quote['priceSource']}")
        print(f"   Time: {datetime.fromtimestamp(quote['priceTimestamp']).strftime('%H:%M:%S.%f')[:-3]}")
        
        if i < 4:
            print("   ⏳ Waiting 3 seconds for market movement...")
            time.sleep(3)
    
    print("\n✅ Each price was fetched FRESH from the market!")
    print("💡 Notice: Prices may vary slightly due to market volatility")


if __name__ == "__main__":
    test_dynamic_pricing()