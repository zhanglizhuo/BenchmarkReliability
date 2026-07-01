---
title: 'benchmark-reliability: A Framework for Auditing Predictive Benchmark Datasets'
tags:
  - Python
  - machine learning
  - benchmarking
  - reproducibility
  - dataset quality
authors:
  - name: Lizhuo Zhang
    orcid: ~
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 1 July 2026
bibliography: paper.bib
---

# Summary

`benchmark-reliability` implements the Benchmark Reliability Framework (BRF),
a protocol that audits the structural reliability of predictive benchmark
datasets *before* model development. Unlike prior work that evaluates benchmark
results (e.g., model ranking stability across random seeds), BRF measures the
dataset itself: whether the features carry predictive signal above noise,
whether that signal is stable across data splits, and whether the grouping
structure (e.g., by school, hospital, or country) is adequate for cross-context
evaluation.

The package computes six continuous metrics from repeated train/test splits
with permutation null models. Two summary coordinates---Signal Identifiability
(S) and Epistemic Completeness (E)---capture the dataset's fitness for
meaningful model comparison. A structured diagnostic report explains *why*
a benchmark is in its current state (rather than assigning an opaque label)
and recommends concrete actions. The package also includes a built-in registry
of 16 group-aware educational datasets with download, SHA-256 verification, and
standardized preprocessing, plus a command-line interface (`brf audit`,
`brf registry sync`).

# Statement of Need

Predictive benchmarks drive progress in machine learning, but the reliability
of benchmarks themselves is rarely audited. Dataset shift, insufficient sample
sizes, poorly chosen grouping variables, and weak predictive signals can
produce benchmark rankings that are unstable or meaningless---yet researchers
typically discover these issues only after substantial model development effort.
Existing tools address adjacent problems: `rliable` [@agarwal2021] evaluates
the *results* of benchmark evaluations (stability of model rankings), while
datasheet frameworks [@gebru2021] document dataset contents without quantitative
measurement. No tool audited the *structural reliability* of the benchmark
dataset itself before model training.

`benchmark-reliability` fills this gap. It is designed for researchers who
build, curate, or use predictive benchmarks and want to know: *does this
dataset support reproducible model comparisons?* The package has been used
to audit 25 educational prediction benchmarks as part of the BRF Registry
[@zhang2025registry], revealing that the theoretically possible "Fragile"
regime (signal present but group structure inadequate) was never observed
across all 25 audited datasets---a negative result that challenges assumptions
about benchmark design.

# Functionality

- **BRF Audit.** `BRFAnalyzer.fit(X, y, groups)` computes B (predictive signal),
  I (instability), N (null separation), M (metadata adequacy), and the summary
  coordinates S and E from repeated ridge regression splits with permutation
  null models.

- **Structured Diagnosis.** `analyzer.diagnose(n_samples, n_features, n_groups)`
  returns per-dimension explanations with context-aware recommendations
  (e.g., "Only N=151 samples (~6 per group). Increase to 300+").

- **Percentile Ranking.** `analyzer.rank()` compares the dataset against the
  25 benchmarks in the BRF Registry, providing S and E percentile scores.

- **Built-in Registry.** 16 Dataset-as-Code modules in `brf.registry` provide
  download (`brf registry sync`), SHA-256 verification, and standardized
  preprocessing for group-aware educational benchmarks.

- **CLI.** `brf audit <dataset>` runs a full audit; `brf registry list` shows
  available datasets; `brf registry info <key>` shows metadata.

# Research Application

The package underpins the BRF Benchmark Registry v1.5 [@zhang2025registry], a
versioned collection of 25 group-aware educational prediction benchmark entries
used for a meta-analysis of benchmark reliability. The BehaviorAudit protocol
[@zhang2025behavior], which originated the BRF measurement dimensions, used an
early version of this package to audit seven datasets.

# Acknowledgements

We thank the maintainers of UCI ML Repository, OpenML, and PSLC DataShop for
making benchmark datasets publicly available.

# References
