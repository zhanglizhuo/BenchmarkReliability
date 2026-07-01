import json
import math
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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
        self.class_: Optional[str] = None  # retained for backward compat
        self._registry_ref: Optional[Dict] = None  # loaded lazily

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

    # ---- improved reporting (v0.2) ----

    def diagnose(self) -> Dict[str, str]:
        """Return structured diagnosis explaining *why* the dataset is in its current state.

        Replaces the opaque 3-class label with interpretable per-dimension
        explanations, enabling benchmark designers to understand what to fix.
        """
        if not self._fitted:
            raise RuntimeError("call fit() before accessing diagnose()")

        issues = {}
        suggestions = {}

        # --- Predictive signal (B) ---
        if self.B < 0:
            issues["B"] = (f"Model performs WORSE than the mean baseline "
                           f"(B={self.B:.3f}). The features carry no useful "
                           f"predictive signal for this target.")
            suggestions["B"] = "Reconsider feature engineering or target definition."
        elif self.B < 0.05:
            issues["B"] = (f"Marginal improvement over mean baseline "
                           f"(B={self.B:.3f}). Features explain very little variance.")
            suggestions["B"] = "Add more informative features or reframe the task."
        elif self.B < 0.2:
            issues["B"] = (f"Moderate predictive signal (B={self.B:.3f}).")
            suggestions["B"] = None
        else:
            issues["B"] = (f"Strong predictive signal (B={self.B:.3f}).")
            suggestions["B"] = None

        # --- Instability (I) ---
        if self.I > 1.0:
            issues["I"] = (f"High cross-split instability (I={self.I:.3f}). "
                           f"Model R^2 varies dramatically depending on which "
                           f"samples happen to be in the test set.")
            suggestions["I"] = ("Increase sample size (N), reduce feature count (p), "
                               "or use regularization.")
        elif self.I > 0.3:
            issues["I"] = (f"Moderate instability (I={self.I:.3f}).")
            suggestions["I"] = "Consider larger N or fewer features for more stable estimates."
        else:
            issues["I"] = (f"Low instability (I={self.I:.3f}). "
                           f"Model is robust to data split variation.")
            suggestions["I"] = None

        # --- Null separation (N) ---
        if self.N < 0.5:
            issues["N"] = (f"Model rarely beats permutation baseline "
                           f"(N={self.N:.3f}). The signal is indistinguishable "
                           f"from random noise.")
            suggestions["N"] = ("The model is effectively fitting noise. "
                               "Consider whether a predictive relationship exists.")
        elif self.N < 0.8:
            issues["N"] = (f"Model sometimes fails to beat permutation "
                           f"(N={self.N:.3f}). Signal is present but inconsistent.")
            suggestions["N"] = "Increase sample size or feature quality for more reliable separation."
        else:
            issues["N"] = (f"Model consistently beats permutation "
                           f"(N={self.N:.3f}). Clear signal above noise.")
            suggestions["N"] = None

        # --- Metadata adequacy (M) ---
        if self.M < 0.1:
            issues["M"] = (f"Insufficient group metadata (M={self.M:.3f}). "
                           f"Groups are too few, highly imbalanced, or absent.")
            suggestions["M"] = ("Add or improve group annotations. "
                               "Consider whether an alternative grouping variable "
                               "captures more meaningful structure.")
        elif self.M < 0.3:
            issues["M"] = (f"Weak group metadata (M={self.M:.3f}). "
                           f"Group structure exists but is sparse or imbalanced.")
            suggestions["M"] = "Use a finer-grained grouping variable if available."
        elif self.M < 0.5:
            issues["M"] = (f"Moderate group metadata (M={self.M:.3f}).")
            suggestions["M"] = None
        else:
            issues["M"] = (f"Strong group metadata (M={self.M:.3f}). "
                           f"Group structure is well-defined and balanced.")
            suggestions["M"] = None

        # --- Synthesis ---
        if self.S <= 0:
            primary = ("The model shows no detectable, stable signal "
                      f"(S={self.S:.3f} <= 0). Performance differences between "
                      f"models on this benchmark may not be meaningful.")
        elif self.E <= 0.5:
            primary = ("Predictive signal is present (S>0) but the benchmark "
                      f"lacks sufficient evidence (E={self.E:.3f} <= 0.5). "
                      f"Results may not generalize across groups.")
        else:
            primary = ("The benchmark shows stable predictive signal and "
                      f"adequate group structure (S={self.S:.3f}, E={self.E:.3f}). "
                      f"Model comparisons are likely reproducible.")

        return {
            "summary": primary,
            "details": issues,
            "recommendations": {k: v for k, v in suggestions.items() if v},
        }

    def rank(self) -> Dict[str, float]:
        """Percentile rank of S and E against the BRF Registry v1.5 benchmarks.

        Returns percentiles (0-100) indicating where this dataset's S and E
        fall relative to the 25 audited benchmarks. Requires the registry
        data to be accessible.
        """
        if not self._fitted:
            raise RuntimeError("call fit() before accessing rank()")
        ref = self._load_registry_ref()
        if ref is None:
            return {"S_percentile": None, "E_percentile": None,
                    "note": "Registry data not available for ranking"}

        s_vals = sorted(r["S"] for r in ref if r["S"] is not None)
        e_vals = sorted(r["E"] for r in ref if r["E"] is not None)

        def pctile(vals, x):
            return sum(1 for v in vals if v <= x) / len(vals) * 100

        return {
            "S_percentile": round(pctile(s_vals, self.S), 1),
            "E_percentile": round(pctile(e_vals, self.E), 1),
            "reference": f"BRF Registry v1.5 ({len(s_vals)} benchmarks)",
        }

    def recommend(self) -> str:
        """One-paragraph actionable recommendation for benchmark improvement."""
        d = self.diagnose()
        recs = d["recommendations"]
        if not recs:
            return ("Benchmark metrics are within normal ranges. "
                    "No specific action recommended.")
        # Prioritize: B < 0 is most critical, then N < 0.5, then I > 1, then M < 0.1
        priority = []
        if self.B < 0:
            priority.append("B")
        if self.N < 0.5:
            priority.append("N")
        if self.I > 1.0:
            priority.append("I")
        if self.M < 0.1:
            priority.append("M")
        if not priority:
            priority = [k for k in recs]

        lines = [
            f"This benchmark has {len(recs)} dimension(s) needing attention. "
            f"Primary concern: {recs[priority[0]]}"
        ]
        return " ".join(lines)

    def _load_registry_ref(self) -> Optional[List[Dict]]:
        """Load Registry reference data for percentile ranking."""
        if self._registry_ref is not None:
            return self._registry_ref
        # Search for registry_v1.5.json in known locations
        candidates = [
            Path(__file__).parent.parent.parent.parent
            / "BRFRegistry" / "results" / "registry_v1.5.json",
            Path(__file__).parent.parent.parent
            / "BRFRegistry" / "results" / "registry_v1.5.json",
        ]
        for p in candidates:
            if p.exists():
                with open(p) as f:
                    data = json.load(f)
                refs = []
                for v in data.values():
                    if v.get("brf_result"):
                        refs.append({
                            "S": v["brf_result"]["S"],
                            "E": v["brf_result"]["E"],
                            "B": v["brf_result"]["B"],
                            "I": v["brf_result"]["I"],
                            "N": v["brf_result"]["N"],
                            "M": v["brf_result"]["M"],
                        })
                self._registry_ref = refs
                return refs
        return None
