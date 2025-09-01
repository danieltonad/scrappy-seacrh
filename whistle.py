from typing import Set


def load_pussies() -> Set[str]:
    with open("pussies.txt", "r") as f:
        return set(f.read().splitlines())
    

