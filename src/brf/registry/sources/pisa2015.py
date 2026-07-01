"""PISA 2015 Science Assessment (OECD).

International student assessment with country-level grouping.
Target: overall science score. Group: Country (73 groups).
"""

import numpy as np

from . import DatasetSource, register_source


@register_source
class PISA2015Source(DatasetSource):
    name = "pisa2015"
    display_name = "PISA 2015 Science"
    version = "1.0"
    source_url = "http://base.ustc.edu.cn/data/pisa2015_science.zip"
    license_info = "OECD Public Use"
    reference = "OECD PISA 2015"
    task = "regression"
    n_samples = 519334
    n_features = 2
    n_groups = 73
    grouping_description = "Country (73 groups)"
    notes = "519K students from 73 countries. Target: overall science accuracy."

    def download(self):
        import urllib.request, zipfile, io
        dest_dir = self._ensure_cache_dir()
        csv_path = dest_dir / "cog_science.csv"
        if csv_path.exists():
            return csv_path

        resp = urllib.request.urlopen(self.source_url, timeout=300)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            for name in z.namelist():
                if name.endswith(".csv"):
                    z.extract(name, str(dest_dir))
                    # File may be nested in subdirectory
                    for f in dest_dir.glob("**/cog_science.csv"):
                        return f
                    for f in dest_dir.glob("**/*.csv"):
                        return f
        return dest_dir

    def prepare(self):
        import csv
        from collections import defaultdict
        from pathlib import Path

        path = self.download()
        if path.is_dir():
            path = next(path.glob("**/*.csv"), path)

        # Parse item-level data, aggregate to student level
        student_scores = defaultdict(list)
        countries = {}

        with open(str(path)) as f:
            reader = csv.reader(f)
            header = next(reader)
            # Find index of first item column
            first_item = 0
            for i, h in enumerate(header):
                if h and "Q" in h and ("DS" in h or "CS" in h):
                    first_item = i
                    break

            for row in reader:
                if len(row) <= first_item:
                    continue
                cntry = row[0].strip().strip("\"'")
                stu = row[1].strip().strip("\"'")
                countries[stu] = cntry
                scores = []
                for j in range(first_item, len(row)):
                    val = row[j].strip().strip("\"'")
                    scores.append(1.0 if val == "Full credit" else 0.0)
                student_scores[stu].extend(scores)

        # Student-level aggregation
        X_list, y_list, g_list = [], [], []
        for stu, scores in student_scores.items():
            if scores:
                X_list.append([len(scores), 1.0])
                y_list.append(np.mean(scores))
                g_list.append(countries.get(stu, "Unknown"))

        X = np.array(X_list)
        y = np.array(y_list)
        groups = np.array(g_list)

        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": len(set(groups)),
            "source": "OECD PISA 2015 (USTC mirror)",
            "features": ["n_items", "intercept"],
        }
        return X, y, groups, card
