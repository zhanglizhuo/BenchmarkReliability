from typing import Sequence

import numpy as np


def compute_i(r2_values: Sequence[float], eps: float = 1e-8) -> float:
    r2_arr = np.array(r2_values)
    mean_r2 = float(np.mean(r2_arr))
    std_r2 = float(np.std(r2_arr, ddof=1))
    denom = max(abs(mean_r2), 1e-4) + eps
    return std_r2 / denom
