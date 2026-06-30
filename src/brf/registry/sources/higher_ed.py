"""Higher Education Students Performance (UCI ID 856)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class HigherEdSource(DatasetSource):
    name = "higher_ed"
    display_name = "Higher Education Students Performance"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/856/higher+education+students+performance+evaluation.zip"
    license_info = "CC BY 4.0"
    reference = "Yilmaz & Sekeroglu (2020); UCI ID 856"
    task = "regression"
    n_samples = 145
    n_features = 31
    n_groups = 9
    grouping_description = "Course (9 categories)"

    def download(self):
        from pathlib import Path as P
        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        exam_path = ba_root / "datasets" / "StudentExam"
        if exam_path.exists():
            return exam_path
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

        from framework.adapters import HigherEdAdapter
        adapter = HigherEdAdapter()
        bundle = adapter.load(dataset_root=str(ba_root / "datasets" / "StudentExam"))
        card = {
            "n_samples": len(bundle.y),
            "n_features": bundle.X.shape[1],
            "n_groups": len(np.unique(bundle.group_ids)),
            "source": "UCI ID 856",
            "features": [f"feat_{i}" for i in range(bundle.X.shape[1])],
        }
        return bundle.X, bundle.y, np.array(bundle.group_ids), card
