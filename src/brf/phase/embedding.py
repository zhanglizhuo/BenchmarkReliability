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


def compute_phase(
    B: float = 0.0,
    I: float = 0.0,
    N: float = 0.0,
    M: float = 0.0,
) -> Tuple[float, float]:
    return compute_phase_from_brf(B, I, N, M)
