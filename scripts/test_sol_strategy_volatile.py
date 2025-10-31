"""
SOL Price Strategy with Simulated Price Movement
Creates realistic price volatility to test buy/sell signals
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
from backend.core.sol_strategy import SOLTradingStrategy  # noqa: E402


class SimulatedPriceStrategy(SOLTradingStrategy):
    """Strategy with simulated price movements for testing"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_price = 139.30  # Start at current Orca price
        self.price_trend = 0.0    # Current trend direction
        
    def update_price(self) -> float:
        """Generate realistic SOL price movement"""
        
        # Add some random volatility (-2% to +2%)
        volatility = random.uniform(-0.02, 0.02)
        
        # Add trend momentum (trends persist)
        trend_change = random.uniform(-0.005, 0.005)
        self.price_trend += trend_change
        self.price_trend = max(-0.03, min(0.03, self.price_trend))  # Cap at ±3%
        
        # Calculate new price
        price_change = volatility + self.price_trend
        self.base_price *= (1 + price_change)
        
        # Keep price reasonable (don't let it crash to $0 or moon to $1000)
        self.base_price = max(100, min(200, self.base_price))
        
        # Add to price history (same as parent class)
        from backend.core.sol_strategy import PricePoint
        point = PricePoint(
            timestamp=time.time(),
            sol_usdc_rate=self.base_price,
            volume_indicator=random.uniform(0.8, 1.2)  # Simulated volume
        )
        self.price_history.append(point)
        
        return self.base_price


def simulate_volatile_trading():
    """Run trading simulation with volatile prices"""
    
    print("📈📉 SOL Strategy with Simulated Price Volatility")
    print("=" * 60)
    
    # Initialize with simulated price feeds
    orca = OrcaClient()  # We'll override the price updates
    strategy = SimulatedPriceStrategy(
        orca_client=orca,
        buy_dip_threshold=1.5,  # Buy on 1.5% dips (sensitive)
        sell_rise_threshold=2.0,  # Sell on 2% rises
        stop_loss_pct=3.0,      # 3% stop loss
        lookback_minutes=5,     # Shorter lookback for simulation
        min_trade_usdc=20.0,    # Min $20 trades
        max_trade_usdc=40.0     # Max $40 trades
    )
    
    # Starting balances
    strategy.update_balances(
        sol_balance=0.0,    # Start with no SOL
        usdc_balance=200.0  # Start with $200 USDC
    )
    
    print("💼 Starting Portfolio:")
    print(f"   SOL: {strategy.sol_position:.6f}")
    print(f"   USDC: ${strategy.usdc_balance:.2f}")
    print(f"   Total Value: ${strategy.usdc_balance:.2f}")
    print()
    
    total_trades = 0
    
    # Longer simulation with more price updates
    for i in range(15):
        print(f"⏰ Update #{i+1}")
        
        try:
            # Get simulated price
            current_price = strategy.update_price()
            
            # Show price movement
            if len(strategy.price_history) > 1:
                prev_price = strategy.price_history[-2].sol_usdc_rate
                change_pct = ((current_price - prev_price) / prev_price) * 100
                change_symbol = "📈" if change_pct > 0 else "📉" if change_pct < 0 else "➡️"
                print(f"   {change_symbol} SOL: ${current_price:.2f} ({change_pct:+.1f}%)")
            else:
                print(f"   💰 SOL: ${current_price:.2f}")
            
            # Get signal
            signal = strategy.analyze_market()
            confidence_bar = "█" * int(signal.confidence * 10)
            print(f"   🎯 Signal: {signal.action} [{confidence_bar:<10}] {signal.confidence:.0%}")
            print(f"   📝 {signal.reason}")
            
            # Execute trades
            if signal.action == "BUY_SOL" and strategy.usdc_balance >= strategy.min_trade_usdc:
                print("   🛒 BUYING SOL...")
                try:
                    # Simulate the buy (no real Orca call)
                    usdc_amount = min(signal.suggested_amount_usdc or strategy.max_trade_usdc, strategy.usdc_balance)
                    sol_received = (usdc_amount / current_price) * 0.995  # 0.5% fees
                    
                    strategy.update_balances(
                        sol_balance=strategy.sol_position + sol_received,
                        usdc_balance=strategy.usdc_balance - usdc_amount
                    )
                    strategy.last_buy_price = current_price
                    total_trades += 1
                    
                    print(f"      ✅ Bought {sol_received:.6f} SOL for ${usdc_amount:.2f}")
                    
                except Exception as e:
                    print(f"      ❌ Buy failed: {e}")
                    
            elif signal.action == "SELL_SOL" and strategy.sol_position > 0.001:
                print("   💸 SELLING SOL...")
                try:
                    # Simulate the sell
                    sol_amount = strategy.sol_position
                    usdc_received = (sol_amount * current_price) * 0.995  # 0.5% fees
                    
                    # Calculate P&L
                    profit_loss = 0.0
                    if strategy.last_buy_price:
                        profit_loss = ((current_price - strategy.last_buy_price) / strategy.last_buy_price) * 100
                    
                    strategy.update_balances(
                        sol_balance=0.0,
                        usdc_balance=strategy.usdc_balance + usdc_received
                    )
                    strategy.last_buy_price = None
                    total_trades += 1
                    
                    pnl_symbol = "💚" if profit_loss > 0 else "❤️" if profit_loss < 0 else "💙"
                    print(f"      ✅ Sold {sol_amount:.6f} SOL for ${usdc_received:.2f}")
                    print(f"      {pnl_symbol} P&L: {profit_loss:+.1f}%")
                    
                except Exception as e:
                    print(f"      ❌ Sell failed: {e}")
            
            # Portfolio status
            portfolio_value = strategy.usdc_balance + (strategy.sol_position * current_price)
            roi = ((portfolio_value / 200.0) - 1) * 100
            
            print(f"   💼 Portfolio: ${portfolio_value:.2f} (ROI: {roi:+.1f}%)")
            print(f"      SOL: {strategy.sol_position:.6f} | USDC: ${strategy.usdc_balance:.2f}")
            
            # Brief pause
            time.sleep(2)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 60)
    print("🏁 SIMULATION COMPLETE")
    
    # Final results
    final_price = strategy.price_history[-1].sol_usdc_rate
    final_value = strategy.usdc_balance + (strategy.sol_position * final_price)
    total_return = final_value - 200.0
    roi_pct = (total_return / 200.0) * 100
    
    print("📊 FINAL RESULTS:")
    print(f"   Starting value: $200.00")
    print(f"   Final value: ${final_value:.2f}")
    print(f"   Total return: ${total_return:+.2f} ({roi_pct:+.1f}%)")
    print(f"   Total trades: {total_trades}")
    print(f"   SOL position: {strategy.sol_position:.6f}")
    print(f"   USDC balance: ${strategy.usdc_balance:.2f}")
    print(f"   Final SOL price: ${final_price:.2f}")
    
    # Performance summary
    if roi_pct > 0:
        print("🎉 PROFITABLE STRATEGY!")
    elif roi_pct == 0:
        print("🤝 BREAK-EVEN STRATEGY")
    else:
        print("⚠️  Strategy lost money - consider adjusting parameters")


if __name__ == "__main__":
    simulate_volatile_trading()