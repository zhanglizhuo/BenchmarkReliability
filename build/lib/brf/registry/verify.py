"""BRF Registry -- SHA256 verification for downloaded datasets.

Each dataset source can declare an expected SHA-256 hash.  This module
provides helpers to verify and compute hashes.

Usage::

    from registry.verify import verify_dataset, compute_sha256

    ok = verify_dataset("tae")
    sha = compute_sha256("/path/to/file")
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Optional

from .sources import REGISTRY_SOURCES


def compute_sha256(path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()


def verify_dataset(key: str) -> Optional[bool]:
    """Verify a single dataset's downloaded file(s).

    Returns:
        True if hash matches, False if mismatch, None if no hash defined
        or dataset not found.
    """
    source = REGISTRY_SOURCES.get(key)
    if source is None:
        print(f"Dataset '{key}' not found.")
        return None

    if not source.sha256:
        print(f"Dataset '{key}' has no SHA-256 checksum defined.")
        return None

    path = source.download()
    if isinstance(path, Path) and path.is_dir():
        print(f"Dataset '{key}' is a directory; skipping hash check.")
        return True

    actual = compute_sha256(path) if isinstance(path, Path) else "N/A"
    expected = source.sha256

    if actual == expected:
        print(f"  OK: {key} sha256={actual[:16]}...")
        return True
    else:
        print(f"  MISMATCH: {key}")
        print(f"    expected: {expected[:32]}...")
        print(f"    actual:   {actual[:32]}...")
        return False


def verify_all() -> dict:
    """Verify all registered datasets. Returns {key: bool_or_None}."""
    from .sources import list_sources

    results = {}
    for key in list_sources():
        results[key] = verify_dataset(key)
    return results
