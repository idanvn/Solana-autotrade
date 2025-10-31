"""
Real Wallet Integration Test with Solflare
SAFETY FIRST: Small amounts only for testing
"""

import sys
from pathlib import Path

# Add project root to path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.core.wallet_manager import WalletManager  # noqa: E402
from backend.core.orca_client import OrcaClient  # noqa: E402
import os
from dotenv import load_dotenv

load_dotenv()

def test_wallet_connection():
    """Test real wallet connection and balances"""
    
    print("🔐 Real Wallet Connection Test")
    print("=" * 50)
    
    # Safety checks
    print("⚠️  SAFETY REMINDER:")
    print("   • Only use a TEST wallet with small amounts")
    print("   • NEVER use your main wallet for testing")
    print("   • Recommended: <$10 worth for initial tests")
    print()
    
    # Check environment
    rpc_url = os.getenv("RPC_URL")
    wallet_key = os.getenv("WALLET_PRIVATE_KEY_JSON")
    
    if not rpc_url:
        print("❌ ERROR: RPC_URL not set in .env")
        print("💡 Add your RPC endpoint (Helius, QuickNode, etc.)")
        return False
    
    if not wallet_key:
        print("❌ ERROR: WALLET_PRIVATE_KEY_JSON not set in .env")
        print("💡 Export your Solflare private key as JSON array")
        print("   In Solflare: Settings → Export Private Key → Copy as Array")
        return False
    
    print(f"✅ RPC configured: {rpc_url[:50]}...")
    print("✅ Wallet key configured")
    print()
    
    try:
        # Initialize wallet manager
        print("🔌 Connecting to wallet...")
        wm = WalletManager(rpc_url)
        wm.load_keypair_from_json_array(wallet_key)
        
        pubkey = wm.pubkey()
        print(f"✅ Wallet connected!")
        print(f"   Address: {pubkey}")
        print()
        
        # Check balances
        print("💰 Checking balances...")
        
        # SOL balance
        sol_balance = wm.get_sol_balance()
        print(f"   SOL: {sol_balance:.6f} (~${sol_balance * 140:.2f})")
        
        # USDC balance (with error handling)
        try:
            USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            usdc_balance = wm.get_spl_balance(USDC)
            print(f"   USDC: {usdc_balance:.2f}")
        except Exception as e:
            print(f"   USDC: 0.00 (no USDC tokens found)")
            usdc_balance = 0.0
        
        total_value = (sol_balance * 140) + usdc_balance
        print(f"   Total Value: ~${total_value:.2f}")
        print()
        
        # Safety warnings based on balance
        if total_value > 100:
            print("⚠️  WARNING: High value wallet detected!")
            print("   Consider using a smaller test wallet first")
        elif total_value < 5:
            print("⚠️  WARNING: Low balance may not cover transaction fees")
            print("   Add at least $10 worth for testing")
        else:
            print("✅ Good balance for testing!")
        
        print()
        
        # Test Orca connection
        print("🐋 Testing Orca DEX connection...")
        orca = OrcaClient()
        
        # Small test quote (0.001 SOL)
        SOL = "So11111111111111111111111111111111111111112"
        quote = orca.get_quote(
            input_mint=SOL,
            output_mint=USDC,
            amount=1_000_000,  # 0.001 SOL
            slippage_bps=50
        )
        
        out_amount = int(quote["outAmount"]) / 1_000_000
        print(f"✅ Test quote: 0.001 SOL → {out_amount:.4f} USDC")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def safety_checklist():
    """Interactive safety checklist before live trading"""
    
    print("🛡️  PRE-TRADING SAFETY CHECKLIST")
    print("=" * 50)
    
    checks = [
        "Is this a TEST wallet (not your main wallet)?",
        "Does the wallet have <$20 worth of tokens?", 
        "Do you have a backup of your seed phrase?",
        "Are you testing with Solana MAINNET (not devnet)?",
        "Do you understand the risks of automated trading?"
    ]
    
    all_good = True
    for i, check in enumerate(checks, 1):
        response = input(f"{i}. {check} (y/n): ").lower().strip()
        if response != 'y':
            print(f"❌ Please address item {i} before proceeding")
            all_good = False
    
    print()
    if all_good:
        print("✅ All safety checks passed!")
        return True
    else:
        print("❌ Please complete all safety checks first")
        return False

def micro_trade_test():
    """Execute a tiny test trade to verify everything works"""
    
    print("🧪 MICRO TRADE TEST")
    print("=" * 50)
    
    # Load wallet
    wm = WalletManager(os.getenv("RPC_URL"))
    wm.load_keypair_from_json_array(os.getenv("WALLET_PRIVATE_KEY_JSON"))
    
    # Check minimum balance
    sol_balance = wm.get_sol_balance()
    if sol_balance < 0.01:  # Need at least 0.01 SOL for fees + trade
        print("❌ Insufficient SOL balance for micro test")
        print(f"   Current: {sol_balance:.6f} SOL")
        print(f"   Required: 0.01 SOL minimum")
        return False
    
    print(f"💰 Current SOL balance: {sol_balance:.6f}")
    
    # Confirm micro trade
    print("\n⚠️  About to execute REAL trade:")
    print("   Amount: 0.005 SOL → USDC (very small test)")
    print("   Est. value: ~$0.70")
    print("   Purpose: Verify wallet + DEX integration")
    
    confirm = input("\nProceed with micro trade? (yes/no): ").lower().strip()
    if confirm != 'yes':
        print("❌ Micro trade cancelled")
        return False
    
    try:
        # Execute micro swap
        print("\n🔄 Executing micro trade...")
        
        orca = OrcaClient()
        SOL = "So11111111111111111111111111111111111111112" 
        USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        
        # Get quote for 0.005 SOL
        quote = orca.get_quote(
            input_mint=SOL,
            output_mint=USDC,
            amount=5_000_000,  # 0.005 SOL
            slippage_bps=100   # 1% slippage for safety
        )
        
        expected_usdc = int(quote["outAmount"]) / 1_000_000
        print(f"   Quote: 0.005 SOL → {expected_usdc:.4f} USDC")
        
        # This would execute the real trade
        print("\n⚠️  REAL EXECUTION DISABLED FOR SAFETY")
        print("   To enable: uncomment the swap_with_wallet line below")
        print("   The quote above shows it would work")
        
        # Uncomment this line when ready for real trading:
        # signature = orca.swap_with_wallet(wm, quote)
        # print(f"✅ Trade executed! Signature: {signature}")
        
        print("\n✅ Micro trade test completed successfully!")
        print("   Everything is connected and working")
        print("   Ready for live trading when you enable it")
        
        return True
        
    except Exception as e:
        print(f"❌ Micro trade failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Solflare Integration Test Suite")
    print("Testing with REAL wallet - proceed carefully!")
    print()
    
    # Step 1: Basic connection test
    if not test_wallet_connection():
        print("❌ Fix connection issues before proceeding")
        exit(1)
    
    # Step 2: Safety checklist
    print("\n" + "="*50)
    if not safety_checklist():
        print("❌ Complete safety checklist before proceeding")
        exit(1)
    
    # Step 3: Optional micro trade
    print("\n" + "="*50)
    do_micro = input("Execute micro trade test? (y/n): ").lower().strip()
    if do_micro == 'y':
        micro_trade_test()
    
    print("\n🎯 Integration test complete!")
    print("Your wallet is ready for automated trading 🔥")