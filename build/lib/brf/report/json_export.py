import json


def export_json(brf_vector: dict, filepath: str) -> None:
    if any(v is None for v in brf_vector.values()):
        raise ValueError("BRF vector contains None values; call fit() first")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(brf_vector, f, indent=2, ensure_ascii=False)
