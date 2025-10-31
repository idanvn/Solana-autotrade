"""
Production-ready dry run using Orca instead of Jupiter
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

print("🐋 Orca DEX - Production Dry Run")
print("Requesting quote for 0.001 SOL -> USDC...")

try:
    orca = OrcaClient()
    
    # Get quote (same interface as Jupiter)
    quote = orca.get_quote(
        input_mint=SOL,
        output_mint=USDC,
        amount=1_000_000,  # 0.001 SOL in lamports
        slippage_bps=50
    )
    
    # Display in same format as original dry_run.py
    out_amount = int(quote["outAmount"])
    print("Best outAmount (raw):", out_amount)
    print("Sample complete. You can now use OrcaClient to build swap transactions.")
    
    # Additional info
    usdc_amount = out_amount / 1_000_000
    print(f"Expected: {usdc_amount:.6f} USDC for 0.001 SOL")
    print(f"Pool: {quote['poolAddress']}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()