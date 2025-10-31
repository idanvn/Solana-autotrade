"""
Test the new Orca client with real SOL->USDC quote
"""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.core.orca_client import OrcaClient  # noqa: E402

SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

print("🐋 Testing Orca DEX integration...")
print("=" * 50)

try:
    # Initialize Orca client
    orca = OrcaClient()
    
    # Test 1: Find SOL/USDC pool
    print("Step 1: Finding best SOL/USDC pool...")
    pool = orca.find_best_pool(SOL, USDC)
    
    if pool:
        print(f"✅ Found pool: {pool['address']}")
        print(f"   Liquidity: {pool.get('liquidity', 'N/A')}")
        print(f"   Token A: {pool['tokenA']['mint'][:8]}... ({pool['tokenA']['decimals']} decimals)")
        print(f"   Token B: {pool['tokenB']['mint'][:8]}... ({pool['tokenB']['decimals']} decimals)")
    else:
        print("❌ No SOL/USDC pool found")
        exit(1)
    
    # Test 2: Get quote for 0.001 SOL -> USDC
    print("\nStep 2: Getting quote for 0.001 SOL -> USDC...")
    amount_lamports = 1_000_000  # 0.001 SOL
    
    quote = orca.get_quote(
        input_mint=SOL,
        output_mint=USDC, 
        amount=amount_lamports,
        slippage_bps=50  # 0.5% slippage
    )
    
    # Display results
    input_sol = int(quote["inAmount"]) / 1_000_000_000
    output_usdc = int(quote["outAmount"]) / 1_000_000
    rate = output_usdc / input_sol if input_sol > 0 else 0
    
    print(f"✅ Quote received:")
    print(f"   Input: {input_sol:.6f} SOL") 
    print(f"   Output: {output_usdc:.6f} USDC")
    print(f"   Rate: ~${rate:.2f} per SOL")
    print(f"   DEX: {quote['dex']}")
    print(f"   Pool: {quote['poolAddress'][:8]}...")
    print(f"   Slippage: {quote['slippageBps']/100:.1f}%")
    
    # Test 3: Simulate swap (mock)
    print("\nStep 3: Simulating swap transaction...")
    mock_sig = orca.swap_with_wallet(None, quote)
    print(f"   Mock signature: {mock_sig}")
    
    print("\n" + "=" * 50)
    print("✅ Orca integration successful!")
    print("💡 Next steps:")
    print("   - Integrate with actual Orca SDK for real swaps")
    print("   - Add proper transaction building")
    print("   - Connect with wallet manager for signing")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()