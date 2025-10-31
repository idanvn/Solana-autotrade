import os
import requests
from dotenv import load_dotenv

load_dotenv()

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

print("Requesting quote ...")
r = requests.get(f"{BASE_URL}/v6/quote", params=params, timeout=20)
r.raise_for_status()
quote = r.json()

if "outAmount" in quote:
    print("Best outAmount (raw):", quote["outAmount"])  # v6 sometimes returns flat structure
else:
    route = quote.get("routePlan", [{}])[0]
    out = route.get("swapInfo", {}).get("outAmount")
    print("Route outAmount (first leg):", out)

print("Sample complete. You can now use JupiterClient to build the swap tx.")
