# BenchmarkReliability — BRF Python Package

## Target

Provide a standardized, pip-installable Python package that computes the Benchmark Reliability Field (BRF) for any predictive dataset, enabling researchers to run the four-dimension audit protocol with a single API call.

## Method

The package wraps the core logic from the BehaviorAudit project into a sklearn-style API:

```python
from brf import BRFAnalyzer
from brf.phase import plot_phase_diagram
from brf.report import export_json

analyzer = BRFAnalyzer(n_splits=30, n_permutations=200).fit(X, y, groups=groups)
print(analyzer.brf_vector)   # (B, I, N, M) → (S, E) → class

# Visualization
plot_phase_diagram(
    [analyzer.S], [analyzer.E],
    labels=[analyzer.class_],
    classes=[analyzer.class_],
)

# Export
export_json(analyzer.brf_vector, "results.json")
```

## Package Structure

```
brf/
├── __init__.py
├── analyzer.py          ← BRFAnalyzer main class
├── metrics/
│   ├── baseline_gap.py  ← B
│   ├── instability.py   ← I
│   ├── null_test.py     ← N (permutation test)
│   └── metadata.py      ← M
├── phase/
│   ├── embedding.py     ← S = N - I, E = B + M
│   ├── classifier.py    ← Reliable / Fragile / Void
│   └── visualization.py ← phase diagram, clustering plot
├── report/
│   ├── json_export.py
│   └── latex_export.py
```

## Steps

### Phase 1: Package skeleton (1-2 weeks)
- [x] Initialize Python project with `pyproject.toml`
- [x] Implement `BRFAnalyzer` main class with fit/predict interface
- [x] Port `compute_b`, `compute_i`, `compute_n`, `compute_m` from BehaviorAudit
- [x] Write unit tests for each metric

### Phase 2: Phase embedding + classification (1 week)
- [x] Implement `compute_phase(S, E)` and `classify_dataset(S, E)`
- [x] Build phase diagram visualization (matplotlib)
- [ ] Test on all 7 datasets from BehaviorAudit; verify BRF output matches SR paper results

### Phase 3: Documentation + distribution (1-2 weeks)
- [ ] Write README with quick-start tutorial and API docs
- [ ] Publish to TestPyPI → PyPI
- [ ] Set up ReadTheDocs for auto-generated documentation
- [ ] Add GitHub Actions CI (test on Python 3.9–3.12)

### Phase 4: HuggingFace Hub integration (optional, 1 week)
- [ ] Add HF dataset loading wrapper
- [ ] Allow `brf.fit(dataset_id="OULAD")` shorthand

## Dependencies

- `numpy`, `scipy`, `scikit-learn`
- `matplotlib`, `seaborn` (visualization)
- `pandas` (report export)
- No deep learning dependencies required

## Relationship to Sister Repos

- `BehaviorAudit/`: source of the audit logic; this package refactors and generalizes it
- `LLMScoringAudit/`: first applied use case (MM-TBA × multiple LLMs)
- `BenchmarkPhase/`: large-scale application (30 datasets BRF leaderboard)
- `llm-annotation/`: cited for complementary MLLM pseudo-label reliability findings

## Target Journal

- Journal of Open Source Software (JOSS) — tool paper, lightweight submission
- Followed by application papers in C&E / BJET

## Timeline

- Phase 1–2: 3 weeks
- Phase 3: 2 weeks
- Phase 4: optional
- JOSS submission: after Phase 3
