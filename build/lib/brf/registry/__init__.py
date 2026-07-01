"""BRF Registry -- Dataset-as-Code benchmark registry.

Part of the benchmark-reliability package (``pip install benchmark-reliability``).

Usage::

    from brf.registry import REGISTRY_SOURCES, list_sources

    for key in list_sources():
        source = REGISTRY_SOURCES[key]
        source.download()
        X, y, groups, card = source.prepare()

CLI::

    python -m brf.registry.cli list
    python -m brf.registry.cli download tae
    python -m brf.registry.cli sync
"""

from .sources import REGISTRY_SOURCES, DatasetSource, list_sources, register_source
from .verify import verify_dataset, verify_all, compute_sha256

__all__ = [
    "REGISTRY_SOURCES",
    "DatasetSource",
    "list_sources",
    "register_source",
    "verify_dataset",
    "verify_all",
    "compute_sha256",
]
