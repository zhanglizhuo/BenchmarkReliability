"""Turkiye Student Evaluation (UCI ID 262)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class TurkiyeSource(DatasetSource):
    name = "turkiye"
    display_name = "Turkiye Student Evaluation"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/262/turkiye+student+evaluation.zip"
    license_info = "CC BY 4.0"
    reference = "Gazi University; UCI ID 262"
    task = "regression"
    n_samples = 5820
    n_features = 28
    n_groups = 13
    grouping_description = "Course (13 categories)"

    def download(self):
        import urllib.request
        import zipfile
        import io
        import shutil

        dest_dir = self._ensure_cache_dir()
        csv_file = dest_dir / "turkiye-student-evaluation_generic.csv"
        if csv_file.exists():
            return csv_file

        resp = urllib.request.urlopen(self.source_url)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            for name in z.namelist():
                if "generic" in name.lower() and name.endswith(".csv"):
                    with z.open(name) as src, open(csv_file, "wb") as dst:
                        shutil.copyfileobj(src, dst)
                    return csv_file
            # Fallback: extract everything
            z.extractall(str(dest_dir))
        for f in dest_dir.glob("*generic*.csv"):
            return f
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        q_cols = [f"Q{i}" for i in range(1, 29)]
        X = df[q_cols].values.astype(float)
        y = df["difficulty"].values.astype(int)
        groups = df["class"].astype(str).values
        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["class"].nunique(),
            "source": "UCI ID 262",
            "features": q_cols,
        }
        return X, y, groups, card
