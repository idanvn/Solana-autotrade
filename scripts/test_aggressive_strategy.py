"""
SOL Strategy with AGGRESSIVE price volatility to trigger buy/sell signals
"""

import sys
import time
import random
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.core.orca_client import OrcaClient  # noqa: E402
from backend.core.sol_strategy import SOLTradingStrategy, PricePoint  # noqa: E402


class AggressivePriceStrategy(SOLTradingStrategy):
    """Strategy with aggressive price swings for testing signals"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_price = 140.0
        self.volatility_mode = "normal"  # normal, crash, pump
        self.scenario_counter = 0
        
    def update_price(self) -> float:
        """Create dramatic price movements to test trading logic"""
        
        self.scenario_counter += 1
        
        # Create different market scenarios
        if self.scenario_counter <= 3:
            # Start normal
            change = random.uniform(-0.005, 0.005)  # ±0.5%
        elif self.scenario_counter <= 6:
            # Market crash! (trigger buy signals)
            change = random.uniform(-0.04, -0.01)  # -4% to -1%
            print(f"      🔥 MARKET CRASH SCENARIO!")
        elif self.scenario_counter <= 9:
            # Recovery pump (trigger sell signals)  
            change = random.uniform(0.01, 0.03)  # +1% to +3%
            print(f"      🚀 RECOVERY PUMP!")
        elif self.scenario_counter <= 12:
            # Volatile trading
            change = random.uniform(-0.02, 0.02)  # ±2%
        else:
            # Final crash to test stop-loss
            change = random.uniform(-0.03, -0.01)  # -3% to -1%
            print(f"      ⚠️ STOP-LOSS TEST!")
        
        self.base_price *= (1 + change)
        self.base_price = max(90, min(200, self.base_price))  # Wider bounds
        
        # Add to history
        point = PricePoint(
            timestamp=time.time(),
            sol_usdc_rate=self.base_price,
            volume_indicator=random.uniform(0.5, 2.0)
        )
        self.price_history.append(point)
        
        return self.base_price


def run_aggressive_simulation():
    """Test strategy with dramatic price moves"""
    
    print("🎢 AGGRESSIVE SOL Strategy Test")
    print("Creating dramatic price swings to test buy/sell logic...")
    print("=" * 65)
    
    orca = OrcaClient()
    strategy = AggressivePriceStrategy(
        orca_client=orca,
        buy_dip_threshold=2.0,   # Buy on 2% dips
        sell_rise_threshold=3.0,  # Sell on 3% rises  
        stop_loss_pct=5.0,       # 5% stop loss
        lookback_minutes=2,      # Very short for quick signals
        min_trade_usdc=30.0,
        max_trade_usdc=60.0
    )
    
    # Start with balanced portfolio
    strategy.update_balances(
        sol_balance=0.0,
        usdc_balance=300.0
    )
    
    print("🏦 Starting Portfolio: $300 USDC, 0 SOL")
    print()
    
    trade_log = []
    
    for i in range(15):
        print(f"📊 Round {i+1}")
        
        # Get price update
        price = strategy.update_price()
        
        # Show price change
        if len(strategy.price_history) > 1:
            prev_price = strategy.price_history[-2].sol_usdc_rate
            change_pct = ((price - prev_price) / prev_price) * 100
            
            if abs(change_pct) >= 2.0:
                emoji = "🔥" if change_pct < -2 else "🚀" if change_pct > 2 else "📊"
            else:
                emoji = "📉" if change_pct < 0 else "📈" if change_pct > 0 else "➡️"
                
            print(f"   {emoji} SOL: ${price:.2f} ({change_pct:+.1f}%)")
        else:
            print(f"   💰 SOL: ${price:.2f}")
        
        # Get signal
        signal = strategy.analyze_market()
        
        # Enhanced signal display
        action_emoji = {"BUY_SOL": "🛒", "SELL_SOL": "💸", "HOLD": "⏸️"}[signal.action]
        confidence_stars = "⭐" * int(signal.confidence * 5)
        
        print(f"   {action_emoji} Signal: {signal.action} {confidence_stars}")
        print(f"   📝 {signal.reason}")
        
        # Execute trades with detailed logging
        if signal.action == "BUY_SOL" and strategy.usdc_balance >= 30:
            print("   🛒 EXECUTING BUY ORDER...")
            
            amount = min(60.0, strategy.usdc_balance * 0.4)  # Use 40% of USDC
            sol_bought = (amount / price) * 0.995  # 0.5% slippage
            
            strategy.update_balances(
                sol_balance=strategy.sol_position + sol_bought,
                usdc_balance=strategy.usdc_balance - amount
            )
            strategy.last_buy_price = price
            
            trade_log.append(f"BUY: {sol_bought:.4f} SOL @ ${price:.2f} (${amount:.2f})")
            print(f"      ✅ Bought {sol_bought:.4f} SOL for ${amount:.2f}")
            
        elif signal.action == "SELL_SOL" and strategy.sol_position > 0.001:
            print("   💸 EXECUTING SELL ORDER...")
            
            sol_amount = strategy.sol_position
            usdc_received = (sol_amount * price) * 0.995
            
            # Calculate P&L
            profit_pct = 0
            if strategy.last_buy_price:
                profit_pct = ((price - strategy.last_buy_price) / strategy.last_buy_price) * 100
            
            strategy.update_balances(
                sol_balance=0.0,
                usdc_balance=strategy.usdc_balance + usdc_received
            )
            
            pnl_emoji = "💚" if profit_pct > 0 else "❤️" if profit_pct < -1 else "💙"
            trade_log.append(f"SELL: {sol_amount:.4f} SOL @ ${price:.2f} = {profit_pct:+.1f}% P&L")
            
            print(f"      ✅ Sold {sol_amount:.4f} SOL for ${usdc_received:.2f}")
            print(f"      {pnl_emoji} P&L: {profit_pct:+.1f}%")
            
            strategy.last_buy_price = None
        
        # Portfolio summary
        portfolio_val = strategy.usdc_balance + (strategy.sol_position * price)
        roi = ((portfolio_val / 300) - 1) * 100
        
        print(f"   💼 Portfolio: ${portfolio_val:.2f} (ROI: {roi:+.1f}%)")
        print(f"      💰 USDC: ${strategy.usdc_balance:.2f}")
        print(f"      🪙 SOL: {strategy.sol_position:.4f} (${strategy.sol_position * price:.2f})")
        
        time.sleep(1.5)  # Quick updates
        print()
    
    print("=" * 65)
    print("🏁 AGGRESSIVE SIMULATION COMPLETE!")
    print()
    
    # Final analysis
    final_price = strategy.price_history[-1].sol_usdc_rate
    final_value = strategy.usdc_balance + (strategy.sol_position * final_price)
    total_pnl = final_value - 300
    roi_pct = (total_pnl / 300) * 100
    
    print("📈 PERFORMANCE SUMMARY:")
    print(f"   Initial: $300.00")
    print(f"   Final: ${final_value:.2f}")
    print(f"   P&L: ${total_pnl:+.2f} ({roi_pct:+.1f}%)")
    print(f"   Trades executed: {len(trade_log)}")
    
    if trade_log:
        print("\n📋 TRADE LOG:")
        for trade in trade_log:
            print(f"   • {trade}")
    
    print("\n🎯 STRATEGY ANALYSIS:")
    if roi_pct > 5:
        print("🎉 EXCELLENT! Strategy generated strong profits")
    elif roi_pct > 0:
        print("✅ PROFITABLE! Strategy beat holding")  
    elif roi_pct > -2:
        print("🤝 BREAK-EVEN! Strategy preserved capital")
    else:
        print("⚠️ LOSS! Consider adjusting parameters")
    
    print(f"\n💡 Price range: ${min(p.sol_usdc_rate for p in strategy.price_history):.2f} - ${max(p.sol_usdc_rate for p in strategy.price_history):.2f}")


if __name__ == "__main__":
    run_aggressive_simulation()