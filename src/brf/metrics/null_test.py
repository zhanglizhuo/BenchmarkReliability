import numpy as np
from sklearn.metrics import r2_score


def compute_n(
    y_true: np.ndarray,
    y_pred_real: np.ndarray,
    n_permutations: int = 500,
    seed: int = 42,
) -> float:
    rng = np.random.default_rng(seed)
    r2_real = r2_score(y_true, y_pred_real)

    count_exceed = 0
    for _ in range(n_permutations):
        y_perm = rng.permutation(y_true)
        r2_perm = r2_score(y_perm, y_pred_real)
        if r2_real >= r2_perm:
            count_exceed += 1

    return count_exceed / n_permutations
