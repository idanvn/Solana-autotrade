from __future__ import annotations

import json
from typing import Any, Dict, Optional

import requests


class OrcaClient:
    """Orca DEX client for Solana trading.
    
    Orca is a major Solana DEX with good liquidity and API.
    Docs: https://docs.orca.so/
    """

    def __init__(self, base_url: str = "https://api.orca.so", timeout: int = 20) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # --- Pool discovery ---
    def get_pools(self) -> Dict[str, Any]:
        """Get all available pools from Orca."""
        url = f"{self.base_url}/v1/whirlpool/list"
        r = requests.get(url, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def find_best_pool(self, input_mint: str, output_mint: str) -> Optional[Dict[str, Any]]:
        """Find the pool with highest liquidity for a token pair."""
        pools_data = self.get_pools()
        
        matching_pools = []
        for pool in pools_data.get("whirlpools", []):
            token_a = pool.get("tokenA", {}).get("mint", "")
            token_b = pool.get("tokenB", {}).get("mint", "")
            
            # Check both directions
            if (token_a == input_mint and token_b == output_mint) or \
               (token_a == output_mint and token_b == input_mint):
                matching_pools.append(pool)
        
        if not matching_pools:
            return None
        
        # Sort by liquidity (highest first)
        matching_pools.sort(key=lambda p: float(p.get("liquidity", "0")), reverse=True)
        return matching_pools[0]

    # --- Quote simulation ---
    def get_quote(
        self,
        input_mint: str,
        output_mint: str,
        amount: int,
        slippage_bps: int = 50,
    ) -> Dict[str, Any]:
        """Get a quote for swapping tokens.
        
        Note: This is a simplified simulation since Orca doesn't have 
        a direct quote API like Jupiter. In production, you'd use
        the Orca SDK or on-chain calculation.
        """
        pool = self.find_best_pool(input_mint, output_mint)
        if not pool:
            raise RuntimeError(f"No pool found for {input_mint} -> {output_mint}")
        
        # Extract pool info
        token_a = pool.get("tokenA", {})
        token_b = pool.get("tokenB", {})
        liquidity = float(pool.get("liquidity", "1"))
        
        # Determine which token is which
        if token_a.get("mint") == input_mint:
            input_token = token_a
            output_token = token_b
        else:
            input_token = token_b
            output_token = token_a
        
        # Simplified price calculation (not accurate, just for demo)
        # In reality, you'd use the Whirlpool price formula
        input_decimals = input_token.get("decimals", 9)
        output_decimals = output_token.get("decimals", 6)
        
        # Mock rate: SOL = ~$140, USDC = $1 (adjust as needed)
        if input_mint == "So11111111111111111111111111111111111111112":  # SOL
            mock_rate = 140.0  # SOL to USDC rate
            raw_output = int(amount * mock_rate * (10 ** output_decimals) / (10 ** input_decimals))
        else:
            mock_rate = 1/140.0  # USDC to SOL rate  
            raw_output = int(amount * mock_rate * (10 ** output_decimals) / (10 ** input_decimals))
        
        # Apply slippage
        slippage_factor = (10000 - slippage_bps) / 10000
        final_output = int(raw_output * slippage_factor)
        
        return {
            "inputMint": input_mint,
            "outputMint": output_mint,
            "inAmount": str(amount),
            "outAmount": str(final_output),
            "slippageBps": slippage_bps,
            "dex": "Orca",
            "poolAddress": pool.get("address"),
            "liquidity": pool.get("liquidity"),
            "priceImpactPct": 0.1,  # Mock value
        }

    # --- Integration with existing wallet ---
    def swap_with_wallet(self, wallet, quote: Dict[str, Any], **kwargs) -> str:
        """Build swap transaction for Orca.
        
        Note: This is a placeholder. Actual Orca swaps require:
        1. Using Orca SDK to build the instruction
        2. Creating a transaction with the swap instruction
        3. Signing and sending
        
        For now, this returns a mock transaction signature.
        """
        print("🐋 Orca swap simulation:")
        print(f"   Input: {quote['inAmount']} units of {quote['inputMint'][:8]}...")
        print(f"   Output: {quote['outAmount']} units of {quote['outputMint'][:8]}...")
        print(f"   Pool: {quote['poolAddress']}")
        print("   ⚠️  Mock mode - no actual transaction sent")
        
        return "mock_signature_orca_" + quote['poolAddress'][:8]