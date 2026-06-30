from typing import Optional

import numpy as np


def compute_m(
    groups: Optional[np.ndarray] = None,
    n_features: int = 0,
    n_samples: int = 0,
) -> float:
    if groups is None:
        return 0.0

    group_arr = np.asarray(groups)  # type: ignore
    unique, counts = np.unique(group_arr, return_counts=True)
    n_groups = len(unique)

    if n_groups <= 1:
        return 0.0

    probs = counts / counts.sum()
    entropy = -np.sum(probs * np.log(probs + 1e-10))
    max_entropy = np.log(n_groups)
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

    group_balance = 1.0 - float(np.std(counts) / (np.mean(counts) + 1e-8))
    group_balance = max(0.0, min(1.0, group_balance))

    return float(0.5 * normalized_entropy + 0.5 * group_balance)
