import math
import warnings
from typing import Optional

import numpy as np
from sklearn.base import clone
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
from sklearn.preprocessing import StandardScaler

from .metrics import compute_b, compute_i, compute_m
from .phase import compute_phase_from_brf, classify_dataset


class BRFAnalyzer:
    def __init__(
        self,
        n_splits: int = 30,
        n_permutations: int = 200,
        model=None,
        seed: int = 42,
        scale: bool = True,
    ):
        if n_splits < 2:
            raise ValueError("n_splits must be >= 2")
        self.n_splits = n_splits
        self.n_permutations = n_permutations
        self.model = model or Ridge(alpha=1.0)
        self.seed = seed
        self.scale = scale

        self._fitted = False
        self.B: Optional[float] = None
        self.I: Optional[float] = None
        self.N: Optional[float] = None
        self.M: Optional[float] = None
        self.S: Optional[float] = None
        self.E: Optional[float] = None
        self.class_: Optional[str] = None

    def _validate_inputs(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if X.ndim != 2:
            raise ValueError(f"X must be 2D, got shape {X.shape}")
        if y.ndim != 1:
            raise ValueError(f"y must be 1D, got shape {y.shape}")
        if len(X) != len(y):
            raise ValueError(f"X and y length mismatch: {len(X)} vs {len(y)}")
        if len(X) < 20:
            raise ValueError(f"Need at least 20 samples, got {len(X)}")
        if not np.all(np.isfinite(X)):
            raise ValueError("X contains NaN or Inf values")
        if not np.all(np.isfinite(y)):
            raise ValueError("y contains NaN or Inf values")
        unique_y = np.unique(y)
        if len(unique_y) <= 12 and np.all(unique_y == unique_y.astype(int)):
            warnings.warn(
                "y appears to be integer classification labels "
                f"({len(unique_y)} unique values). "
                "BRF is designed for regression targets."
            )
        return X, y

    def fit(self, X, y, groups=None):
        X, y = self._validate_inputs(X, y)
        n = len(y)

        if self.scale:
            scaler = StandardScaler()
            X = scaler.fit_transform(X)

        rng_cv = np.random.default_rng(self.seed)
        rng_perm = np.random.default_rng(self.seed + 10_007)

        r2_scores = []
        b_gains = []

        n_per_fold = max(3, math.ceil(self.n_permutations / self.n_splits))
        exceed_count = 0

        for i in range(self.n_splits):
            idx = rng_cv.permutation(n)
            split = max(1, int(0.8 * n))
            train_idx = idx[:split]
            test_idx = idx[split:]

            Xtr, Xte = X[train_idx], X[test_idx]
            ytr, yte = y[train_idx], y[test_idx]

            y_mean = np.full(len(yte), float(np.mean(ytr)))
            m = clone(self.model)
            m.fit(Xtr, ytr)
            y_pred = m.predict(Xte)

            r2_real = r2_score(yte, y_pred)
            r2_scores.append(r2_real)
            b_gains.append(compute_b(yte, y_pred, y_mean))

            perm_r2s = []
            for _ in range(n_per_fold):
                y_perm = rng_perm.permutation(ytr)
                m_perm = clone(self.model)
                m_perm.fit(Xtr, y_perm)
                y_pred_perm = m_perm.predict(Xte)
                perm_r2s.append(r2_score(yte, y_pred_perm))

            if r2_real > float(np.median(perm_r2s)):
                exceed_count += 1

        self.B = float(np.mean(b_gains))
        self.I = compute_i(r2_scores)
        self.N = exceed_count / self.n_splits
        self.M = compute_m(groups)
        self.S, self.E = compute_phase_from_brf(self.B, self.I, self.N, self.M)
        self.class_ = classify_dataset(self.S, self.E)
        self._fitted = True

        return self

    @property
    def brf_vector(self) -> dict:
        if not self._fitted:
            raise RuntimeError("call fit() before accessing brf_vector")
        return {
            "B": self.B,
            "I": self.I,
            "N": self.N,
            "M": self.M,
            "S": self.S,
            "E": self.E,
            "class": self.class_,
        }
