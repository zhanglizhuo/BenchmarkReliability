"""Colleges AAUP -- Faculty Salary Survey (OpenML ID 488)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class CollegesAAUPSource(DatasetSource):
    name = "colleges_aaup"
    display_name = "AAUP College Faculty Salary"
    version = "1.0"
    source_url = "https://www.openml.org/search?type=data&id=488"
    license_info = "Public Domain (OpenML)"
    reference = "AAUP Faculty Salary Survey (OpenML ID 488)"
    task = "regression"
    n_samples = 1161
    n_features = 9
    n_groups = 52
    grouping_description = "US State (52 groups)"
    sha256 = "5eafc5406a35b84887cd3bd13721615fbb73e33cf304b77bfbe38b5e16668ace"
    notes = "1161 US colleges. Institutional-level prediction."

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "colleges_aaup.csv"
        if csv_path.exists():
            return csv_path

        import openml
        import pandas as pd

        ds = openml.datasets.get_dataset(488)
        X, y, _, _ = ds.get_data(dataset_format="dataframe")
        X.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))

        target_col = "Average_salary-all_ranks"
        y = df[target_col].values.astype(float)

        type_d = pd.get_dummies(df["Type"], prefix="type", dtype=float)
        faculty_cols = [c for c in df.columns if c.startswith("Number_of")]
        X = np.hstack([type_d.values.astype(float), df[faculty_cols].values.astype(float)])
        groups = df["State"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["State"].nunique(),
            "source": "OpenML ID 488 (AAUP)",
            "features": list(type_d.columns) + faculty_cols,
        }
        return X, y, groups, card
