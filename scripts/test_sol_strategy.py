"""
Test SOL Buy Low / Sell High Strategy
Simulates price monitoring and trading decisions
"""

import sys
import time
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.core.orca_client import OrcaClient  # noqa: E402
from backend.core.sol_strategy import SOLTradingStrategy  # noqa: E402

def simulate_trading_session():
    """Run a simulated trading session"""
    
    print("💰 SOL Trading Strategy Test")
    print("=" * 50)
    
    # Initialize
    orca = OrcaClient()
    strategy = SOLTradingStrategy(
        orca_client=orca,
        buy_dip_threshold=2.0,  # Buy on 2% dips (more sensitive)
        sell_rise_threshold=3.0,  # Sell on 3% rises
        stop_loss_pct=1.5,  # 1.5% stop loss
        min_trade_usdc=10.0,  # Min $10 trades
        max_trade_usdc=50.0   # Max $50 trades
    )
    
    # Simulate starting balances
    strategy.update_balances(
        sol_balance=0.0,    # Start with no SOL
        usdc_balance=100.0  # Start with $100 USDC
    )
    
    print(f"📊 Starting balances:")
    print(f"   SOL: {strategy.sol_position:.6f}")
    print(f"   USDC: ${strategy.usdc_balance:.2f}")
    print()
    
    # Simulation loop
    for i in range(5):
        print(f"🕐 Price Update #{i+1}")
        
        try:
            # Get current price
            current_price = strategy.update_price()
            print(f"   Current SOL price: ${current_price:.2f}")
            
            # Get trading signal
            signal = strategy.analyze_market()
            print(f"   Signal: {signal.action}")
            print(f"   Confidence: {signal.confidence:.1%}")
            print(f"   Reason: {signal.reason}")
            
            # Execute trades based on signal
            if signal.action == "BUY_SOL" and strategy.usdc_balance >= strategy.min_trade_usdc:
                print("   💸 EXECUTING BUY ORDER...")
                try:
                    result = strategy.execute_buy(signal)
                    expected_sol = int(result["quote"]["outAmount"]) / 1_000_000_000
                    usdc_spent = result["usdc_spent"]
                    
                    print(f"      ✅ Buy executed!")
                    print(f"      💰 Spent: ${usdc_spent:.2f} USDC")
                    print(f"      🪙 Expected SOL: {expected_sol:.6f}")
                    print(f"      📈 Price: ${result['price']:.2f}")
                    
                    # Update balances (simulation)
                    strategy.update_balances(
                        sol_balance=strategy.sol_position + expected_sol,
                        usdc_balance=strategy.usdc_balance - usdc_spent
                    )
                    
                except Exception as e:
                    print(f"      ❌ Buy failed: {e}")
            
            elif signal.action == "SELL_SOL" and strategy.sol_position > 0:
                print("   💰 EXECUTING SELL ORDER...")
                try:
                    result = strategy.execute_sell(signal)
                    expected_usdc = int(result["quote"]["outAmount"]) / 1_000_000
                    sol_sold = result["sol_sold"]
                    profit_loss = result["profit_loss_pct"]
                    
                    print(f"      ✅ Sell executed!")
                    print(f"      🪙 Sold: {sol_sold:.6f} SOL")
                    print(f"      💰 Received: ${expected_usdc:.2f} USDC")
                    print(f"      📊 P&L: {profit_loss:+.1f}%")
                    
                    # Update balances (simulation)
                    strategy.update_balances(
                        sol_balance=0.0,
                        usdc_balance=strategy.usdc_balance + expected_usdc
                    )
                    
                except Exception as e:
                    print(f"      ❌ Sell failed: {e}")
            
            else:
                print("   ⏸️  No action taken")
            
            # Show current balances
            total_value = strategy.usdc_balance + (strategy.sol_position * current_price)
            print(f"   💼 Current portfolio:")
            print(f"      SOL: {strategy.sol_position:.6f} (${strategy.sol_position * current_price:.2f})")
            print(f"      USDC: ${strategy.usdc_balance:.2f}")
            print(f"      Total Value: ${total_value:.2f}")
            
            if i < 4:  # Don't wait after last iteration
                print(f"   ⏳ Waiting 10 seconds for next update...")
                time.sleep(10)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 50)
    print("🏁 Trading session complete!")
    
    # Final summary
    final_price = strategy.price_history[-1].sol_usdc_rate if strategy.price_history else 0
    final_value = strategy.usdc_balance + (strategy.sol_position * final_price)
    
    print(f"📈 Final Results:")
    print(f"   Starting value: $100.00")
    print(f"   Final value: ${final_value:.2f}")
    print(f"   Total P&L: ${final_value - 100:.2f} ({(final_value/100-1)*100:+.1f}%)")
    print(f"   SOL position: {strategy.sol_position:.6f}")
    print(f"   USDC balance: ${strategy.usdc_balance:.2f}")

if __name__ == "__main__":
    simulate_trading_session()