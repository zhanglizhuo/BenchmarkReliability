"""OLI Engineering Statics 2011 (CMU PSLC DataShop).

Student-step level data from CMU Open Learning Initiative.
Target: first attempt correctness. Group: curriculum module (19 groups).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class OLISource(DatasetSource):
    name = "oli"
    display_name = "OLI Engineering Statics 2011"
    version = "1.0"
    source_url = "http://base.ustc.edu.cn/data/OLI_data.zip"
    license_info = "Public research data (PSLC DataShop)"
    reference = "CMU OLI; PSLC DataShop"
    task = "classification"
    n_samples = 194947
    n_features = 2
    n_groups = 19
    grouping_description = "Curriculum module (19 groups)"
    sha256 = "8ba76de29f34cf9ffbbb6ef49b83875a6971af25a449a066da6371257edd99d9"
    notes = "Engineering Statics course. Step-level prediction."

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "AllData_student_step_2011F.csv"
        if csv_path.exists():
            return csv_path

        # Try USTC mirror first
        try:
            resp = urllib.request.urlopen(self.source_url, timeout=120)
            with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
                z.extractall(str(dest_dir))
            for f in dest_dir.glob("**/*student_step*.csv"):
                return f
        except Exception:
            pass

        # Fallback: try /tmp/oli/ if already downloaded
        import os
        alt = "/tmp/oli/AllData_student_step_2011F.csv"
        if os.path.exists(alt):
            import shutil
            shutil.copy(alt, str(csv_path))
            return csv_path

        return dest_dir

    def prepare(self):
        import pandas as pd
        import os

        path = self.download()
        if path.is_dir():
            raise FileNotFoundError(f"OLI data not found. Download from {self.source_url}")

        df = pd.read_csv(str(path), encoding="latin-1")

        # Extract module from Problem Hierarchy
        df["module"] = df["Problem Hierarchy"].str.split(",", expand=True)[2].str.strip()

        # Binary target: first attempt correct
        df["correct"] = (df["First Attempt"] == "correct").astype(float)

        # Features: past-performance metrics (no leakage)
        feat_cols = ["Opportunity (F2011)", "Predicted Error Rate (F2011)"]
        for c in feat_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        X = df[feat_cols].fillna(0).values.astype(float)
        y = df["correct"].values.astype(float)
        groups = df["module"].values

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": len(np.unique(groups)),
            "source": "CMU OLI / PSLC DataShop",
            "features": feat_cols,
        }
        return X, y, groups, card
