"""Student Dropout (UCI ID 697)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class StudentDropoutSource(DatasetSource):
    name = "student_dropout"
    display_name = "Student Dropout and Academic Success"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/697/predict+students+dropout+and+academic+success.zip"
    license_info = "CC BY 4.0"
    reference = "Realinho et al. (2022); UCI ID 697"
    task = "classification"
    n_samples = 3630
    n_features = 36
    n_groups = 17
    grouping_description = "Course (17 categories)"

    def download(self):
        import urllib.request, zipfile, io, shutil
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "data.csv"
        if csv_path.exists():
            return csv_path
        resp = urllib.request.urlopen(self.source_url)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        for f in sorted(dest_dir.glob("**/*.csv")):
            if "dropout" in f.name.lower() or "data" in f.name.lower():
                return f
        return dest_dir

    def prepare(self):
        import pandas as pd

        # Try BehaviorAudit adapter first (has proven preprocessing)
        from pathlib import Path as P
        import sys
        ba_root = P(__file__).resolve().parent.parent.parent.parent / "AutoResearchClaw" / "BehaviorAudit"
        if ba_root.exists() and str(ba_root) not in sys.path:
            sys.path.insert(0, str(ba_root))

        try:
            from framework.adapters import StudentDropoutAdapter
            adapter = StudentDropoutAdapter()
            bundle = adapter.load(dataset_root=str(ba_root / "datasets" / "StudentDropout"))
            X = bundle.X
            y = bundle.y
            groups = np.array(bundle.group_ids)
            card = {
                "n_samples": len(y),
                "n_features": X.shape[1],
                "n_groups": len(np.unique(groups)),
                "source": "UCI ID 697",
                "features": [f"feat_{i}" for i in range(X.shape[1])],
            }
            return X, y, groups, card
        except Exception:
            self.download()
            # Fallback: simple load
            csv = next(self._ensure_cache_dir().glob("*.csv"))
            df = pd.read_csv(str(csv))
            target_col = [c for c in df.columns if "target" in c.lower() or "status" in c.lower()]
            if not target_col:
                target_col = ["Target"]
            y = df[target_col[0]].values
            drop_cols = target_col + [c for c in df.columns if "id" in c.lower() or "group" in c.lower()]
            groups = df.get("Course", [None] * len(df)).values
            X = df.drop(columns=[c for c in drop_cols if c in df.columns]).select_dtypes(include=["number"]).values
            card = {"n_samples": len(y), "n_features": X.shape[1], "n_groups": len(np.unique(groups)),
                    "source": "UCI ID 697", "features": []}
            return X, y, groups, card
