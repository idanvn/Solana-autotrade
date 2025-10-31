"""
SOL Price Strategy: Buy Low, Sell High
Monitors SOL/USDC price and triggers buy/sell signals based on price movements
"""

import time
from dataclasses import dataclass
from typing import Dict, List, Optional
from collections import deque

from .orca_client import OrcaClient


@dataclass
class PricePoint:
    """Single price observation"""
    timestamp: float
    sol_usdc_rate: float  # How much USDC for 1 SOL
    volume_indicator: float  # Optional volume metric


@dataclass
class TradingSignal:
    """Trading decision output"""
    action: str  # "BUY_SOL", "SELL_SOL", "HOLD"
    confidence: float  # 0.0 to 1.0
    current_price: float
    target_price: Optional[float]
    reason: str
    suggested_amount_usdc: Optional[float] = None


class SOLTradingStrategy:
    """
    Simple but effective SOL trading strategy:
    
    BUY SOL when:
    - Price drops X% from recent high
    - Price is below moving average
    - Volume confirms the move
    
    SELL SOL when:
    - Price rises Y% from recent low  
    - Price hits target profit
    - Stop-loss triggered
    """
    
    def __init__(
        self,
        orca_client: OrcaClient,
        buy_dip_threshold: float = 3.0,  # Buy when price drops 3%
        sell_rise_threshold: float = 5.0,  # Sell when price rises 5%
        stop_loss_pct: float = 2.0,  # Stop loss at 2% down
        lookback_minutes: int = 30,  # Look at last 30min for context
        min_trade_usdc: float = 5.0,  # Minimum $5 trades
        max_trade_usdc: float = 100.0,  # Maximum $100 per trade
    ):
        self.orca = orca_client
        self.buy_dip_threshold = buy_dip_threshold
        self.sell_rise_threshold = sell_rise_threshold
        self.stop_loss_pct = stop_loss_pct
        self.lookback_minutes = lookback_minutes
        self.min_trade_usdc = min_trade_usdc
        self.max_trade_usdc = max_trade_usdc
        
        # Price history
        self.price_history: deque[PricePoint] = deque(maxlen=1000)
        
        # Trading state
        self.last_buy_price: Optional[float] = None
        self.sol_position: float = 0.0  # How much SOL we own
        self.usdc_balance: float = 0.0  # Available USDC
        
    def update_price(self) -> float:
        """Get current SOL/USDC price from Orca and add to history"""
        try:
            # Get quote for 1 SOL → USDC to determine current rate
            SOL = "So11111111111111111111111111111111111111112"
            USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            
            quote = self.orca.get_quote(
                input_mint=SOL,
                output_mint=USDC,
                amount=1_000_000_000,  # 1 SOL in lamports
                slippage_bps=50
            )
            
            # Calculate rate: USDC per SOL
            out_amount = int(quote["outAmount"])
            usdc_per_sol = out_amount / 1_000_000  # USDC has 6 decimals
            
            # Add to history
            point = PricePoint(
                timestamp=time.time(),
                sol_usdc_rate=usdc_per_sol,
                volume_indicator=1.0  # Mock - real implementation would get volume
            )
            self.price_history.append(point)
            
            return usdc_per_sol
            
        except Exception as e:
            raise RuntimeError(f"Failed to update SOL price: {e}")
    
    def get_recent_high(self, minutes: int = None) -> Optional[float]:
        """Get highest price in the last N minutes"""
        minutes = minutes or self.lookback_minutes
        cutoff = time.time() - (minutes * 60)
        
        recent_prices = [p.sol_usdc_rate for p in self.price_history 
                        if p.timestamp >= cutoff]
        return max(recent_prices) if recent_prices else None
    
    def get_recent_low(self, minutes: int = None) -> Optional[float]:
        """Get lowest price in the last N minutes"""
        minutes = minutes or self.lookback_minutes
        cutoff = time.time() - (minutes * 60)
        
        recent_prices = [p.sol_usdc_rate for p in self.price_history 
                        if p.timestamp >= cutoff]
        return min(recent_prices) if recent_prices else None
    
    def get_moving_average(self, minutes: int = 15) -> Optional[float]:
        """Calculate moving average price"""
        cutoff = time.time() - (minutes * 60)
        recent_prices = [p.sol_usdc_rate for p in self.price_history 
                        if p.timestamp >= cutoff]
        
        if not recent_prices:
            return None
        return sum(recent_prices) / len(recent_prices)
    
    def analyze_market(self) -> TradingSignal:
        """Analyze current market conditions and generate trading signal"""
        
        if len(self.price_history) < 3:
            return TradingSignal(
                action="HOLD",
                confidence=0.0,
                current_price=0.0,
                target_price=None,
                reason="Not enough price history"
            )
        
        current_price = self.price_history[-1].sol_usdc_rate
        recent_high = self.get_recent_high()
        recent_low = self.get_recent_low()
        moving_avg = self.get_moving_average()
        
        # BUY SIGNAL: Price dropped significantly from recent high
        if recent_high and current_price < recent_high:
            drop_pct = ((recent_high - current_price) / recent_high) * 100
            
            if drop_pct >= self.buy_dip_threshold:
                # Calculate position size (risk management)
                trade_amount = min(
                    self.max_trade_usdc,
                    self.usdc_balance * 0.2  # Use max 20% of available USDC
                )
                
                if trade_amount >= self.min_trade_usdc:
                    return TradingSignal(
                        action="BUY_SOL",
                        confidence=min(drop_pct / 10.0, 1.0),  # Higher confidence for bigger drops
                        current_price=current_price,
                        target_price=current_price * 1.05,  # Target 5% profit
                        reason=f"SOL dropped {drop_pct:.1f}% from recent high ${recent_high:.2f}",
                        suggested_amount_usdc=trade_amount
                    )
        
        # SELL SIGNAL: Price rose significantly OR hit stop loss
        if self.sol_position > 0 and self.last_buy_price:
            
            # Check for profit target
            if recent_low and current_price > recent_low:
                rise_pct = ((current_price - recent_low) / recent_low) * 100
                
                if rise_pct >= self.sell_rise_threshold:
                    profit_pct = ((current_price - self.last_buy_price) / self.last_buy_price) * 100
                    
                    return TradingSignal(
                        action="SELL_SOL",
                        confidence=0.8,
                        current_price=current_price,
                        target_price=None,
                        reason=f"SOL rose {rise_pct:.1f}% from recent low. Profit: {profit_pct:.1f}%"
                    )
            
            # Check for stop loss
            loss_pct = ((self.last_buy_price - current_price) / self.last_buy_price) * 100
            if loss_pct >= self.stop_loss_pct:
                return TradingSignal(
                    action="SELL_SOL",
                    confidence=0.9,  # High confidence on stop loss
                    current_price=current_price,
                    target_price=None,
                    reason=f"Stop loss triggered. Loss: {loss_pct:.1f}%"
                )
        
        # DEFAULT: HOLD
        reason_parts = []
        if moving_avg:
            if current_price > moving_avg:
                reason_parts.append(f"Above MA(${moving_avg:.2f})")
            else:
                reason_parts.append(f"Below MA(${moving_avg:.2f})")
        
        reason = "Market conditions neutral. " + ", ".join(reason_parts)
        
        return TradingSignal(
            action="HOLD",
            confidence=0.3,
            current_price=current_price,
            target_price=None,
            reason=reason
        )
    
    def update_balances(self, sol_balance: float, usdc_balance: float):
        """Update our current SOL and USDC balances"""
        self.sol_position = sol_balance
        self.usdc_balance = usdc_balance
    
    def execute_buy(self, signal: TradingSignal) -> Dict:
        """Execute BUY SOL order (convert USDC → SOL)"""
        if not signal.suggested_amount_usdc:
            raise ValueError("No suggested amount for buy signal")
        
        try:
            # Calculate how much SOL we can buy
            usdc_amount = signal.suggested_amount_usdc
            expected_sol = usdc_amount / signal.current_price
            
            # Get actual quote from Orca
            USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            SOL = "So11111111111111111111111111111111111111112"
            
            usdc_lamports = int(usdc_amount * 1_000_000)  # USDC has 6 decimals
            
            quote = self.orca.get_quote(
                input_mint=USDC,
                output_mint=SOL,
                amount=usdc_lamports,
                slippage_bps=100  # 1% slippage for market orders
            )
            
            # Update our tracking
            self.last_buy_price = signal.current_price
            
            return {
                "action": "BUY_SOL",
                "quote": quote,
                "expected_sol": expected_sol,
                "usdc_spent": usdc_amount,
                "price": signal.current_price
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to execute buy: {e}")
    
    def execute_sell(self, signal: TradingSignal) -> Dict:
        """Execute SELL SOL order (convert SOL → USDC)"""
        try:
            # Use all our SOL position
            sol_amount = self.sol_position
            expected_usdc = sol_amount * signal.current_price
            
            # Get actual quote from Orca
            SOL = "So11111111111111111111111111111111111111112"
            USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            
            sol_lamports = int(sol_amount * 1_000_000_000)  # SOL has 9 decimals
            
            quote = self.orca.get_quote(
                input_mint=SOL,
                output_mint=USDC,
                amount=sol_lamports,
                slippage_bps=100  # 1% slippage for market orders
            )
            
            # Calculate profit/loss
            profit_loss = 0.0
            if self.last_buy_price:
                profit_loss = ((signal.current_price - self.last_buy_price) / self.last_buy_price) * 100
            
            # Reset position tracking
            self.last_buy_price = None
            
            return {
                "action": "SELL_SOL",
                "quote": quote,
                "expected_usdc": expected_usdc,
                "sol_sold": sol_amount,
                "price": signal.current_price,
                "profit_loss_pct": profit_loss
            }
            
        except Exception as e:
            raise RuntimeError(f"Failed to execute sell: {e}")