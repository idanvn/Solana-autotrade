# SETUP_GUIDE.md

This guide explains the project structure, configuration files, and how each piece fits together.

## Folder structure

```
.
├─ backend
│  └─ core
│     ├─ wallet_manager.py      # Wallet load, balances, sign, send
│     ├─ jupiter_client.py      # Quote + swap via Jupiter v6
│     └─ price_monitor.py       # Signal scaffolding (volume/momentum)
├─ scripts
│  └─ dry_run.py                # SOL→USDC quote test
├─ .env.example                 # Copy to .env and fill
├─ config.json                  # Basic runtime config
├─ requirements.txt             # Pinned deps
├─ CRITICAL_FIXES_2025.md       # Breaking changes & fixes
├─ QUICK_START.md               # 15-minute setup
├─ README.md                    # Overview
└─ GITHUB_COPILOT_INSTRUCTIONS.md
```

## Configuration files

- `.env`: not committed. Holds secrets and RPC URL.
  - `RPC_URL`: HTTPS Solana RPC endpoint
  - `WALLET_PRIVATE_KEY_JSON`: 64-int json array string
  - `JUPITER_BASE_URL`: default `https://quote-api.jup.ag`
- `config.json`:
  - `slippage_bps`: default 50 (0.5%)
  - `risk`: position sizing and daily loss cap
  - `tokens`: common mint addresses

## Runtime expectations

- Python 3.10/3.11 virtualenv, dependencies from `requirements.txt`.
- Network access to Jupiter APIs and your RPC provider.
- Sufficient SOL balance for fees.

## Extending

- Add your strategy loop to poll quotes, build swaps, and submit.
- Integrate a scheduler and persistent storage for trades.
- Add retries, priority fees, and rate limiting.

See `GITHUB_COPILOT_INSTRUCTIONS.md` for detailed function signatures and extension points.
