"""OULAD -- Open University Learning Analytics Dataset."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class OULADSource(DatasetSource):
    name = "oulad"
    display_name = "Open University Learning Analytics Dataset"
    version = "1.0"
    source_url = "https://analyse.kmi.open.ac.uk/open_dataset"
    license_info = "CC BY-SA 4.0"
    reference = "Kuzilek et al. (2017)"
    task = "classification"
    n_samples = 32593
    n_features = 44
    n_groups = 22
    grouping_description = "Course module (22)"

    def download(self):
        from pathlib import Path as P
        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        oulad_path = ba_root / "datasets" / "OULAD"
        if oulad_path.exists():
            return oulad_path
        raise FileNotFoundError(
            f"OULAD not found at {oulad_path}. "
            "Please download from https://analyse.kmi.open.ac.uk/open_dataset "
            "and place CSV files under datasets/OULAD/ in the BehaviorAudit repo."
        )

    def prepare(self):
        import sys
        from pathlib import Path as P

        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        if str(ba_root) not in sys.path:
            sys.path.insert(0, str(ba_root))

        from framework.adapters import OULADAdapter
        adapter = OULADAdapter()
        bundle = adapter.load(dataset_root=str(ba_root / "datasets" / "OULAD"))
        card = {
            "n_samples": len(bundle.y),
            "n_features": bundle.X.shape[1],
            "n_groups": len(np.unique(bundle.group_ids)),
            "source": "OULAD / Open University",
            "features": [f"feat_{i}" for i in range(bundle.X.shape[1])],
        }
        return bundle.X, bundle.y, np.array(bundle.group_ids), card
