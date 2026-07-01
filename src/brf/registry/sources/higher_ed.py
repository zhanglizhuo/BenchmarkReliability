"""Higher Education Students Performance (UCI ID 856).

Download from UCI, one-hot encode. Target: OUTPUT Grade (0-7).
Group: Course ID (9 groups).
"""

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
    grouping_description = "Course ID (9 courses)"

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "higher_ed_856.csv"
        if csv_path.exists():
            return csv_path
        resp = urllib.request.urlopen(self.source_url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        for f in dest_dir.glob("**/*.csv"):
            if "higher" in f.name.lower() or "856" in f.name:
                return f
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        y = df["OUTPUT Grade"].values.astype(float)
        groups = df["Course ID"].astype(str).values
        feat_df = df.drop(columns=["OUTPUT Grade"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["Course ID"].nunique(), "source": "UCI ID 856",
                "features": list(X_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
