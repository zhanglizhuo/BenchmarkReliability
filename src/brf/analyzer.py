import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score

from .metrics import compute_b, compute_i, compute_n, compute_m
from .phase import compute_phase_from_brf, classify_dataset


class BRFAnalyzer:
    def __init__(
        self,
        n_splits: int = 100,
        n_permutations: int = 500,
        model=None,
        seed: int = 42,
    ):
        self.n_splits = n_splits
        self.n_permutations = n_permutations
        self.model = model or Ridge(alpha=1.0)
        self.seed = seed

        self.B: float | None = None
        self.I: float | None = None
        self.N: float | None = None
        self.M: float | None = None
        self.S: float | None = None
        self.E: float | None = None
        self.class_: str | None = None

    def fit(self, X, y, groups=None):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        rng = np.random.default_rng(self.seed)

        r2_scores = []
        b_gains = []

        for i in range(self.n_splits):
            idx = rng.permutation(len(y))
            split = max(1, int(0.8 * len(y)))
            train_idx = idx[:split]
            test_idx = idx[split:]

            Xtr, Xte = X[train_idx], X[test_idx]
            ytr, yte = y[train_idx], y[test_idx]

            y_mean = np.full(len(yte), float(np.mean(ytr)))
            m = self.model.__class__(**self.model.get_params())
            m.fit(Xtr, ytr)
            y_pred = m.predict(Xte)

            r2_scores.append(r2_score(yte, y_pred))
            b_gains.append(compute_b(yte, y_pred, y_mean))

        self.B = float(np.mean(b_gains))
        self.I = compute_i(r2_scores)

        final_model = self.model.__class__(**self.model.get_params())
        final_model.fit(X, y)
        y_pred_full = final_model.predict(X)
        self.N = compute_n(y, y_pred_full, self.n_permutations, self.seed)

        self.M = compute_m(groups, X.shape[1], len(y))

        self.S, self.E = compute_phase_from_brf(self.B, self.I, self.N, self.M)
        self.class_ = classify_dataset(self.S, self.E)

        return self

    @property
    def brf_vector(self) -> dict:
        return {
            "B": self.B,
            "I": self.I,
            "N": self.N,
            "M": self.M,
            "S": self.S,
            "E": self.E,
            "class": self.class_,
        }

    def summary(self) -> dict:
        return self.brf_vector
