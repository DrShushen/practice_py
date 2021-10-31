# player_order.py

from typing import Sequence, Optional


def player_order(
    names: Sequence[str], start: Optional[str] = None
) -> Sequence[str]:
    start_idx = names.index(start)
    return names[start_idx:] + names[:start_idx]
