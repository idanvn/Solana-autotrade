# GITHUB_COPILOT_INSTRUCTIONS.md

Use this document to co-drive development with GitHub Copilot. It lists key modules, function contracts, and example prompts.

## Modules and contracts

### backend/core/wallet_manager.py

Class: `WalletManager`

- init(rpc_url: str, commitment: str = "confirmed")
  - Creates a sync RPC client tied to `rpc_url`.
- load_keypair_from_json_array(json_array_str: str) -> None
  - Parses a 64-int JSON array string and initializes `self.keypair`.
- pubkey() -> str
  - Returns base58 string of the wallet public key.
- get_sol_balance() -> float
  - Returns SOL balance in SOL units.
- get_spl_balance(mint: str) -> float
  - Returns token balance in UI units using token decimals (best effort).
- sign_and_send_v0_txn(serialized_txn_b64: str) -> str
  - Deserializes, signs with wallet, submits to RPC. Returns tx signature.
- close() -> None

Edge cases:
- Invalid JSON key → raise ValueError.
- Empty balance → return 0.0.
- RPC errors → raise RuntimeError with provider message.

### backend/core/jupiter_client.py

Class: `JupiterClient`

- init(base_url: str = "https://quote-api.jup.ag")
- get_quote(input_mint: str, output_mint: str, amount: int, slippage_bps: int = 50, only_direct_routes: bool = False) -> dict
- build_swap_transaction(quote: dict, user_pubkey: str, wrap_unwrap_sol: bool = True, prioritization_fee_lamports: int | None = None) -> str
  - Returns base64 serialized transaction.
- swap_with_wallet(wallet: WalletManager, quote: dict, **kwargs) -> str
  - Builds swap, signs and sends using `wallet`.

Edge cases:
- Bad mint or amount → Jupiter returns error JSON. Propagate with context.
- Amount units: pass smallest units always.

### backend/core/price_monitor.py

Class: `PriceMonitor`

- add_point(ts: float, price: float, volume: float) -> None
- volume_spike(multiplier: float = 4.0, window: int = 20) -> bool
- momentum(min_change_pct: float = 3.0, lookback: int = 10) -> bool
- signal() -> dict
  - Returns `{ "volume_spike": bool, "momentum": bool }`

Notes:
- Stateless market data ingestion; you wire it to your source of candles/trades.

## Example end-to-end (pseudocode)

```python
from backend.core.wallet_manager import WalletManager
from backend.core.jupiter_client import JupiterClient
from dotenv import load_dotenv
import os, json

load_dotenv()
wm = WalletManager(os.getenv("RPC_URL"))
wm.load_keypair_from_json_array(os.getenv("WALLET_PRIVATE_KEY_JSON"))

jup = JupiterClient()
quote = jup.get_quote(
  input_mint="So11111111111111111111111111111111111111112",
  output_mint="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  amount=1000000,  # 0.001 SOL
  slippage_bps=50
)
sig = jup.swap_with_wallet(wm, quote)
print("Sent:", sig)
```

## Good Copilot prompts

- "Generate a retry wrapper with exponential backoff for RPC calls that returns the first successful result or raises after 3 attempts."
- "Add a method to JupiterClient to compute the UI out amount using token decimals from the quote response."
- "Write unit tests for PriceMonitor.momentum and volume_spike (happy path + edge cases)."

## Safety checks to add

- Pre-trade balance check ensures sufficient SOL and token balances + fee buffer.
- Post-trade signature confirmation with `get_signature_statuses`.
- Slippage guard comparing executed vs expected out amount.

## API references

- Jupiter Station: https://station.jup.ag/
- solana-py: https://michaelhly.github.io/solana-py/
- solders: https://crates.io/crates/solders (Python bindings are documented within solana-py releases)
