"""BRF Benchmark Registry -- Dataset-as-Code framework.

Each dataset is a Python module in this directory implementing a DatasetSource
subclass with ``@register_source``.  Modules are auto-discovered on first import.

Architecture:
  Layer 1: metadata    (name, version, source, license, sha256, etc.)
  Layer 2: download    (get from public source, verify checksum)
  Layer 3: prepare     (return X, y, groups ready for BRF)

Example::

    from registry.sources import REGISTRY_SOURCES

    source = REGISTRY_SOURCES["tae"]
    source.download()
    source.verify()
    X, y, groups, meta = source.prepare()
"""

from __future__ import annotations

import importlib
import os

import hashlib
import json
import logging
import shutil
import subprocess
import sys
import tempfile
import zipfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.request import urlretrieve

import numpy as np

logger = logging.getLogger("brf.registry")

# ---- config ----

_CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
_CACHE_DIR.mkdir(parents=True, exist_ok=True)


# ---- base class ----


class DatasetSource(ABC):
    """Abstract base for a BRF Registry dataset source.

    Subclasses must define class-level metadata and implement :meth:`download`,
    :meth:`verify`, and :meth:`prepare`.
    """

    # -- Layer 1: metadata (override in subclasses) --

    name: str = ""
    """Canonical key (e.g. ``"tae"``)."""

    display_name: str = ""
    """Human-readable name (e.g. ``"Teaching Assistant Evaluation"``)."""

    version: str = "1.0"
    """Dataset version (independent of Registry version)."""

    source_url: str = ""
    """Primary download URL."""

    fallback_urls: List[str] = []
    """Alternative download URLs if primary is unreachable."""

    license_info: str = "TBD"
    """License string (e.g. ``"CC BY 4.0"``)."""

    reference: str = ""
    """Citation / paper reference."""

    task: str = "regression"
    """``"regression"`` or ``"classification"``."""

    n_samples: int = 0
    n_features: int = 0
    n_groups: int = 0

    sha256: str = ""
    """SHA-256 checksum of the primary downloaded file (if applicable)."""

    grouping_description: str = ""
    """What the grouping variable represents (e.g. ``"instructor"``)."""

    notes: str = ""

    # -- Layer 2: download / verify --

    def _cache_path(self, filename: str) -> Path:
        return _CACHE_DIR / f"{self.name}" / filename

    def _ensure_cache_dir(self) -> Path:
        p = _CACHE_DIR / self.name
        p.mkdir(parents=True, exist_ok=True)
        return p

    @staticmethod
    def _download_url(url: str, dest: Path, timeout: int = 120) -> Path:
        """Download a file from *url* to *dest* with progress indication."""
        logger.info("Downloading %s -> %s", url, dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        urlretrieve(url, str(dest))
        return dest

    @staticmethod
    def _compute_sha256(path: Path) -> str:
        sha = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha.update(chunk)
        return sha.hexdigest()

    def _check_sha256(self, path: Path) -> bool:
        if not self.sha256:
            return True
        actual = self._compute_sha256(path)
        ok = actual == self.sha256
        if not ok:
            logger.error(
                "SHA256 mismatch for %s: expected %s, got %s",
                path, self.sha256[:16], actual[:16],
            )
        return ok

    @abstractmethod
    def download(self) -> Path:
        """Download the raw dataset, return path to downloaded file/directory."""

    def verify(self, path: Optional[Path] = None) -> bool:
        """Verify integrity (checksum, file existence).
        
        Default implementation checks SHA-256 if ``self.sha256`` is set.
        """
        if path is None:
            path = self.download()
        if path.is_dir():
            return True
        return self._check_sha256(path)

    # -- Layer 3: prepare (BRF-ready format) --

    @abstractmethod
    def prepare(self) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray], Dict[str, Any]]:
        """Return (X, y, groups, metadata_card).

        Returns
        -------
        X : np.ndarray
            Feature matrix (N, p).
        y : np.ndarray
            Target vector (N,).
        groups : np.ndarray or None
            Group labels (N,) or ``None`` if no grouping.
        metadata_card : dict
            At minimum contains ``n_samples``, ``n_features``, ``n_groups``,
            ``source``, ``features``.
        """

    def metadata(self) -> Dict[str, Any]:
        """Return full Layer-1 metadata as a dict (for serialization)."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "version": self.version,
            "source_url": self.source_url,
            "license": self.license_info,
            "reference": self.reference,
            "task": self.task,
            "n_samples": self.n_samples,
            "n_features": self.n_features,
            "n_groups": self.n_groups,
            "sha256": self.sha256,
            "grouping": self.grouping_description,
            "notes": self.notes,
        }


# ---- registry ----

REGISTRY_SOURCES: Dict[str, DatasetSource] = {}
"""Global dict mapping dataset key -> DatasetSource instance."""


def register_source(source_cls_or_instance) -> DatasetSource:
    """Register a DatasetSource class or instance."""
    if isinstance(source_cls_or_instance, type):
        instance = source_cls_or_instance()
    else:
        instance = source_cls_or_instance
    REGISTRY_SOURCES[instance.name] = instance
    return instance


def list_sources() -> List[str]:
    """Return sorted list of registered dataset keys."""
    return sorted(REGISTRY_SOURCES.keys())


# ---- auto-discovery ----

_MODULE_DIR = os.path.dirname(__file__)
for _fn in sorted(os.listdir(_MODULE_DIR)):
    if _fn.startswith("_") or _fn == "README" or not _fn.endswith(".py"):
        continue
    _modname = _fn[:-3]
    importlib.import_module(f".{_modname}", package=__package__ if __package__ else "registry.sources")
