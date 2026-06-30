"""Entrance Exam (UCI ID 582)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class EntranceExamSource(DatasetSource):
    name = "entrance_exam"
    display_name = "Entrance Exam"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/582/student+academic+performance.zip"
    license_info = "CC BY 4.0"
    reference = "Bora & Dey (2021); UCI ID 582"
    task = "classification"
    n_samples = 666
    n_features = 49
    n_groups = 3
    grouping_description = "Qualification (3 categories)"

    def download(self):
        from pathlib import Path as P
        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        exam_path = ba_root / "datasets" / "StudentExam"
        if exam_path.exists():
            return exam_path
        # Fallback: download from UCI
        import urllib.request, zipfile, io
        dest = self._ensure_cache_dir()
        resp = urllib.request.urlopen(self.source_url)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest))
        return dest

    def prepare(self):
        import sys
        from pathlib import Path as P

        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        if str(ba_root) not in sys.path:
            sys.path.insert(0, str(ba_root))

        from framework.adapters import EntranceExamAdapter
        adapter = EntranceExamAdapter()
        dataset_root = str(ba_root / "datasets" / "StudentExam")
        bundle = adapter.load(dataset_root=dataset_root)
        card = {
            "n_samples": len(bundle.y),
            "n_features": bundle.X.shape[1],
            "n_groups": len(np.unique(bundle.group_ids)),
            "source": "UCI ID 582",
            "features": [f"feat_{i}" for i in range(bundle.X.shape[1])],
        }
        return bundle.X, bundle.y, np.array(bundle.group_ids), card
