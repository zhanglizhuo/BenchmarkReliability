"""BRF Registry CLI -- download, verify, and prepare datasets.

Usage::

    # List all datasets
    python -m registry.cli list

    # Download a dataset (with verification)
    python -m registry.cli download tae
    python -m registry.cli download --all

    # Verify checksums
    python -m registry.cli verify tae
    python -m registry.cli verify --all

    # Sync (download + verify all)
    python -m registry.cli sync

    # Show metadata
    python -m registry.cli info tae
"""

from __future__ import annotations

import argparse
from pathlib import Path

import sys

from .sources import REGISTRY_SOURCES, list_sources
from .verify import verify_dataset, verify_all


def cmd_list():
    """List all registered datasets."""
    print(f"BRF Registry -- {len(list_sources())} datasets\n")
    for key in list_sources():
        source = REGISTRY_SOURCES[key]
        print(f"  {key:<20} {source.display_name:<45} "
              f"N={source.n_samples:>5d}  G={source.n_groups:>4d}")


def cmd_download(key: str = None, all_: bool = False):
    """Download dataset(s)."""
    if all_:
        keys = list_sources()
    elif key:
        keys = [key]
    else:
        print("Usage: download <key> or download --all")
        return

    for k in keys:
        source = REGISTRY_SOURCES.get(k)
        if source is None:
            print(f"  Unknown dataset: {k}")
            continue
        print(f"Downloading {k} ({source.display_name})...")
        try:
            path = source.download()
            print(f"  -> {path}")
            # Verify after download
            if source.sha256:
                ok = source._check_sha256(path) if isinstance(path, Path) else True
                if not ok:
                    print(f"  WARNING: SHA-256 mismatch!")
        except Exception as e:
            print(f"  FAILED: {e}")


def cmd_verify(key: str = None, all_: bool = False):
    """Verify dataset checksums."""
    if all_:
        verify_all()
    elif key:
        verify_dataset(key)
    else:
        print("Usage: verify <key> or verify --all")


def cmd_sync():
    """Download + verify all datasets."""
    print("Syncing all datasets...")
    for key in list_sources():
        source = REGISTRY_SOURCES[key]
        print(f"\n  [{key}] {source.display_name}")
        try:
            path = source.download()
            print(f"    Downloaded to {path}")
            if source.sha256:
                ok = source._check_sha256(path) if isinstance(path, Path) else True
                print(f"    Checksum: {'OK' if ok else 'FAIL'}")
        except Exception as e:
            print(f"    FAILED: {e}")


def cmd_info(key: str):
    """Show dataset metadata."""
    source = REGISTRY_SOURCES.get(key)
    if source is None:
        print(f"Unknown dataset: {key}")
        return
    meta = source.metadata()
    for k, v in meta.items():
        print(f"  {k}: {v}")


def main():
    parser = argparse.ArgumentParser(description="BRF Registry CLI")
    sub = parser.add_subparsers(dest="command", help="Command")

    sub.add_parser("list", help="List all datasets")

    dl = sub.add_parser("download", help="Download dataset(s)")
    dl.add_argument("key", nargs="?", help="Dataset key")
    dl.add_argument("--all", action="store_true", help="Download all")

    vf = sub.add_parser("verify", help="Verify checksums")
    vf.add_argument("key", nargs="?", help="Dataset key")
    vf.add_argument("--all", action="store_true", help="Verify all")

    sub.add_parser("sync", help="Download + verify all datasets")

    info = sub.add_parser("info", help="Show dataset metadata")
    info.add_argument("key", help="Dataset key")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "download":
        cmd_download(key=args.key, all_=args.all)
    elif args.command == "verify":
        cmd_verify(key=args.key, all_=args.all)
    elif args.command == "sync":
        cmd_sync()
    elif args.command == "info":
        cmd_info(args.key)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
