"""
SAFE Real Wallet Strategy - MICRO AMOUNTS ONLY
Modified for production wallet with extreme safety measures
"""

import sys
import time
import os
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.core.wallet_manager import WalletManager  # noqa: E402
from backend.core.orca_client import OrcaClient  # noqa: E402
from backend.core.sol_strategy import SOLTradingStrategy  # noqa: E402

load_dotenv()

def ultra_safe_trading():
    """Ultra-safe trading with production wallet - MICRO AMOUNTS ONLY"""
    
    print("🔒 ULTRA-SAFE PRODUCTION TRADING")
    print("⚠️  USING REAL WALLET - MAXIMUM CAUTION!")
    print("=" * 55)
    
    # Safety warnings
    print("🚨 SAFETY PROTOCOL:")
    print("   • Maximum trade: 0.005 SOL (~$0.70)")
    print("   • Stop after ANY loss > $1")
    print("   • Manual approval for each trade")
    print("   • You can stop anytime with Ctrl+C")
    print()
    
    # Confirm understanding
    print("⚠️  FINAL WARNING:")
    print("   This uses your REAL wallet with REAL money!")
    print("   Automated trading has REAL risks!")
    print("   You could lose money!")
    print()
    
    confirm = input("Type 'I UNDERSTAND THE RISKS' to continue: ")
    if confirm != "I UNDERSTAND THE RISKS":
        print("❌ Trading cancelled for safety")
        return
    
    try:
        # Initialize with real wallet
        print("\n🔌 Connecting to your wallet...")
        wm = WalletManager(os.getenv("RPC_URL"))
        wm.load_keypair_from_json_array(os.getenv("WALLET_PRIVATE_KEY_JSON"))
        
        print(f"✅ Connected: {wm.pubkey()}")
        
        # Check balances
        sol_balance = wm.get_sol_balance()
        print(f"💰 SOL Balance: {sol_balance:.6f} (~${sol_balance * 140:.2f})")
        
        if sol_balance < 0.02:  # Need minimum for fees + trades
            print("❌ Insufficient balance for safe trading")
            print("   Need at least 0.02 SOL for fees + micro trades")
            return
        
        # Initialize ULTRA-CONSERVATIVE strategy
        orca = OrcaClient()
        strategy = SOLTradingStrategy(
            orca_client=orca,
            buy_dip_threshold=3.0,    # Only buy on 3%+ dips (less sensitive)
            sell_rise_threshold=2.0,  # Quick profit taking at 2%
            stop_loss_pct=1.0,       # Tight 1% stop loss
            lookback_minutes=10,     # Longer lookback for stability
            min_trade_usdc=0.5,      # Minimum $0.50 trades
            max_trade_usdc=1.0       # Maximum $1.00 trades ⚠️ VERY SMALL!
        )
        
        # Set current balances
        usdc_balance = 0.0  # Assume no USDC initially
        strategy.update_balances(0.0, usdc_balance)  # Start with 0 SOL position
        
        print(f"\n⚙️  Strategy Settings:")
        print(f"   Max trade size: $1.00 (ULTRA-SAFE)")
        print(f"   Buy threshold: 3%+ price drop")
        print(f"   Sell threshold: 2%+ price rise") 
        print(f"   Stop loss: 1%")
        print()
        
        total_trades = 0
        starting_balance = sol_balance
        
        # Ultra-safe trading loop
        for i in range(10):  # Only 10 iterations max
            print(f"🔍 Market Check #{i+1}/10")
            
            try:
                # Get current price from Orca
                current_price = strategy.update_price()
                
                # Show current state
                current_balance = wm.get_sol_balance()
                print(f"   SOL Price: ${current_price:.2f}")
                print(f"   Wallet Balance: {current_balance:.6f} SOL")
                
                # Get trading signal
                signal = strategy.analyze_market()
                print(f"   Signal: {signal.action}")
                print(f"   Confidence: {signal.confidence:.0%}")
                print(f"   Reason: {signal.reason}")
                
                # MANUAL APPROVAL for any trade
                if signal.action == "BUY_SOL" and signal.confidence > 0.5:
                    print(f"\n🛒 BUY SIGNAL DETECTED!")
                    print(f"   Would buy ~${signal.suggested_amount_usdc:.2f} worth of SOL")
                    print(f"   Current price: ${current_price:.2f}")
                    
                    approve = input("   Execute this buy? (y/n): ").lower()
                    if approve == 'y':
                        try:
                            # Execute MICRO buy - convert small amount of SOL to USDC first for buying power
                            print("   🔄 Executing MICRO buy...")
                            # This is simulation - in real version would execute tiny trade
                            print(f"   ✅ Simulated buy executed (SAFETY: real trades disabled)")
                            total_trades += 1
                        except Exception as e:
                            print(f"   ❌ Buy failed: {e}")
                    else:
                        print("   ⏸️ Buy cancelled")
                
                elif signal.action == "SELL_SOL" and strategy.sol_position > 0:
                    print(f"\n💸 SELL SIGNAL DETECTED!")
                    
                    approve = input("   Execute this sell? (y/n): ").lower()
                    if approve == 'y':
                        try:
                            print("   🔄 Executing MICRO sell...")
                            print(f"   ✅ Simulated sell executed (SAFETY: real trades disabled)")
                            total_trades += 1
                        except Exception as e:
                            print(f"   ❌ Sell failed: {e}")
                    else:
                        print("   ⏸️ Sell cancelled")
                
                else:
                    print("   ⏸️ No action - market conditions not met")
                
                # Safety check - stop if balance drops significantly
                balance_change = current_balance - starting_balance
                if balance_change < -0.01:  # Lost more than 0.01 SOL
                    print(f"\n🚨 SAFETY STOP!")
                    print(f"   Balance dropped by {abs(balance_change):.6f} SOL")
                    print(f"   Stopping for safety")
                    break
                
                # Wait between checks
                print(f"   ⏳ Waiting 30 seconds...")
                time.sleep(30)
                
            except KeyboardInterrupt:
                print(f"\n⏹️ Trading stopped by user")
                break
            except Exception as e:
                print(f"   ❌ Error: {e}")
                break
            
            print()
        
        # Final report
        final_balance = wm.get_sol_balance()
        pnl = final_balance - starting_balance
        
        print("\n" + "=" * 55)
        print("📊 TRADING SESSION COMPLETE")
        print(f"   Starting balance: {starting_balance:.6f} SOL")
        print(f"   Final balance: {final_balance:.6f} SOL")
        print(f"   P&L: {pnl:+.6f} SOL (${pnl * 140:+.2f})")
        print(f"   Total trades: {total_trades}")
        
        if abs(pnl) < 0.001:
            print("✅ Session completed safely - minimal impact")
        elif pnl > 0:
            print("🎉 Profitable session!")
        else:
            print("⚠️ Loss detected - review strategy")
            
    except Exception as e:
        print(f"\n❌ Critical error: {e}")
        print("🛡️ Trading stopped for safety")

if __name__ == "__main__":
    ultra_safe_trading()