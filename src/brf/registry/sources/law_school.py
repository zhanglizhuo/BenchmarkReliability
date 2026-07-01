"""Law School Admission (OpenML ID 43889).

Predict bar exam passage from admission characteristics.
Target: bar exam pass. Group: cluster (6 law school tiers).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class LawSchoolSource(DatasetSource):
    name = "law_school"
    display_name = "Law School Admission"
    version = "1.0"
    source_url = "https://www.openml.org/search?type=data&id=43889"
    license_info = "Public Domain (OpenML)"
    reference = "LSAC; OpenML ID 43889"
    task = "classification"
    n_samples = 20800
    n_features = 7
    n_groups = 6
    grouping_description = "Cluster (6 groups)"
    notes = "20.8K law school applicants. Target: bar exam passage."

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "law_school.csv"
        if csv_path.exists():
            return csv_path
        import openml
        ds = openml.datasets.get_dataset(43889)
        X, _, _, _ = ds.get_data(dataset_format="dataframe")
        X.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))

        # Target: bar exam pass (binary)
        y = (df["bar"].astype(str).str.upper() == "TRUE").astype(float).values

        # Features: numeric admission predictors
        feat_cols = ["age", "decile1", "decile3", "fam_inc", "lsat", "ugpa", "fulltime"]
        for c in feat_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        X = df[feat_cols].fillna(0).values.astype(float)

        groups = df["cluster"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["cluster"].nunique(),
            "source": "OpenML ID 43889",
            "features": feat_cols,
        }
        return X, y, groups, card
