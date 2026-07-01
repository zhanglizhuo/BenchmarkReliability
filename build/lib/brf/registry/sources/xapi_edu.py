"""xAPI-Edu-Data (Kaggle / UCI)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class XAPIEduSource(DatasetSource):
    name = "xapi_edu"
    display_name = "xAPI-Edu-Data"
    version = "1.0"
    source_url = "https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data"
    license_info = "CC BY-SA 4.0 (Kaggle)"
    reference = "Amrieh et al. (2016)"
    task = "classification"
    n_samples = 480
    n_features = 72
    n_groups = 12
    grouping_description = "Student (12 anonymized IDs)"

    def download(self):
        from pathlib import Path as P
        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        valid_dir = ba_root / "datasets" / "xAPI-Edu"
        if valid_dir.exists():
            return valid_dir
        raise FileNotFoundError(
            "xAPI-Edu data not found. Please download from Kaggle "
            "and place under datasets/xAPI-Edu/ in BehaviorAudit repo."
        )

    def prepare(self):
        import sys
        from pathlib import Path as P

        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        if str(ba_root) not in sys.path:
            sys.path.insert(0, str(ba_root))

        from framework.adapters import XAPIEduAdapter
        adapter = XAPIEduAdapter()
        bundle = adapter.load(dataset_root=str(ba_root / "datasets" / "xAPI-Edu"))
        card = {
            "n_samples": len(bundle.y),
            "n_features": bundle.X.shape[1],
            "n_groups": len(np.unique(bundle.group_ids)),
            "source": "Kaggle / Kalboard 360",
            "features": [f"feat_{i}" for i in range(bundle.X.shape[1])],
        }
        return bundle.X, bundle.y, np.array(bundle.group_ids), card
