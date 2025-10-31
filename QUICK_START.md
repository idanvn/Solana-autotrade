# QUICK_START.md

15-minute setup to run a dry-run quote on Jupiter and prepare your Solana trading bot.

## Prerequisites

- Python 3.10 or 3.11
- An RPC endpoint (e.g., Helius, Triton, QuickNode). Mainnet recommended.
- A Solana wallet private key exported as a 64-int JSON array (Phantom format).

## 1) Create environment files

Copy and edit `.env` from the example:

```powershell
Copy-Item .env.example .env
```

Open `.env` and set:

- `RPC_URL`: your HTTPS RPC endpoint
- `WALLET_PRIVATE_KEY_JSON`: the 64-int JSON array as a single line

## 2) Install dependencies

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Run a dry-run quote

This will fetch a SOL→USDC quote and print expected output amount, no signing.

```powershell
python .\scripts\dry_run.py
```

Expected output includes a route with `outAmount` and estimated price impact.

## 4) Next steps

- Read `CRITICAL_FIXES_2025.md` to understand imports and VersionedTransaction usage.
- Explore `backend/core/wallet_manager.py` and `backend/core/jupiter_client.py`.
- Configure `config.json` risk and trade settings.
- Add your strategy logic to call Jupiter swap once your signals fire.

If you hit issues, check `README.md` → Troubleshooting.
