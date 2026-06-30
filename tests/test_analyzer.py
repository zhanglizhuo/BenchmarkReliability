import numpy as np
import pytest

from brf import BRFAnalyzer


class TestBRFAnalyzer:
    def test_fit_returns_self(self):
        X = np.random.default_rng(0).normal(size=(100, 5))
        y = X[:, 0] + 0.1 * np.random.default_rng(0).normal(size=100)
        analyzer = BRFAnalyzer(n_splits=5, n_permutations=20, seed=42)
        result = analyzer.fit(X, y)
        assert result is analyzer

    def test_brf_vector_keys(self):
        X = np.random.default_rng(1).normal(size=(100, 5))
        y = X[:, 0] + 0.1 * np.random.default_rng(1).normal(size=100)
        analyzer = BRFAnalyzer(n_splits=5, n_permutations=20, seed=42)
        analyzer.fit(X, y)
        v = analyzer.brf_vector
        expected_keys = {"B", "I", "N", "M", "S", "E", "class"}
        assert set(v.keys()) == expected_keys

    def test_all_values_computed(self):
        X = np.random.default_rng(2).normal(size=(100, 5))
        y = X[:, 0] + 0.5 * X[:, 1] + np.random.default_rng(2).normal(scale=0.2, size=100)
        analyzer = BRFAnalyzer(n_splits=10, n_permutations=30, seed=42)
        analyzer.fit(X, y)
        v = analyzer.brf_vector
        for key in ["B", "I", "N", "M", "S", "E"]:
            assert v[key] is not None, f"{key} should not be None"
            assert np.isfinite(v[key]), f"{key} should be finite"
        assert v["class"] in ["Reliable", "Fragile", "Void"]

    def test_reliable_with_clean_signal(self):
        rng = np.random.default_rng(42)
        X = rng.normal(size=(200, 3))
        y = 2.0 * X[:, 0] + 1.5 * X[:, 1] + rng.normal(scale=0.1, size=200)
        analyzer = BRFAnalyzer(n_splits=10, n_permutations=50, seed=42)
        analyzer.fit(X, y)
        assert analyzer.class_ == "Reliable"

    def test_void_with_noise_only(self):
        rng = np.random.default_rng(42)
        X = rng.normal(size=(200, 3))
        y = rng.normal(size=200)
        analyzer = BRFAnalyzer(n_splits=10, n_permutations=50, seed=42)
        analyzer.fit(X, y)
        assert analyzer.class_ == "Void"

    def test_groups_affect_m_score(self):
        rng = np.random.default_rng(42)
        X = rng.normal(size=(200, 3))
        y = X[:, 0] + 0.3 * rng.normal(size=200)

        a1 = BRFAnalyzer(n_splits=5, n_permutations=20, seed=42)
        a1.fit(X, y, groups=np.repeat([0, 1, 2, 3], 50))
        m_with = a1.M

        a2 = BRFAnalyzer(n_splits=5, n_permutations=20, seed=42)
        a2.fit(X, y)
        m_without = a2.M

        assert m_with > 0.0
        assert m_without == 0.0

    def test_custom_model(self):
        from sklearn.linear_model import LinearRegression

        X = np.random.default_rng(3).normal(size=(100, 3))
        y = X[:, 0] + 0.2 * np.random.default_rng(3).normal(size=100)
        analyzer = BRFAnalyzer(n_splits=5, n_permutations=20, model=LinearRegression(), seed=42)
        analyzer.fit(X, y)
        assert analyzer.class_ is not None

    def test_nan_input_raises(self):
        X = np.array([[1.0, np.nan], [2.0, 3.0], [4.0, 5.0], [6.0, 7.0], [8.0, 9.0]])
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        analyzer = BRFAnalyzer(n_splits=2, n_permutations=5)
        with pytest.raises(ValueError, match="NaN"):
            analyzer.fit(X, y)

    def test_inf_input_raises(self):
        X = np.array([[1.0, np.inf], [2.0, 3.0], [4.0, 5.0], [6.0, 7.0], [8.0, 9.0]])
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        analyzer = BRFAnalyzer(n_splits=2, n_permutations=5)
        with pytest.raises(ValueError, match="Inf"):
            analyzer.fit(X, y)

    def test_too_few_samples_raises(self):
        X = np.random.default_rng(0).normal(size=(3, 2))
        y = np.random.default_rng(0).normal(size=3)
        analyzer = BRFAnalyzer(n_splits=2, n_permutations=5)
        with pytest.raises(ValueError, match="5 samples"):
            analyzer.fit(X, y)

    def test_dimension_mismatch_raises(self):
        X = np.random.default_rng(0).normal(size=(10, 2))
        y = np.random.default_rng(0).normal(size=5)
        analyzer = BRFAnalyzer(n_splits=2, n_permutations=5)
        with pytest.raises(ValueError, match="length mismatch"):
            analyzer.fit(X, y)

    def test_1d_X_raises(self):
        X = np.random.default_rng(0).normal(size=10)
        y = np.random.default_rng(0).normal(size=10)
        analyzer = BRFAnalyzer(n_splits=2, n_permutations=5)
        with pytest.raises(ValueError, match="2D"):
            analyzer.fit(X, y)
