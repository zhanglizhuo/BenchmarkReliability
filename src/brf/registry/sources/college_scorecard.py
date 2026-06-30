"""US College Scorecard (OpenML ID 42121).

Comprehensive US college data with Rich feature set.
Target: admission rate. Group: State (59 groups).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class CollegeScorecardSource(DatasetSource):
    name = "college_scorecard"
    display_name = "US College Scorecard"
    version = "1.0"
    source_url = "https://www.openml.org/search?type=data&id=42121"
    license_info = "Public Domain (OpenML)"
    reference = "US Dept of Education; OpenML ID 42121"
    task = "regression"
    n_samples = 2220  # 7804 in source, filtered to 2220 with admission_rate
    n_features = 30   # 40 in source, 30 numeric after filtering
    n_groups = 55  # 59 states in source, 55 after filtering for admission_rate
    grouping_description = "US State (59 groups)"
    sha256 = "d4dca5f3d35fba46a164a1e8a59c35d643a89cbc25a216431a44913dd4cf5e00"
    notes = "7804 US colleges. Target: admission rate."

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "college_scorecard.csv"
        if csv_path.exists():
            return csv_path

        import openml
        import pandas as pd

        ds = openml.datasets.get_dataset(42121)
        X, y, _, _ = ds.get_data(dataset_format="dataframe")
        X.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path), low_memory=False)

        id_cols = ["school_name", "city", "zip", "school_webpage", "latitude", "longitude",
                   "state"]
        target_col = "admission_rate"

        # Filter rows with valid target
        mask = df[target_col].notna()
        df = df[mask].copy()
        df[target_col] = df[target_col].astype(float)

        y = df[target_col].values

        # Feature columns: numeric, exclude ID cols and target
        feat_cols = [
            c for c in df.columns
            if c not in id_cols and c != target_col
        ]
        X_feat = df[feat_cols].select_dtypes(include=[np.number]).fillna(0)
        X = X_feat.values.astype(float)
        groups = df["state"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["state"].nunique(),
            "source": "OpenML ID 42121 (US College Scorecard)",
            "features": list(X_feat.columns),
        }
        return X, y, groups, card
