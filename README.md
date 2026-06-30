# benchmark-reliability

A Python package for computing the **Benchmark Reliability Framework (BRF)**: a four-dimension audit protocol that evaluates whether a predictive dataset is structurally reliable before model development.

## Installation

```bash
pip install benchmark-reliability
```

Requires Python 3.8+ with numpy, scikit-learn, and matplotlib.

## Quick Start

```python
import numpy as np
from brf import BRFAnalyzer

# Your data
X = np.random.randn(200, 10)
y = np.random.randn(200)
groups = np.random.choice(["A", "B", "C"], 200)

# Run the audit
analyzer = BRFAnalyzer(n_splits=30, n_permutations=200).fit(X, y, groups=groups)

# Results
print(analyzer.brf_vector)
# {'B': 0.123, 'I': 0.045, 'N': 0.97, 'M': 0.82,
#  'S': 0.925, 'E': 0.943, 'class': 'Reliable'}
```

## BRF Dimensions

| Dimension | Name | Meaning |
|-----------|------|---------|
| B | Baseline Gain | Model improvement over mean predictor |
| I | Instability | Sensitivity to train/test split choice |
| N | Null Separability | Signal distinguishability from noise |
| M | Metadata Sufficiency | Group structure completeness |

The embedding coordinates S = N - I (Signal Identifiability) and E = B + M (Epistemic Completeness) classify datasets into one of three categories:

| Class | Condition | Meaning |
|-------|-----------|---------|
| **Reliable** | S > 0 and E > 0.5 | Dataset supports reproducible model comparisons. Predictors carry signal beyond noise, and metadata (group structure) is adequate for cross-context evaluation. |
| **Fragile** | S > 0 and E <= 0.5 | Predictors show signal, but metadata is insufficient. Results may not generalize across groups (e.g., schools, courses, cohorts). Use with caution and report group-aware diagnostics. |
| **Void** | S <= 0 | No detectable signal beyond noise. Model performance on this dataset cannot be meaningfully interpreted. Consider whether the target, features, or sample size need revisiting. |

## Visualization

```python
from brf.phase import plot_phase_diagram

plot_phase_diagram(
    [analyzer.S], [analyzer.E],
    labels=[analyzer.class_],
    classes=[analyzer.class_],
)
```

## Export

```python
from brf.report import export_json, export_latex

export_json(analyzer.brf_vector, "results.json")
latex_table = export_latex(analyzer.brf_vector)
```

## Citation

If you use this package, please cite the BehaviorAudit paper:

```
BehaviorAudit: a four-dimension pre-modeling audit protocol
for educational prediction benchmarks. Scientific Reports (under review).
```

## Related Tools

- [rliable](https://github.com/google-research/rliable) (NeurIPS 2021 Outstanding Paper): statistically reliable evaluation of benchmark *results* (e.g., confidence intervals across seeds). BRF addresses a complementary question: structural reliability of the benchmark *dataset* itself (signal identifiability, instability, group adequacy).

## License

MIT

## Links

- GitHub: https://github.com/zhanglizhuo/BenchmarkReliability
- PyPI: https://pypi.org/project/benchmark-reliability/
