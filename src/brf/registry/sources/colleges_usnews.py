"""Colleges US News Rankings (OpenML ID 538).

US News & World Report college ranking data.
Target: Graduation rate. Group: US State (51 groups).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class CollegesUSNewsSource(DatasetSource):
    name = "colleges_usnews"
    display_name = "Colleges US News Rankings"
    version = "1.0"
    source_url = "https://www.openml.org/data/download/22101655/colleges_usnews.arff"
    license_info = "Public Domain (OpenML)"
    reference = "US News College Rankings (OpenML ID 538)"
    task = "regression"
    n_samples = 1204
    n_features = 31
    n_groups = 51
    grouping_description = "US State (51 groups)"
    notes = "1204 US colleges. Target: graduation rate."

    def download(self):
        from pathlib import Path
        dest_dir = self._ensure_cache_dir()
        arff_path = dest_dir / "colleges_usnews.arff"
        if arff_path.exists():
            return arff_path

        # Try OpenML API first (faster for large files)
        try:
            import openml
            ds = openml.datasets.get_dataset(538)
            X, y, _, _ = ds.get_data(dataset_format='dataframe')
            import pandas as pd
            df = pd.concat([X, y], axis=1) if y is not None else X.copy()
            df.to_csv(dest_dir / "colleges_usnews.csv", index=False)
            return dest_dir / "colleges_usnews.csv"
        except Exception:
            pass

        # Fallback: direct ARFF download
        import urllib.request
        urllib.request.urlretrieve(self.source_url, str(arff_path))
        return arff_path

    def prepare(self):
        from scipy.io import arff
        import pandas as pd

        path = self.download()

        if path.suffix == ".csv":
            df = pd.read_csv(str(path))
        else:
            data, meta = arff.loadarff(str(path))
            df = pd.DataFrame(data)
            for col in df.select_dtypes([object]).columns:
                df[col] = df[col].str.decode("utf-8") if hasattr(df[col], "str") else df[col]

        target_col = "Graduation_rate"
        mask = df[target_col].notna() & (df[target_col] != "")
        df = df[mask].copy()
        df[target_col] = df[target_col].astype(float)

        y = df[target_col].values

        exclude = ["State", target_col]
        feat_cols = [c for c in df.columns if c not in exclude]
        X_feat = df[feat_cols].select_dtypes(include=[np.number]).fillna(0)
        X = X_feat.values.astype(float)
        groups = df["State"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["State"].nunique(),
            "source": "OpenML ID 538 (US News)",
            "features": list(X_feat.columns),
        }
        return X, y, groups, card
