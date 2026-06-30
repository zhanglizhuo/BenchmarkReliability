from typing import List

import numpy as np


def compute_i(r2_values: List[float], eps: float = 1e-8) -> float:
    r2_arr = np.array(r2_values)
    mean_r2 = float(np.mean(r2_arr))
    std_r2 = float(np.std(r2_arr))
    return std_r2 / (abs(mean_r2) + eps)
