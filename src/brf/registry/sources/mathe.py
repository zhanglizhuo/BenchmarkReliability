"""MathE -- Assessing Mathematics Learning in Higher Education (UCI ID 1031)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class MathESource(DatasetSource):
    name = "mathe"
    display_name = "MathE Mathematics Learning"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/1031/dataset+for+assessing+mathematics+learning+in+higher+education.zip"
    license_info = "CC BY 4.0"
    reference = "Azevedo et al. (2024); UCI ID 1031"
    task = "regression"
    n_samples = 833
    n_features = 26
    n_groups = 14
    grouping_description = "Math Topic (14 categories)"
    sha256 = "97844121a1e4cc6b7ad435f9ed6710d84141fc8fe61087df8bc5eb77b22e060c"
    notes = "Question-level aggregation of 9546 student answers."

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        for f in dest_dir.glob("MathE*.csv"):
            return f
        resp = urllib.request.urlopen(self.source_url, timeout=60)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        for f in dest_dir.glob("**/*.csv"):
            return f
        return dest_dir

    def prepare(self):
        import pandas as pd

        path = self.download()
        df = pd.read_csv(str(path), sep=";", encoding="latin-1", engine="python")

        q_agg = (
            df.groupby("Question ID")
            .agg(
                difficulty=("Type of Answer", "mean"),
                n_attempts=("Student ID", "nunique"),
                topic=("Topic", "first"),
                subtopic=("Subtopic", "first"),
                level=("Question Level", "first"),
            )
            .reset_index()
        )
        q_agg["level_int"] = (q_agg["level"] == "Advanced").astype(float)

        subtopic_d = pd.get_dummies(q_agg["subtopic"], prefix="sub", dtype=float)
        X = np.hstack([
            q_agg[["n_attempts", "level_int"]].values.astype(float),
            subtopic_d.values.astype(float),
        ])
        y = q_agg["difficulty"].values
        groups = q_agg["topic"].astype(str).values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": q_agg["topic"].nunique(),
            "source": "UCI ID 1031",
            "features": ["n_attempts", "level_int"] + [f"subtopic_{i}" for i in range(subtopic_d.shape[1])],
        }
        return X, y, groups, card
