"""
🚀 LIVE SOL TRADING BOT - SIMPLE VERSION
Monitors SOL price and executes trades based on price movements
"""

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from core.wallet_manager import WalletManager
from core.dynamic_price_feed import LivePriceOrcaClient


class SimpleTradingBot:
    """Simple SOL trading bot with dynamic pricing"""
    
    def __init__(self, wallet_manager, dex_client):
        self.wallet = wallet_manager
        self.dex = dex_client
        
        # Trading parameters
        self.buy_dip_pct = 2.0          # Buy when price drops 2%
        self.sell_rise_pct = 2.0        # Sell when price rises 2%
        self.stop_loss_pct = 5.0        # Stop loss at 5%
        self.position_size_usd = 5.0    # Trade $5 at a time
        self.max_daily_trades = 10
        
        # State
        self.price_history = []
        self.position = None  # {"sol_amount": 0.1, "entry_price": 180.0}
        self.trades_today = 0
        self.total_pnl = 0.0
        
    def update_price(self):
        """Get fresh price and add to history"""
        current_price = self.dex.get_current_sol_price()
        
        self.price_history.append({
            "timestamp": time.time(),
            "price": current_price
        })
        
        # Keep only last 100 prices
        if len(self.price_history) > 100:
            self.price_history.pop(0)
        
        return current_price
    
    def get_recent_high(self):
        """Get highest price in last 30 minutes"""
        if not self.price_history:
            return None
        
        cutoff = time.time() - (30 * 60)
        recent = [p["price"] for p in self.price_history if p["timestamp"] >= cutoff]
        return max(recent) if recent else None
    
    def get_recent_low(self):
        """Get lowest price in last 30 minutes"""
        if not self.price_history:
            return None
        
        cutoff = time.time() - (30 * 60)
        recent = [p["price"] for p in self.price_history if p["timestamp"] >= cutoff]
        return min(recent) if recent else None
    
    def check_buy_signal(self, current_price):
        """Check if we should buy SOL"""
        
        # Don't buy if we already have a position
        if self.position:
            return False, "Already have position"
        
        # Don't buy if max trades reached
        if self.trades_today >= self.max_daily_trades:
            return False, "Max daily trades reached"
        
        # Check if price dropped enough
        recent_high = self.get_recent_high()
        if not recent_high:
            return False, "Not enough price history"
        
        drop_pct = ((recent_high - current_price) / recent_high) * 100
        
        if drop_pct >= self.buy_dip_pct:
            return True, f"Price dropped {drop_pct:.2f}% from ${recent_high:.2f}"
        
        return False, f"Waiting for {self.buy_dip_pct}% dip (current: {drop_pct:.2f}%)"
    
    def check_sell_signal(self, current_price):
        """Check if we should sell SOL"""
        
        # Can't sell if no position
        if not self.position:
            return False, "No position to sell"
        
        entry_price = self.position["entry_price"]
        
        # Check stop loss
        loss_pct = ((entry_price - current_price) / entry_price) * 100
        if loss_pct >= self.stop_loss_pct:
            return True, f"STOP LOSS: Down {loss_pct:.2f}% from ${entry_price:.2f}"
        
        # Check profit target
        profit_pct = ((current_price - entry_price) / entry_price) * 100
        if profit_pct >= self.sell_rise_pct:
            return True, f"PROFIT TARGET: Up {profit_pct:.2f}% from ${entry_price:.2f}"
        
        return False, f"Waiting for {self.sell_rise_pct}% rise (current: {profit_pct:.2f}%)"
    
    def execute_buy(self, current_price):
        """Execute buy order"""
        
        sol_amount = self.position_size_usd / current_price
        
        print(f"\n🟢 BUY SIGNAL")
        print(f"   Amount: {sol_amount:.6f} SOL")
        print(f"   Price: ${current_price:.2f}")
        print(f"   Cost: ${self.position_size_usd:.2f} USDC")
        
        confirm = input("\n   Execute this trade? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            # TODO: Add real swap execution here
            print("   ⚠️ SIMULATION MODE - Trade not executed")
            
            # Update position
            self.position = {
                "sol_amount": sol_amount,
                "entry_price": current_price,
                "entry_time": time.time()
            }
            self.trades_today += 1
            
            print(f"   ✅ Position opened: {sol_amount:.6f} SOL @ ${current_price:.2f}")
        else:
            print("   ❌ Trade cancelled")
    
    def execute_sell(self, current_price):
        """Execute sell order"""
        
        if not self.position:
            return
        
        sol_amount = self.position["sol_amount"]
        entry_price = self.position["entry_price"]
        usdc_received = sol_amount * current_price
        profit = (current_price - entry_price) * sol_amount
        profit_pct = ((current_price / entry_price) - 1) * 100
        
        print(f"\n🔴 SELL SIGNAL")
        print(f"   Amount: {sol_amount:.6f} SOL")
        print(f"   Entry Price: ${entry_price:.2f}")
        print(f"   Current Price: ${current_price:.2f}")
        print(f"   Receive: ${usdc_received:.2f} USDC")
        print(f"   Profit: ${profit:+.2f} ({profit_pct:+.2f}%)")
        
        confirm = input("\n   Execute this trade? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            # TODO: Add real swap execution here
            print("   ⚠️ SIMULATION MODE - Trade not executed")
            
            # Update stats
            self.total_pnl += profit
            self.trades_today += 1
            self.position = None
            
            print(f"   ✅ Position closed. P&L: ${profit:+.2f}")
        else:
            print("   ❌ Trade cancelled")
    
    def run(self):
        """Main trading loop"""
        
        print("🚀 SOL TRADING BOT - LIVE MODE")
        print("=" * 70)
        print(f"💼 Wallet: {self.wallet.pubkey()}")
        
        sol_balance = self.wallet.get_sol_balance()
        print(f"   SOL Balance: {sol_balance:.6f} SOL")
        
        current_price = self.dex.get_current_sol_price()
        print(f"   Current SOL Price: ${current_price:.2f}")
        print(f"   SOL Value: ${sol_balance * current_price:.2f}")
        
        print(f"\n📊 Trading Parameters:")
        print(f"   Buy on dip: {self.buy_dip_pct}%")
        print(f"   Sell on rise: {self.sell_rise_pct}%")
        print(f"   Stop loss: {self.stop_loss_pct}%")
        print(f"   Position size: ${self.position_size_usd}")
        print(f"   Max daily trades: {self.max_daily_trades}")
        
        print(f"\n🔴 MONITORING STARTED - Press Ctrl+C to stop")
        print("=" * 70)
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                
                # Get fresh price
                current_price = self.update_price()
                
                print(f"\n📊 Check #{iteration} - {time.strftime('%H:%M:%S')}")
                print(f"   LIVE Price: ${current_price:.2f}")
                
                # Check for signals
                if not self.position:
                    # Look for buy opportunity
                    should_buy, reason = self.check_buy_signal(current_price)
                    print(f"   📈 Buy check: {reason}")
                    
                    if should_buy:
                        self.execute_buy(current_price)
                
                else:
                    # Look for sell opportunity
                    should_sell, reason = self.check_sell_signal(current_price)
                    print(f"   📉 Sell check: {reason}")
                    
                    if should_sell:
                        self.execute_sell(current_price)
                    
                    # Show current position
                    pos = self.position
                    current_value = pos["sol_amount"] * current_price
                    unrealized_pnl = (current_price - pos["entry_price"]) * pos["sol_amount"]
                    unrealized_pct = ((current_price / pos["entry_price"]) - 1) * 100
                    
                    print(f"\n   📍 Active Position:")
                    print(f"      {pos['sol_amount']:.6f} SOL @ ${pos['entry_price']:.2f}")
                    print(f"      Current: ${current_price:.2f}")
                    print(f"      Value: ${current_value:.2f}")
                    print(f"      P&L: ${unrealized_pnl:+.2f} ({unrealized_pct:+.2f}%)")
                
                # Show stats
                if self.trades_today > 0:
                    print(f"\n   📈 Today: {self.trades_today} trades, P&L: ${self.total_pnl:+.2f}")
                
                # Heartbeat for Docker health check
                try:
                    with open("/app/logs/heartbeat.txt", "w") as f:
                        f.write(str(time.time()))
                except:
                    pass  # Not in Docker, ignore
                
                # Wait before next check
                print("   ⏳ Next check in 20 seconds...")
                time.sleep(20)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
            print(f"\n📊 Final Stats:")
            print(f"   Total trades: {self.trades_today}")
            print(f"   Total P&L: ${self.total_pnl:+.2f}")
            
            if self.position:
                print(f"\n   ⚠️ Open position: {self.position['sol_amount']:.6f} SOL")


def main():
    """Initialize and run the bot"""
    
    load_dotenv()
    rpc_url = os.getenv("RPC_URL")
    wallet_key = os.getenv("WALLET_PRIVATE_KEY_JSON")
    
    wallet = WalletManager(rpc_url=rpc_url)
    wallet.load_keypair_from_json_array(wallet_key)
    
    dex = LivePriceOrcaClient()
    
    bot = SimpleTradingBot(wallet, dex)
    bot.run()


if __name__ == "__main__":
    main()
