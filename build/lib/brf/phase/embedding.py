from typing import Tuple


def compute_phase_from_brf(
    B: float,
    I: float,
    N: float,
    M: float,
) -> Tuple[float, float]:
    S = N - I
    E = B + M
    return S, E
