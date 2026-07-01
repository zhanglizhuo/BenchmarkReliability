"""MM-TBA -- Multi-Modal Teaching Behavior Analysis."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class MMTBASource(DatasetSource):
    name = "mm_tba"
    display_name = "MM-TBA Teaching Behavior Analysis"
    version = "1.0"
    source_url = "https://github.com/broadsense/MM-TBA"
    license_info = "TBD"
    reference = "Huang et al. (2025)"
    task = "regression"
    n_samples = 186
    n_features = 13
    n_groups = 0
    grouping_description = "None (no grouping metadata)"
    notes = "LLM-scored benchmark. No grouping variable available."

    def download(self):
        from pathlib import Path as P
        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        mmtba_path = ba_root / "datasets" / "MM-TBA"
        if mmtba_path.exists():
            return mmtba_path
        raise FileNotFoundError(f"MM-TBA not found at {mmtba_path}")

    def prepare(self):
        import sys
        from pathlib import Path as P

        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        if str(ba_root) not in sys.path:
            sys.path.insert(0, str(ba_root))

        from framework.adapters import MMTBAAdapter
        adapter = MMTBAAdapter()
        bundle = adapter.load(dataset_root=str(ba_root / "datasets" / "MM-TBA"))
        card = {
            "n_samples": len(bundle.y),
            "n_features": bundle.X.shape[1],
            "n_groups": 0,
            "source": "MM-TBA (GitHub)",
            "features": [f"feat_{i}" for i in range(bundle.X.shape[1])],
        }
        return bundle.X, bundle.y, None, card
