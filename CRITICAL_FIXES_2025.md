# CRITICAL_FIXES_2025.md

Read this first. These are the breaking changes and working patterns verified for 2025 with solana-py 0.36.x, solders 0.26.x, and Jupiter v6 APIs.

## ✅ Library versions (pin exactly)

- solana==0.36.9
- solders==0.26.0
- requests==2.32.3
- python-dotenv==1.0.1
- websockets==12.0 (optional; only if you add WS streams)
- cryptography==43.0.1 (optional; only if you enable local key encryption)

Pinning is required to avoid subtle API/typing breakages.

## 🔁 Imports that changed

- Public keys and keypairs come from solders:
  - `from solders.pubkey import Pubkey`
  - `from solders.keypair import Keypair`
- RPC client stays in solana:
  - `from solana.rpc.async_api import AsyncClient`
  - or sync: `from solana.rpc.api import Client`
- Versioned transactions are handled via solders:
  - `from solders.transaction import VersionedTransaction`
- Do not import `PublicKey` from `solana.publickey` in new code; prefer `solders.Pubkey`.

## 🧩 VersionedTransaction handling (Jupiter v6)

Jupiter v6 /swap endpoint returns a base64-encoded versioned transaction that must be signed by the user's wallet and sent to the cluster.

- Decode and parse bytes:
  - `vtx_in = VersionedTransaction.from_bytes(base64.b64decode(swapTxnB64))`
- Sign (payer must match `userPublicKey` you passed to Jupiter) by reconstructing with your signer:
  - `vtx_signed = VersionedTransaction(vtx_in.message, [keypair])`
- Send raw bytes to RPC using `send_raw_transaction`:
  - `client.send_raw_transaction(bytes(vtx_signed))`

Important notes:
- Use the same RPC URL for both quote/swap and submission to avoid cluster mismatches.
- On mainnet, set a sane commitment like `confirmed`.
- Keep `wrapUnwrapSOL=True` when swapping SOL<->SPL.

## 🌐 Jupiter v6 endpoints (2025)

- Quote (GET): `https://quote-api.jup.ag/v6/quote`
  - Required params: `inputMint`, `outputMint`, `amount` (in smallest units), `slippageBps` (e.g., 50 for 0.5%)
- Swap (POST): `https://quote-api.jup.ag/v6/swap`
  - JSON body:
    ```json
    {
      "quoteResponse": { /* quote object from v6/quote */ },
      "userPublicKey": "<base58 pubkey>",
      "wrapUnwrapSOL": true,
      "prioritizationFeeLamports": null
    }
    ```
  - Response: `{ "swapTransaction": "<base64>" , ...}`

Docs: https://station.jup.ag/

## 🔐 Wallet input format (recommended)

Provide `WALLET_PRIVATE_KEY_JSON` in `.env` as a JSON array of 64 integers (Phantom export style). Example:

```
WALLET_PRIVATE_KEY_JSON=[12,34,56, ... 64 numbers ...]
```

The code will parse that into `solders.Keypair` safely. Seed phrases are NOT handled directly in this starter.

## 🧪 Minimal working example (sync)

```python
import os, json, base64, asyncio
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.transaction import VersionedTransaction
import requests

load_dotenv()
rpc = os.getenv("RPC_URL")
kp_json = os.getenv("WALLET_PRIVATE_KEY_JSON")
secret = bytes(json.loads(kp_json))
kp = Keypair.from_bytes(secret)
client = Client(rpc)

# 1) Get quote
params = {
    "inputMint": "So11111111111111111111111111111111111111112",  # SOL
    "outputMint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",  # USDC
    "amount": str(1000000),  # 0.001 SOL
    "slippageBps": 50
}
qr = requests.get("https://quote-api.jup.ag/v6/quote", params=params, timeout=20)
quote = qr.json()

# 2) Build swap
body = {
    "quoteResponse": quote,
    "userPublicKey": str(kp.pubkey()),
    "wrapUnwrapSOL": True
}
sr = requests.post("https://quote-api.jup.ag/v6/swap", json=body, timeout=20)
swap_tx_b64 = sr.json()["swapTransaction"]

# 3) Sign & send
vtx_in = VersionedTransaction.from_bytes(base64.b64decode(swap_tx_b64))
vtx_signed = VersionedTransaction(vtx_in.message, [kp])
sig = client.send_raw_transaction(bytes(vtx_signed))
print("signature:", sig.value)
```

This pattern matches the code in `backend/core/wallet_manager.py` and `backend/core/jupiter_client.py`.

## 🧯 Common errors fixed

- Import errors for `PublicKey`/`Keypair` → move to `solders`.
- Type mismatch when deserializing Jupiter tx → use `VersionedTransaction.deserialize`.
- Incorrect amount units → always pass amounts in the token's smallest unit.
- Missing `wrapUnwrapSOL` when swapping SOL → set it to True.
- Wrong RPC commitment leading to stuck transactions → use `confirmed` and retry with backoff.

## ✅ Status

All starter files in this repo follow the above conventions and run with the pinned versions.
