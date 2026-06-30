import numpy as np

from brf.metrics import compute_b, compute_i, compute_n, compute_m


class TestComputeB:
    def test_perfect_prediction(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred_model = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred_baseline = np.array([2.5, 2.5, 2.5, 2.5])
        b = compute_b(y_true, y_pred_model, y_pred_baseline)
        assert b == 1.0

    def test_model_no_better_than_baseline(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred_model = np.array([2.5, 2.5, 2.5, 2.5])
        y_pred_baseline = np.array([2.5, 2.5, 2.5, 2.5])
        b = compute_b(y_true, y_pred_model, y_pred_baseline)
        assert b == 0.0

    def test_negative_b_gap(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred_model = np.array([4.0, 3.0, 2.0, 1.0])
        y_pred_baseline = np.array([2.5, 2.5, 2.5, 2.5])
        b = compute_b(y_true, y_pred_model, y_pred_baseline)
        assert b < 0.0


class TestComputeI:
    def test_zero_instability(self):
        values = [0.5, 0.5, 0.5, 0.5]
        i = compute_i(values)
        assert i == 0.0

    def test_low_instability(self):
        values = [0.5, 0.51, 0.49, 0.5]
        i = compute_i(values)
        assert 0.0 < i < 0.1

    def test_high_instability(self):
        values = [0.9, 0.1, 0.8, 0.2]
        i = compute_i(values)
        assert i > 0.5

    def test_eps_avoid_division_by_zero(self):
        values = [0.0, 0.0, 0.0, 0.0]
        i = compute_i(values)
        assert not np.isnan(i)
        assert np.isfinite(i)


class TestComputeN:
    def test_perfect_predictions(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        n = compute_n(y_true, y_pred, n_permutations=200)
        assert n >= 0.99

    def test_worse_than_random(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([5.0, 4.0, 3.0, 2.0, 1.0])
        n = compute_n(y_true, y_pred, n_permutations=200)
        assert n < 0.5

    def test_deterministic_seed(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0])
        y_pred = np.array([1.2, 2.3, 2.8, 4.1, 4.9, 6.0, 7.1, 7.8, 9.2, 9.9])
        n1 = compute_n(y_true, y_pred, n_permutations=100, seed=42)
        n2 = compute_n(y_true, y_pred, n_permutations=100, seed=42)
        assert n1 == n2

    def test_range_bounded(self):
        rng = np.random.default_rng(99)
        y_true = rng.normal(size=50)
        y_pred = y_true + rng.normal(scale=0.3, size=50)
        n = compute_n(y_true, y_pred, n_permutations=100)
        assert 0.0 <= n <= 1.0


class TestComputeM:
    def test_no_groups(self):
        m = compute_m(groups=None, n_features=10, n_samples=100)
        assert m == 0.0

    def test_single_group(self):
        groups = np.zeros(100)
        m = compute_m(groups=groups, n_features=10, n_samples=100)
        assert m == 0.0

    def test_perfectly_balanced_multi_group(self):
        groups = np.repeat([0, 1, 2, 3], 25)
        m = compute_m(groups=groups, n_features=10, n_samples=100)
        assert m > 0.5

    def test_imbalanced_groups_lower_score(self):
        balanced = np.repeat([0, 1, 2, 3], 25)
        imbalanced = np.concatenate([np.full(85, 0), np.full(5, 1), np.full(5, 2), np.full(5, 3)])
        m_bal = compute_m(groups=balanced, n_features=10, n_samples=100)
        m_imb = compute_m(groups=imbalanced, n_features=10, n_samples=100)
        assert m_bal > m_imb

    def test_range_bounded_01(self):
        rng = np.random.default_rng(42)
        for _ in range(10):
            n = rng.integers(5, 20)
            groups = rng.integers(0, n // 2, size=100)
            m = compute_m(groups=groups, n_features=20, n_samples=100)
            assert 0.0 <= m <= 1.0
