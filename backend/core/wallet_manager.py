from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Optional

from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solders.transaction import VersionedTransaction


@dataclass
class WalletManager:
    """
    Wallet utilities: load keypair, query balances, sign and submit Jupiter v6 transactions.

    Usage:
        wm = WalletManager(rpc_url)
        wm.load_keypair_from_json_array(os.getenv("WALLET_PRIVATE_KEY_JSON"))
        balance = wm.get_sol_balance()
    """

    rpc_url: str
    commitment: str = "confirmed"

    def __post_init__(self) -> None:
        self._client = Client(self.rpc_url, commitment=self.commitment)
        self._keypair: Optional[Keypair] = None

    # --- Key management ---
    def load_keypair_from_json_array(self, json_array_str: str) -> None:
        """Load a wallet from a JSON array of 64 integers (Phantom export style).

        Raises ValueError on malformed input.
        """
        if not json_array_str:
            raise ValueError("Empty WALLET_PRIVATE_KEY_JSON")
        try:
            arr = json.loads(json_array_str)
            if not isinstance(arr, list) or len(arr) not in (64, 32):
                raise ValueError("Expected JSON array of length 64 (or 32)")
            secret = bytes(arr)
            self._keypair = Keypair.from_bytes(secret)
        except Exception as e:  # noqa: BLE001
            raise ValueError(f"Invalid private key json: {e}") from e

    def has_keypair(self) -> bool:
        return self._keypair is not None

    def pubkey(self) -> str:
        if not self._keypair:
            raise RuntimeError("Keypair not loaded")
        return str(self._keypair.pubkey())

    # --- Balances ---
    def get_sol_balance(self) -> float:
        """Return SOL balance in SOL units."""
        if not self._keypair:
            raise RuntimeError("Keypair not loaded")
        resp = self._client.get_balance(self._keypair.pubkey())
        lamports = resp.value
        return lamports / 1_000_000_000

    def get_spl_balance(self, mint: str) -> float:
        """Return SPL token balance (UI units best-effort).

        Strategy: fetch token accounts by owner + parsed info, sum uiAmount.
        """
        if not self._keypair:
            raise RuntimeError("Keypair not loaded")
        owner = self._keypair.pubkey()
        resp = self._client.get_token_accounts_by_owner_json_parsed(owner, {"mint": mint})
        total = 0.0
        for acc in resp.value:
            try:
                info = acc.account.data.parsed["info"]
                ui_amt = float(info["tokenAmount"]["uiAmount"] or 0)
                total += ui_amt
            except Exception:  # noqa: BLE001
                continue
        return total

    # --- Signing & submission ---
    def sign_and_send_v0_txn(self, serialized_txn_b64: str, skip_preflight: bool = False, max_retries: int | None = None) -> str:
        """Deserialize a base64 versioned transaction, sign with wallet, and submit.

        Returns the transaction signature (base58 string).
        """
        if not self._keypair:
            raise RuntimeError("Keypair not loaded")
        try:
            raw = base64.b64decode(serialized_txn_b64)
            vtx_in = VersionedTransaction.from_bytes(raw)
            # Recreate a signed transaction using the original message and our signer
            vtx_signed = VersionedTransaction(vtx_in.message, [self._keypair])
            opts = TxOpts(skip_preflight=skip_preflight, max_retries=max_retries)
            sig = self._client.send_raw_transaction(bytes(vtx_signed), opts=opts)
            return sig.value
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"send transaction failed: {e}") from e

    def close(self) -> None:
        try:
            self._client.close()
        except Exception:
            pass
