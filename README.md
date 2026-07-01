# benchmark-reliability

**Benchmark Reliability Framework (BRF)**  --  audit whether a predictive benchmark
dataset is structurally reliable *before* model development.

```
pip install benchmark-reliability
```

Requires Python 3.8+ with numpy, scikit-learn, pandas, scipy, openml.

## Quick Start

### Audit a dataset from the Registry

```python
from brf.registry import REGISTRY_SOURCES
from brf import BRFAnalyzer
from sklearn.preprocessing import StandardScaler

# Load Teaching Assistant Evaluation (UCI ID 100)
source = REGISTRY_SOURCES["tae"]
X, y, groups, metadata = source.prepare()

# Standardize and audit
X_scaled = StandardScaler().fit_transform(X)
analyzer = BRFAnalyzer(n_splits=30, n_permutations=200).fit(X_scaled, y, groups=groups)

# Continuous metrics (always use these)
print(f"S={analyzer.S:.3f}  E={analyzer.E:.3f}")
# S=-0.423  E=0.746

# Diagnostic report: explains WHY, not just a label
print(analyzer.diagnose()["summary"])
# "The model shows no detectable, stable signal (S=-0.423 <= 0). ..."

# Per-dimension details + actionable recommendations
for dim, issue in analyzer.diagnose()["details"].items():
    print(f"  {dim}: {issue}")

# Percentile rank against 25 audited benchmarks
print(analyzer.rank())
# {'S_percentile': 16.0, 'E_percentile': 36.0, ...}

# One-paragraph recommendation
print(analyzer.recommend())
```

### Browse the Registry

```bash
$ brf registry list
BRF Registry

  assistments          ASSISTments 2009-2010           N= 3729  G= 124
  college_scorecard    US College Scorecard            N= 7804  G=  59
  oulad                Open University Learning ...    N=32593  G=  22
  tae                  Teaching Assistant Evaluation   N=  151  G=  25
  ...

$ brf audit tae
BRF Audit: Teaching Assistant Evaluation (tae)
  N=151, p=4, G=25
  B=0.1172  I=1.3559  N=0.9333  M=0.6288
  S=-0.4226  E=0.7460  ->  Void
```

### Download and verify all datasets

```bash
$ brf registry sync     # download + SHA-256 verify all
$ brf registry info oulad
  name: oulad
  display_name: Open University Learning Analytics Dataset
  n_samples: 32593  n_features: 44  n_groups: 22
  education_level: Higher Education
  country: UK
  ...
```

## BRF Metrics

The framework computes six continuous metrics. S and E are the primary
summary coordinates; the three-class label (Reliable/Void/Fragile) is
communication shorthand only --- **the signal is in the continuous values**.

| Metric | Formula | Meaning |
|--------|---------|---------|
| B | mean(Delta R^2 vs mean baseline) | Predictive signal strength |
| I | std(R^2) / max(|mean(R^2)|, 1e-4) + 1e-8 | Intrinsic instability |
| N | fraction of folds where R^2_real > median(R^2_perm) | Null separation |
| M | 0.5 * norm_group_entropy + 0.5 * group_balance | Metadata adequacy |
| S | N - I | Stability (signal above noise) |
| E | B + M | Evidence (predictive + structural) |

Use `analyzer.diagnose()` for per-dimension explanations and actionable
recommendations, or `analyzer.rank()` to see percentile scores against
the 25 benchmarks in the BRF Registry.

## CLI Reference

```
brf audit <dataset_key>         # run BRF on a registered dataset
brf registry list               # list all datasets
brf registry download <key>     # download + cache
brf registry sync               # download + verify all datasets
brf registry info <key>         # show full metadata
brf registry verify <key>       # SHA-256 checksum check
```

## Export

```python
from brf.report import export_json, export_latex

export_json(analyzer.brf_vector, "results.json")
latex_table = export_latex(analyzer.brf_vector)
```

## Citation

To cite the BRF framework and package (JOSS paper forthcoming):

```bibtex
@software{zhang2026brf,
  author = {Lizhuo Zhang},
  title = {benchmark-reliability: Benchmark Reliability Framework},
  url = {https://github.com/zhanglizhuo/BenchmarkReliability},
  version = {0.2.1},
  year = {2026},
}
```

The behavior audit protocol is described in:

> Zhang, L. *BehaviorAudit: a four-dimension protocol for auditing
> benchmark reliability under group-aware evaluation.*
> Scientific Reports (under review).

## Related Work

- [rliable](https://github.com/google-research/rliable) (NeurIPS 2021): evaluates
  reliability of benchmark *results* (confidence intervals across seeds).
  BRF addresses the complementary question: structural reliability of the
  benchmark *dataset* itself.
- [OpenML](https://openml.org), [UCI ML Repository](https://archive.ics.uci.edu):
  general-purpose dataset catalogs. The BRF Registry adds group-aware metadata,
  SHA-256 verification, versioning, and a standardized pipeline for
  reliability auditing  --  filling a gap these platforms do not address.

## License

MIT
