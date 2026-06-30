"""TAE -- Teaching Assistant Evaluation (UCI ID 100)."""

import numpy as np

from . import DatasetSource, register_source


@register_source
class TAESource(DatasetSource):
    name = "tae"
    display_name = "Teaching Assistant Evaluation"
    version = "1.0"
    source_url = "https://archive.ics.uci.edu/static/public/100/teaching+assistant+evaluation.zip"
    license_info = "CC BY 4.0"
    reference = "Loh (1997); UCI ID 100"
    task = "classification"
    n_samples = 151
    n_features = 4
    n_groups = 25
    grouping_description = "Instructor (25 categories)"

    def download(self):
        import urllib.request
        import zipfile
        import io

        dest_dir = self._ensure_cache_dir()
        data_file = dest_dir / "tae.data"
        if data_file.exists():
            return data_file

        resp = urllib.request.urlopen(self.source_url)
        with zipfile.ZipFile(io.BytesIO(resp.read())) as z:
            z.extractall(str(dest_dir))

        # The zip contains 'tae.data'
        tae_data = dest_dir / "tae.data"
        if tae_data.exists():
            return tae_data
        # Try alternate: rename extracted file
        for f in dest_dir.iterdir():
            if f.suffix == ".data":
                return f
        return dest_dir

    def prepare(self):
        path = self.download()
        raw = np.loadtxt(str(path), delimiter=",")
        # Cols: 0=English, 1=Instructor, 2=Course, 3=Semester, 4=Class size, 5=Target
        X = raw[:, [0, 2, 3, 4]]
        y = raw[:, 5].astype(int)
        groups = raw[:, 1].astype(int).astype(str)
        card = {
            "n_samples": len(y),
            "n_features": X.shape[1],
            "n_groups": len(np.unique(groups)),
            "source": "UCI ID 100",
            "features": ["english_speaker", "course", "semester", "class_size"],
        }
        return X, y, groups, card
