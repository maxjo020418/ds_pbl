import numpy as np


def rng(low: int = 10, high: int = 30, lam: float = 20.0) -> int:
    """Return a Poisson-distributed integer within [low, high]."""
    val = np.random.poisson(lam)
    return max(min(val, high), low)
