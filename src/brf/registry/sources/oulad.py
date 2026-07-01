"""OULAD (Open University Learning Analytics Dataset).

Download from UCI mirror (ID 349). Multi-file join.
Target: final_result (pass: 1, fail/withdrawn: 0).
Group: code_module_code_presentation (22 combinations).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class OULADSource(DatasetSource):
    name = "oulad"
    display_name = "Open University Learning Analytics Dataset"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/349/open+university+learning+analytics+dataset.zip"
    license_info = "CC BY-SA 4.0"
    reference = "Kuzilek et al. (2017); UCI ID 349"
    task = "classification"
    n_samples = 32593
    n_features = 44
    n_groups = 22
    sha256 = "9ce92381e4a0ac457f8e251b2eb2c179ed51e023ab30d1d671a0268bd62316ba"
    grouping_description = "Course module + presentation (22)"

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        info_path = dest_dir / "studentInfo.csv"
        if info_path.exists():
            return dest_dir
        resp = urllib.request.urlopen(self.source_url, timeout=300)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))
        return dest_dir

    def prepare(self):
        import pandas as pd

        root = self.download()
        info = pd.read_csv(str(root / "studentInfo.csv"))

        # Aggregate VLE data
        vle = pd.read_csv(str(root / "studentVle.csv"), low_memory=False)
        vle_agg = vle.groupby(["code_module", "code_presentation", "id_student"]).agg(
            sum_click=("sum_click", "sum"), n_visits=("date", "count")
        ).reset_index()

        # Aggregate assessments
        try:
            ass = pd.read_csv(str(root / "studentAssessment.csv"), low_memory=False)
            ass_agg = ass.groupby(["id_student"]).agg(
                n_assessments=("id_assessment", "count"),
                avg_score=("score", "mean"),
                std_score=("score", "std"),
            ).fillna(0).reset_index()
        except Exception:
            ass_agg = pd.DataFrame(columns=["id_student", "n_assessments", "avg_score", "std_score"])

        # Merge
        info = info.merge(vle_agg, on=["code_module", "code_presentation", "id_student"], how="left")
        if not ass_agg.empty:
            info = info.merge(ass_agg, on="id_student", how="left")

        # Target: pass=1, fail/withdrawn=0
        info["target"] = (info["final_result"].isin(["Pass", "Distinction"])).astype(float)
        y = info["target"].values

        # Group
        info["group"] = info["code_module"].astype(str) + "_" + info["code_presentation"].astype(str)
        groups = info["group"].values

        # Features
        feat_cols = [c for c in info.select_dtypes(include=[np.number]).columns
                     if c not in ["target"]]
        X_feat = info[feat_cols].fillna(0).values.astype(float)

        # One-hot categorical
        cat_cols = [c for c in info.select_dtypes(include=["object"]).columns
                    if c not in ["final_result", "group", "id_student"]]
        if cat_cols:
            cat_df = pd.get_dummies(info[cat_cols], columns=cat_cols, dummy_na=False)
            X = np.hstack([X_feat, cat_df.fillna(0).values.astype(float)])
        else:
            X = X_feat

        card = {"n_samples": len(y), "n_features": X.shape[1],
                "n_groups": info["group"].nunique(), "source": "UCI ID 349 (OULAD)",
                "features": feat_cols + [f"cat_{i}" for i in range(len(cat_cols))]}
        return X, y, groups, card
