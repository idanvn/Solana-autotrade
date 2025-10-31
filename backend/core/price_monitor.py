from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Tuple


@dataclass
class PriceMonitor:
    """Lightweight signal scaffolding for volume spikes and price momentum.

    Provide your own data feed and call `add_point(ts, price, volume)`.
    """

    max_points: int = 500

    def __post_init__(self) -> None:
        self.points: Deque[Tuple[float, float, float]] = deque(maxlen=self.max_points)

    def add_point(self, ts: float, price: float, volume: float) -> None:
        self.points.append((ts, price, volume))

    def _window(self, n: int):
        if n <= 0:
            return []
        return list(self.points)[-n:]

    def volume_spike(self, multiplier: float = 4.0, window: int = 20) -> bool:
        win = self._window(window)
        if len(win) < window:
            return False
        vols = [v for _, _, v in win]
        avg = sum(vols[:-1]) / max(1, len(vols) - 1)
        return vols[-1] >= multiplier * avg if avg > 0 else False

    def momentum(self, min_change_pct: float = 3.0, lookback: int = 10) -> bool:
        win = self._window(lookback)
        if len(win) < lookback:
            return False
        p0 = win[0][1]
        p1 = win[-1][1]
        if p0 <= 0:
            return False
        change_pct = (p1 - p0) / p0 * 100
        return change_pct >= min_change_pct

    def signal(self) -> dict:
        return {
            "volume_spike": self.volume_spike(),
            "momentum": self.momentum(),
        }
