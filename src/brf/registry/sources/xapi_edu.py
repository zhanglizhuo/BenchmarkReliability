"""xAPI-Edu-Data (Kalboard 360).

Download from UCI mirror. Target: Class (L/M/H, ordinal).
Group: Topic (12 subjects).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class XAPIEduSource(DatasetSource):
    name = "xapi_edu"
    display_name = "xAPI-Edu-Data"
    version = "1.0"
    source_url = "https://www.kaggle.com/datasets/aljarah/xAPI-Edu-Data"
    fallback_urls = ["https://archive.ics.uci.edu/dataset/511/xapi-edu-data"]
    license_info = "CC BY-SA 4.0"
    reference = "Amrieh et al. (2016)"
    task = "classification"
    n_samples = 480
    n_features = 72
    n_groups = 12
    sha256 = "ca48b2373f389b32d57b62293f3930f82a3d93eb7f84457940df69208e2edade"
    grouping_description = "Topic (12 subjects)"

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "xAPI-Edu-Data.csv"
        if csv_path.exists():
            return csv_path
        # Try UCI mirror (more accessible than Kaggle)
        urls = self.fallback_urls + [self.source_url]
        for url in urls:
            try:
                resp = urllib.request.urlopen(url, timeout=60)
                with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
                    z.extractall(str(dest_dir))
                for f in dest_dir.glob("**/*.csv"):
                    if "xapi" in f.name.lower() or "edu" in f.name.lower():
                        return f
                break
            except Exception:
                continue
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        label_map = {"L": 0, "M": 1, "H": 2}
        y = df["Class"].map(label_map).values.astype(float)
        groups = df["Topic"].astype(str).values
        feat_df = df.drop(columns=["Class"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values
        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["Topic"].nunique(),
                "source": "Kaggle / Kalboard 360",
                "features": list(X_df.columns)[:8] + [f"... ({X.shape[1]} total)"]}
        return X, y, groups, card
