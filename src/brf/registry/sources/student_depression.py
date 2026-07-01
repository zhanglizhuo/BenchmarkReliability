"""Student Depression Dataset (OpenML ID 46753).

Mental health survey of students across Indian cities.
Target: depression (binary). Group: City (30 groups).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class StudentDepressionSource(DatasetSource):
    name = "student_depression"
    display_name = "Student Depression Survey"
    version = "1.0"
    source_url = "https://www.openml.org/search?type=data&id=46753"
    license_info = "Public Domain (OpenML)"
    reference = "Student Depression Dataset; OpenML ID 46753"
    task = "classification"
    n_samples = 27875
    n_features = 21
    n_groups = 30
    grouping_description = "City (30 groups, Indian cities)"
    sha256 = "d18d7476eec0f3f1352dd3cdf1ade52dbe9084cc8c523d3c8aa22f9d7248957a"
    notes = "27.9K students. Target: depression (binary). Run as regression."

    def download(self):
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "student_depression.csv"
        if csv_path.exists():
            return csv_path

        import openml
        import pandas as pd

        ds = openml.datasets.get_dataset(46753)
        X, y, _, _ = ds.get_data(dataset_format="dataframe")
        df = pd.concat([X, y], axis=1) if y is not None else X.copy()
        df.to_csv(str(csv_path), index=False)
        return csv_path

    def prepare(self):
        import pandas as pd
        import sys

        path = self.download()
        df = pd.read_csv(str(path), low_memory=False)

        # Decode bytes-only columns
        for col in df.select_dtypes([object]).columns:
            sample = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else None
            if sample is not None and isinstance(sample, bytes):
                df[col] = df[col].str.decode("utf-8")

        # Target
        y = df["Depression"].astype(float).values

        # Filter cities >= 5
        city_counts = df["City"].value_counts()
        valid = city_counts[city_counts >= 5].index
        df = df[df["City"].isin(valid)].copy()
        y = df["Depression"].astype(float).values

        # Numeric features
        num_cols = ["Age", "Academic Pressure", "CGPA", "Study Satisfaction",
                    "Work/Study Hours", "Financial Stress"]
        X_num = df[num_cols].fillna(0).values.astype(float)

        # Categorical (one-hot, exclude City/Profession/Degree)
        dummy_list = [X_num]
        for col in df.select_dtypes([object]).columns:
            if col in ("City", "Profession", "Degree", "Depression"):
                continue
            d = pd.get_dummies(df[col], prefix=col[:4], dtype=float)
            dummy_list.append(d.values.astype(float))

        X = np.hstack(dummy_list)
        groups = df["City"].values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": df["City"].nunique(),
            "source": "OpenML ID 46753",
            "features": num_cols + [f"cat_{i}" for i in range(X.shape[1] - len(num_cols))],
        }
        return X, y, groups, card
