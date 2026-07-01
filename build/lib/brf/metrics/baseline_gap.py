import numpy as np
from sklearn.metrics import r2_score


def compute_b(
    y_true: np.ndarray,
    y_pred_model: np.ndarray,
    y_pred_baseline: np.ndarray,
) -> float:
    r2_model = r2_score(y_true, y_pred_model)
    r2_baseline = r2_score(y_true, y_pred_baseline)
    return float(r2_model - r2_baseline)
