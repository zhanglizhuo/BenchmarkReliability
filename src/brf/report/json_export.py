import json


def export_json(brf_vector: dict, filepath: str) -> None:
    with open(filepath, "w") as f:
        json.dump(brf_vector, f, indent=2, ensure_ascii=False)
