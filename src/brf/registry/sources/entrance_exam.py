"""Entrance Exam (UCI ID 582).

Download from UCI, one-hot encode, extract target/features/groups.
"""

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
    sha256 = "6f7545c3876f72c1789b0938eca1ed50cce2da59368621184e1f874f5fa50b10"
    grouping_description = "Qualification board (3: SEBA/CBSE/OTHERS)"

    def download(self):
        import urllib.request, zipfile, io, shutil, pandas as pd
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "student_entrance_582.csv"
        if csv_path.exists():
            return csv_path
        # Try direct UCI URL first
        try:
            resp = urllib.request.urlopen(self.source_url, timeout=60)
            with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
                z.extractall(str(dest_dir))
        except Exception:
            # Fallback: ucimlrepo API
            from ucimlrepo import fetch_ucirepo
            d = fetch_ucirepo(id=582)
            df = d.data.originals
            df.to_csv(str(csv_path), index=False)
            return csv_path
        for f in dest_dir.glob("**/*.csv"):
            if "entrance" in f.name.lower() or "582" in f.name:
                return f
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))

        label_map = {"Average": 0, "Good": 1, "Vg": 2, "Excellent": 3}
        y = df["Performance"].map(label_map).values.astype(float)
        groups = df["Class_ten_education"].astype(str).values

        feat_df = df.drop(columns=["Performance"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values

        card = {
            "n_samples": len(y), "n_features": X.shape[1],
            "n_groups": df["Class_ten_education"].nunique(),
            "source": "UCI ID 582",
            "features": list(X_df.columns)[:10] + [f"... ({X.shape[1]} total)"],
        }
        return X, y, groups, card
