"""
Test REAL price Orca client vs old mock client
"""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.core.orca_client import OrcaClient  # noqa: E402 (old mock)
from backend.core.real_price_orca_client import RealPriceOrcaClient  # noqa: E402 (new real)

SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

def test_price_comparison():
    """Compare old mock prices vs real market prices"""
    
    print("💰 SOL Price Comparison: Mock vs Real")
    print("=" * 55)
    
    # Test amount: 1 SOL
    amount_lamports = 1_000_000_000  # 1 SOL
    
    print("🧪 Testing 1 SOL → USDC conversion:")
    print()
    
    # Test 1: Old mock client
    print("📊 OLD CLIENT (Mock Prices):")
    try:
        old_client = OrcaClient()
        old_quote = old_client.get_quote(SOL, USDC, amount_lamports, 50)
        old_usdc = int(old_quote["outAmount"]) / 1_000_000
        old_rate = old_usdc / 1.0  # Rate per SOL
        
        print(f"   Input: 1.000000 SOL")
        print(f"   Output: {old_usdc:.2f} USDC") 
        print(f"   Implied SOL price: ${old_rate:.2f}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        old_rate = 0
    
    print()
    
    # Test 2: New real price client  
    print("🎯 NEW CLIENT (Real Market Prices):")
    try:
        new_client = RealPriceOrcaClient()
        new_quote = new_client.get_quote(SOL, USDC, amount_lamports, 50)
        new_usdc = int(new_quote["outAmount"]) / 1_000_000
        new_rate = new_usdc / 1.0  # Rate per SOL
        real_price = new_quote.get("realSolPrice", "Unknown")
        
        print(f"   Input: 1.000000 SOL")
        print(f"   Output: {new_usdc:.2f} USDC")
        print(f"   Market SOL price: ${real_price:.2f}")
        print(f"   Quote rate: ${new_rate:.2f}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        new_rate = 0
    
    print()
    print("=" * 55)
    
    # Analysis
    if old_rate > 0 and new_rate > 0:
        difference = new_rate - old_rate
        error_pct = (difference / new_rate) * 100
        
        print("📈 ANALYSIS:")
        print(f"   Old mock rate: ${old_rate:.2f}")
        print(f"   New real rate: ${new_rate:.2f}")
        print(f"   Difference: ${difference:+.2f} ({error_pct:+.1f}%)")
        
        if abs(error_pct) > 10:
            print("🚨 CRITICAL ERROR: >10% price difference!")
            print("   Using old client could cause major losses!")
        elif abs(error_pct) > 5:
            print("⚠️ WARNING: >5% price difference")
            print("   Consider using real price client")
        else:
            print("✅ Prices are reasonably close")
    
    print()
    
    # Test small amounts too
    print("🔍 Testing small amount (0.001 SOL):")
    small_amount = 1_000_000  # 0.001 SOL
    
    try:
        small_quote = new_client.get_quote(SOL, USDC, small_amount, 50)
        small_usdc = int(small_quote["outAmount"]) / 1_000_000
        print(f"   0.001 SOL → {small_usdc:.4f} USDC (Real prices)")
    except Exception as e:
        print(f"   ❌ Small quote failed: {e}")

if __name__ == "__main__":
    test_price_comparison()