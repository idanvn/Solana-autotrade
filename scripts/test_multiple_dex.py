"""
Alternative DEX test using Orca API
Orca is another major Solana DEX with simpler API structure
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Orca API endpoint - different domain to test connectivity
ORCA_API = "https://api.orca.so"

print("🐋 Testing Orca DEX API instead of Jupiter...")

# Test 1: Check basic connectivity to Orca
try:
    print("Step 1: Testing basic connectivity to api.orca.so...")
    health_response = requests.get(f"{ORCA_API}/v1/whirlpool/list", timeout=10)
    print(f"✅ Orca API accessible! Status: {health_response.status_code}")
    
    if health_response.status_code == 200:
        data = health_response.json()
        pools_count = len(data.get("whirlpools", []))
        print(f"   Found {pools_count} liquidity pools")
        
        # Look for SOL/USDC pools
        sol_usdc_pools = []
        for pool in data.get("whirlpools", [])[:50]:  # Check first 50
            token_a = pool.get("tokenA", {}).get("mint", "")
            token_b = pool.get("tokenB", {}).get("mint", "")
            
            SOL = "So11111111111111111111111111111111111111112"
            USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            
            if (token_a == SOL and token_b == USDC) or (token_a == USDC and token_b == SOL):
                sol_usdc_pools.append({
                    "address": pool.get("address"),
                    "liquidity": pool.get("liquidity", "0")
                })
        
        if sol_usdc_pools:
            print(f"✅ Found {len(sol_usdc_pools)} SOL/USDC pools on Orca:")
            for pool in sol_usdc_pools[:3]:  # Show top 3
                print(f"   Pool: {pool['address'][:8]}...{pool['address'][-8:]}")
        else:
            print("ℹ️  No SOL/USDC pools found in first 50 results")
    
except requests.exceptions.RequestException as e:
    print(f"❌ Orca API also failed: {e}")
    print("\n🔧 This confirms it's a general DNS/network issue")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")

print("\n" + "="*60)
print("📊 CONCLUSION:")
print("="*60)

# Test with multiple APIs to isolate the problem
test_apis = [
    ("Jupiter", "https://quote-api.jup.ag"),
    ("Orca", "https://api.orca.so"),
    ("Raydium", "https://api-v3.raydium.io"),
    ("Coinbase (external)", "https://api.coinbase.com"),
]

working_apis = 0
for name, url in test_apis:
    try:
        resp = requests.get(url, timeout=5)
        print(f"✅ {name}: WORKING (status {resp.status_code})")
        working_apis += 1
    except Exception as e:
        print(f"❌ {name}: FAILED ({str(e)[:50]}...)")

if working_apis == 0:
    print("\n🚨 ALL APIs failed - this is a local network/DNS issue")
    print("💡 Solutions:")
    print("   1. Change DNS servers (most likely fix)")
    print("   2. Check firewall/antivirus settings") 
    print("   3. Try VPN or mobile hotspot")
    print("   4. Use offline development with mock data")
elif working_apis < len(test_apis):
    print(f"\n⚠️  Only {working_apis}/{len(test_apis)} APIs working")
    print("💡 Some crypto-related domains may be blocked")
else:
    print(f"\n✅ All APIs working - the original issue was temporary")