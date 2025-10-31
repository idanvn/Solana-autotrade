# Imports-only test (no network)
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
	sys.path.insert(0, str(ROOT))

from backend.core.wallet_manager import WalletManager  # noqa: E402
from backend.core.jupiter_client import JupiterClient  # noqa: E402
from backend.core.price_monitor import PriceMonitor  # noqa: E402

print("imports: OK")
