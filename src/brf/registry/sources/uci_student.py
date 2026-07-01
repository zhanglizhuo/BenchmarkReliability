"""UCI Student Performance (UCI ID 320).

Download from UCI. Target: G3 (final grade 0-20). Group: school (GP/MS).
G1 and G2 excluded as trivially predictive.
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class UCIStudentSource(DatasetSource):
    name = "uci_student"
    display_name = "UCI Student Performance"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/320/student+performance.zip"
    license_info = "CC BY 4.0"
    reference = "Cortez & Silva (2008); UCI ID 320"
    task = "regression"
    n_samples = 649
    n_features = 56
    n_groups = 2
    sha256 = "a7594a11d7771c0efe1a740824e0e833da9c4cad07c39a9766a874575563fb3f"
    grouping_description = "School (2: GP/MS)"

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "student-por.csv"
        if csv_path.exists():
            return csv_path
        resp = urllib.request.urlopen(self.source_url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        for f in dest_dir.glob("**/*.csv"):
            if "por" in f.name.lower():
                return f
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path), sep=";")
        y = df["G3"].values.astype(float)
        groups = df["school"].astype(str).values
        feat_df = df.drop(columns=["G1", "G2", "G3"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["school"].nunique(), "source": "UCI ID 320",
                "features": list(X_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
