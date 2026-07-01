"""Student Dropout (UCI ID 697).

Download from UCI. Target: Graduate/Dropout (binary, Enrolled excluded).
Group: Course (17 programs).
"""

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
    grouping_description = "Course (17 programs)"

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "student_dropout.csv"
        if csv_path.exists():
            return csv_path
        resp = urllib.request.urlopen(self.source_url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        for f in dest_dir.glob("**/*.csv"):
            if "dropout" in f.name.lower() or "697" in f.name:
                return f
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        df = df[df["Target"] != "Enrolled"].copy()
        y = (df["Target"] == "Graduate").astype(float).values
        groups = df["Course"].astype(str).values
        feat_df = df.drop(columns=["Target"]).select_dtypes(include=[np.number])
        X = feat_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["Course"].nunique(), "source": "UCI ID 697",
                "features": list(feat_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
