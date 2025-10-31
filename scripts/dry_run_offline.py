"""
Mock dry-run for offline testing.
Returns a fake quote structure to validate the rest of the pipeline.
"""

import json

# Fake Jupiter v6 quote response (structure from real API)
mock_quote = {
    "inputMint": "So11111111111111111111111111111111111111112",
    "inAmount": "1000000",
    "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "outAmount": "141234",  # ~0.14 USDC for 0.001 SOL (fake rate)
    "otherAmountThreshold": "140822",
    "swapMode": "ExactIn",
    "slippageBps": 50,
    "priceImpactPct": 0.01,
    "routePlan": [
        {
            "swapInfo": {
                "ammKey": "58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2",
                "label": "Raydium",
                "inputMint": "So11111111111111111111111111111111111111112",
                "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                "inAmount": "1000000",
                "outAmount": "141234",
                "feeAmount": "25",
                "feeMint": "So11111111111111111111111111111111111111112"
            },
            "percent": 100
        }
    ]
}

print("🔧 MOCK MODE (offline)")
print("=" * 50)
print(json.dumps(mock_quote, indent=2))
print("=" * 50)
print(f"Input: {int(mock_quote['inAmount']) / 1_000_000_000:.6f} SOL")
print(f"Expected output: {int(mock_quote['outAmount']) / 1_000_000:.6f} USDC")
print(f"Route: {mock_quote['routePlan'][0]['swapInfo']['label']}")
print("\n✅ Mock quote ready. When network is available, run dry_run.py instead.")
