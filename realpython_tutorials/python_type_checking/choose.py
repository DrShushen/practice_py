# choose.py

import random
from typing import Any, Sequence


def choose(items: Sequence[Any]) -> Any:
    return random.choice(items)


names = ["Guido", "Jukka", "Ivan"]

reveal_type(names)


name = choose(names)

reveal_type(name)
