"""UCI Student Performance (UCI ID 320)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class UCIStudentSource(DatasetSource):
    name = "uci_student"
    display_name = "UCI Student Performance"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
    license_info = "CC BY 4.0"
    reference = "Cortez & Silva (2008)"
    task = "regression"
    n_samples = 649
    n_features = 56
    n_groups = 2
    grouping_description = "School (2 categories)"

    def download(self):
        from pathlib import Path as P
        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        uci_path = ba_root / "datasets" / "UCI"
        if uci_path.exists():
            return uci_path
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

        from framework.adapters import UCIStudentAdapter
        adapter = UCIStudentAdapter()
        bundle = adapter.load(dataset_root=str(ba_root / "datasets" / "UCI"))
        card = {
            "n_samples": len(bundle.y),
            "n_features": bundle.X.shape[1],
            "n_groups": len(np.unique(bundle.group_ids)),
            "source": "UCI ID 320",
            "features": [f"feat_{i}" for i in range(bundle.X.shape[1])],
        }
        return bundle.X, bundle.y, np.array(bundle.group_ids), card
