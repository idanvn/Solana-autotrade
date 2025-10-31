import os
import socket
import requests
from dotenv import load_dotenv

# Force use of specific DNS servers for this session
# This bypasses the faulty local DNS server
def force_dns_resolution():
    """Override default DNS to use public servers"""
    original_getaddrinfo = socket.getaddrinfo
    
    def custom_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
        # For Jupiter API, resolve using known IP addresses
        if 'jup.ag' in host:
            # Use Cloudflare DNS to resolve
            import subprocess
            try:
                result = subprocess.run(['nslookup', host, '1.1.1.1'], 
                                      capture_output=True, text=True, timeout=10)
                if 'Address:' in result.stdout:
                    # Extract IP from nslookup output
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'Address:' in line and '1.1.1.1' not in line:
                            ip = line.split('Address:')[-1].strip()
                            if ip:
                                return [(family, type, proto, '', (ip, port))]
            except Exception:
                pass
        return original_getaddrinfo(host, port, family, type, proto, flags)
    
    socket.getaddrinfo = custom_getaddrinfo

load_dotenv()

# Apply DNS fix
force_dns_resolution()

RPC_URL = os.getenv("RPC_URL")
BASE_URL = os.getenv("JUPITER_BASE_URL", "https://quote-api.jup.ag")

SOL = "So11111111111111111111111111111111111111112"
USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"

params = {
    "inputMint": SOL,
    "outputMint": USDC,
    "amount": str(1_000_000),  # 0.001 SOL
    "slippageBps": "50"
}

print("🔧 Using DNS bypass...")
print("Requesting quote from Jupiter...")

try:
    r = requests.get(f"{BASE_URL}/v6/quote", params=params, timeout=20)
    r.raise_for_status()
    quote = r.json()

    if "outAmount" in quote:
        out_amount = int(quote["outAmount"])
        usdc_amount = out_amount / 1_000_000  # USDC has 6 decimals
        print(f"✅ Success! Best quote: {usdc_amount:.6f} USDC for 0.001 SOL")
        print(f"   Rate: ~{usdc_amount * 1000:.2f} USDC per SOL")
    else:
        print("❌ Unexpected response format")
        print("Response:", quote)
    
except requests.exceptions.RequestException as e:
    print(f"❌ Network error: {e}")
    print("\n💡 Alternative: Try the offline mock version:")
    print("   python .\\scripts\\dry_run_offline.py")