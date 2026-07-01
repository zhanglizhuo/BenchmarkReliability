"""ASSISTments 2009-2010 Skill Builder (corrected).

Data sourced from USTC datashop mirror.
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class ASSISTmentsSource(DatasetSource):
    name = "assistments"
    display_name = "ASSISTments 2009-2010"
    version = "1.0"
    source_url = "http://base.ustc.edu.cn/data/ASSISTment/2009_skill_builder_data_corrected.zip"
    fallback_urls = ["https://pslcdatashop.web.cmu.edu/DatasetInfo?datasetId=74"]
    license_info = "Public research data"
    reference = "Feng, Heffernan & Koedinger (2009)"
    task = "regression"
    n_samples = 3729
    n_features = 5
    n_groups = 124
    grouping_description = "Teacher (124 categories)"
    sha256 = "1aa296e00b6c88c4d6fad4ca2ae4866484d9fe5484f38f5c8c94dfc49f045e08"
    notes = "Student-level aggregates of 401K transactions."

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_file = dest_dir / "skill_builder_data_corrected.csv"
        if csv_file.exists():
            return csv_file

        urls = [self.source_url] + self.fallback_urls
        for url in urls:
            try:
                resp = urllib.request.urlopen(url, timeout=120)
                with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
                    z.extractall(str(dest_dir))
                for f in dest_dir.iterdir():
                    if f.suffix == ".csv" and "skill" in f.name.lower():
                        return f
                break
            except Exception:
                continue
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path), encoding="ISO-8859-15", low_memory=False)
        df = df[df["original"] == 1].copy()

        agg = (
            df.groupby("user_id")
            .agg(
                n_problems=("correct", "count"),
                mean_correct=("correct", "mean"),
                mean_attempt=("attempt_count", "mean"),
                mean_hint=("hint_count", "mean"),
                median_response_ms=("ms_first_response", "median"),
                n_skills=("skill_id", "nunique"),
                teacher_id=("teacher_id", "first"),
            )
            .reset_index()
        )
        agg = agg[agg["n_problems"] >= 5].copy()

        feat_cols = ["n_problems", "mean_attempt", "mean_hint", "median_response_ms", "n_skills"]
        X = agg[feat_cols].values.astype(float)
        X[:, 3] = np.log1p(X[:, 3])
        y = agg["mean_correct"].values
        groups = agg["teacher_id"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": len(feat_cols),
            "n_groups": agg["teacher_id"].nunique(),
            "source": "ASSISTments 2009-2010 (USTC datashop)",
            "features": feat_cols + ["log_response_ms"],
        }
        return X, y, groups, card
