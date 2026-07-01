"""Students Exam Scores (Kaggle).

30,641 US high school students. Target: math score.
Group: EthnicGroup (5 groups).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class StudentsExamScoresSource(DatasetSource):
    name = "students_exam_scores"
    display_name = "Students Exam Scores (Kaggle)"
    version = "1.0"
    source_url = "https://www.kaggle.com/datasets/desalegngeb/students-exam-scores"
    license_info = "CC0 (Kaggle)"
    reference = "Kaggle: Students Exam Scores"
    task = "regression"
    n_samples = 30641
    n_features = 14
    n_groups = 5
    sha256 = "e08f2f4d11f9187c685d84eabd3dee72bbf0e514e940bff3bfacf341ee43f71d"
    grouping_description = "Ethnic group (5 groups)"

    def download(self):
        import os, shutil
        from pathlib import Path
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "exam_scores.csv"
        if csv_path.exists():
            return csv_path
        
        os.environ.setdefault('HTTP_PROXY', 'http://Clash:meO8PQ5J@192.168.1.234:7890')
        os.environ.setdefault('HTTPS_PROXY', 'http://Clash:meO8PQ5J@192.168.1.234:7890')
        
        import kagglehub
        path = Path(kagglehub.dataset_download("desalegngeb/students-exam-scores"))
        for f in path.glob("*.csv"):
            if "Original" in f.name:
                shutil.copy(str(f), str(csv_path))
                return csv_path
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path))
        # Drop unnamed index column
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])

        y = df["MathScore"].values.astype(float)
        groups = df["EthnicGroup"].astype(str).values

        feat_df = df.drop(columns=["MathScore", "ReadingScore", "WritingScore"])
        cat_cols = feat_df.select_dtypes(include=["object"]).columns.tolist()
        X_df = pd.get_dummies(feat_df, columns=cat_cols, dummy_na=False)
        X = X_df.fillna(0).astype(float).values

        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": df["EthnicGroup"].nunique(),
                "source": "Kaggle", "features": list(X_df.columns)}
        return X, y, groups, card
