from __future__ import annotations

import json
from typing import Any, Dict, Optional

import requests


class JupiterClient:
    """Minimal Jupiter v6 REST client.

    Docs: https://station.jup.ag/
    """

    def __init__(self, base_url: str = "https://quote-api.jup.ag", timeout: int = 20) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # --- Quote ---
    def get_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
        only_direct_routes: bool = False,
    ) -> Dict[str, Any]:
        """Fetch a quote. `amount` is in the token's smallest unit.

        Returns the raw Jupiter v6 quote JSON.
        """
        params = {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": str(amount),
            "slippageBps": str(slippage_bps),
        }
        if only_direct_routes:
            params["onlyDirectRoutes"] = "true"

        url = f"{self.base_url}/v6/quote"
        r = requests.get(url, params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # --- Build swap ---
    def build_swap_transaction(
        self,
        quote: Dict[str, Any],
        user_pubkey: str,
        wrap_unwrap_sol: bool = True,
        prioritization_fee_lamports: Optional[int] = None,
    ) -> str:
        """Build a swap transaction. Returns base64-encoded serialized transaction."""
        url = f"{self.base_url}/v6/swap"
        body: Dict[str, Any] = {
            "quoteResponse": quote,
            "userPublicKey": user_pubkey,
            "wrapUnwrapSOL": wrap_unwrap_sol,
        }
        if prioritization_fee_lamports is not None:
            body["prioritizationFeeLamports"] = prioritization_fee_lamports

        r = requests.post(url, json=body, timeout=self.timeout)
        r.raise_for_status()
        data = r.json()
        if "swapTransaction" not in data:
            raise RuntimeError(f"Unexpected swap response: {json.dumps(data)[:500]}")
        return data["swapTransaction"]

    # --- Convenience: build + sign + send with wallet ---
    def swap_with_wallet(self, wallet, quote: Dict[str, Any], **kwargs) -> str:
        """Build the swap with Jupiter, then sign and send with the given wallet.

        `wallet` is expected to implement:
          - `pubkey() -> str`
          - `sign_and_send_v0_txn(serialized_txn_b64: str) -> str`
        """
        serialized_b64 = self.build_swap_transaction(quote, user_pubkey=wallet.pubkey(), **kwargs)
        return wallet.sign_and_send_v0_txn(serialized_b64)
