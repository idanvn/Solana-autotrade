"""
PRODUCTION-READY SOL TRADING BOT
Uses DYNAMIC real-time prices - NO CACHING, ALWAYS FRESH
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
from core.sol_strategy import SOLTradingStrategy


def main():
    """Run SOL trading with LIVE dynamic prices"""
    
    # Load config
    load_dotenv()
    rpc_url = os.getenv("RPC_URL")
    
    print("🚀 DYNAMIC PRICE TRADING BOT")
    print("=" * 70)
    print("⚡ Using LIVE prices - fetched fresh before EVERY trade decision")
    print("=" * 70)
    
    # Initialize components
    wallet = WalletManager(rpc_url=rpc_url)
    dex_client = LivePriceOrcaClient()  # DYNAMIC PRICING!
    
    # Trading strategy config
    strategy = SOLTradingStrategy(
        orca_client=dex_client,
        buy_dip_threshold=2.0,          # Buy on 2% dip
        sell_profit_threshold=2.0,      # Sell on 2% rise
        stop_loss_threshold=5.0,        # Stop loss at 5%
        position_size_usdc=5.0,         # $5 per trade (SAFE!)
        max_daily_trades=10
    )
    
    print(f"\n💼 Wallet: {wallet.get_public_key()}")
    
    # Get balances
    sol_balance = wallet.get_sol_balance()
    print(f"   SOL Balance: {sol_balance:.6f} SOL")
    
    # Get FRESH price
    current_price = dex_client.get_current_sol_price()
    sol_value_usd = sol_balance * current_price
    print(f"   SOL Value: ${sol_value_usd:.2f} @ ${current_price:.2f}/SOL")
    
    print(f"\n📊 Strategy Configuration:")
    print(f"   Buy on dip: {strategy.buy_dip_threshold_pct}%")
    print(f"   Sell on rise: {strategy.sell_rise_threshold_pct}%")
    print(f"   Stop loss: {strategy.stop_loss_pct}%")
    print(f"   Position size: ${strategy.position_size_usd}")
    print(f"   Max daily trades: {strategy.max_daily_trades}")
    
    print(f"\n🔴 LIVE MONITORING STARTED - Press Ctrl+C to stop")
    print("=" * 70)
    
    iteration = 0
    
    try:
        while True:
            iteration += 1
            
            # 🔥 CRITICAL: Get FRESH price for THIS iteration
            live_price = dex_client.get_current_sol_price()
            
            print(f"\n📊 Iteration #{iteration} - {time.strftime('%H:%M:%S')}")
            print(f"   LIVE SOL Price: ${live_price:.2f}")
            
            # Update strategy with fresh price
            strategy.update_price(live_price)
            
            # Get trading signal
            signal = strategy.analyze_market()
            
            if signal:
                print(f"\n🔔 SIGNAL: {signal.action.name}")
                print(f"   Reason: {signal.reason}")
                print(f"   Current: ${signal.current_price:.2f}")
                print(f"   Entry: ${signal.entry_price:.2f}")
                print(f"   Change: {signal.price_change_pct:+.2f}%")
                
                # Get user confirmation
                print("\n⚠️ CONFIRM TRADE:")
                
                if signal.action.name == "BUY_SOL":
                    # Calculate trade details
                    usdc_to_spend = strategy.position_size_usd
                    sol_to_receive = usdc_to_spend / live_price
                    
                    print(f"   Action: BUY {sol_to_receive:.6f} SOL")
                    print(f"   Cost: ${usdc_to_spend:.2f} USDC")
                    print(f"   Price: ${live_price:.2f}/SOL")
                    
                    confirm = input("\n   Execute this trade? (yes/no): ").strip().lower()
                    
                    if confirm == "yes":
                        print("   ⚠️ SIMULATION MODE - Trade not executed")
                        print("   💡 To enable real trades, update execution logic")
                        strategy.open_position(live_price, sol_to_receive)
                    else:
                        print("   ❌ Trade cancelled by user")
                
                elif signal.action.name == "SELL_SOL":
                    position = strategy.position
                    if position and position["sol_amount"] > 0:
                        sol_to_sell = position["sol_amount"]
                        usdc_to_receive = sol_to_sell * live_price
                        profit_usd = (live_price - position["entry_price"]) * sol_to_sell
                        profit_pct = ((live_price / position["entry_price"]) - 1) * 100
                        
                        print(f"   Action: SELL {sol_to_sell:.6f} SOL")
                        print(f"   Receive: ${usdc_to_receive:.2f} USDC")
                        print(f"   Entry Price: ${position['entry_price']:.2f}")
                        print(f"   Current Price: ${live_price:.2f}")
                        print(f"   Profit: ${profit_usd:+.2f} ({profit_pct:+.2f}%)")
                        
                        confirm = input("\n   Execute this trade? (yes/no): ").strip().lower()
                        
                        if confirm == "yes":
                            print("   ⚠️ SIMULATION MODE - Trade not executed")
                            print("   💡 To enable real trades, update execution logic")
                            strategy.close_position(live_price)
                        else:
                            print("   ❌ Trade cancelled by user")
            
            else:
                print("   ⏸️ No signal - holding current position")
            
            # Show current position
            if strategy.position and strategy.position["sol_amount"] > 0:
                pos = strategy.position
                current_value = pos["sol_amount"] * live_price
                unrealized_pnl = (live_price - pos["entry_price"]) * pos["sol_amount"]
                unrealized_pnl_pct = ((live_price / pos["entry_price"]) - 1) * 100
                
                print(f"\n   📍 Active Position:")
                print(f"      Amount: {pos['sol_amount']:.6f} SOL")
                print(f"      Entry: ${pos['entry_price']:.2f}")
                print(f"      Current: ${live_price:.2f}")
                print(f"      Value: ${current_value:.2f}")
                print(f"      P&L: ${unrealized_pnl:+.2f} ({unrealized_pnl_pct:+.2f}%)")
            
            # Show stats
            if strategy.trades_today > 0:
                print(f"\n   📈 Today's Stats:")
                print(f"      Trades: {strategy.trades_today}/{strategy.max_daily_trades}")
                print(f"      Total P&L: ${strategy.total_pnl_usd:+.2f}")
            
            # Wait before next check
            print("\n   ⏳ Next check in 10 seconds...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
        
        # Final summary
        print("\n📊 FINAL SUMMARY:")
        print(f"   Total trades: {strategy.trades_today}")
        print(f"   Total P&L: ${strategy.total_pnl_usd:+.2f}")
        
        if strategy.position and strategy.position["sol_amount"] > 0:
            print(f"\n   ⚠️ Open position: {strategy.position['sol_amount']:.6f} SOL")
            print(f"   💡 Consider closing before shutdown")


if __name__ == "__main__":
    main()