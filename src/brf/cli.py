"""BRF CLI -- Benchmark Reliability Framework command-line interface.

Usage::

    brf audit dataset.csv           # Run BRF on a dataset
    brf registry list               # List registered datasets
    brf registry sync               # Download + verify all datasets
    brf registry info oulad         # Show dataset metadata
"""

from __future__ import annotations

import argparse
import sys


def _registry_cli(args):
    """Dispatch to registry subcommand."""
    from .registry.cli import (
        cmd_list, cmd_download, cmd_verify, cmd_sync, cmd_info,
    )
    if args.registry_cmd == "list":
        cmd_list()
    elif args.registry_cmd == "download":
        cmd_download(key=args.key, all_=args.all)
    elif args.registry_cmd == "verify":
        cmd_verify(key=args.key, all_=args.all)
    elif args.registry_cmd == "sync":
        cmd_sync()
    elif args.registry_cmd == "info":
        cmd_info(args.key)
    else:
        print("Unknown registry command")


def _audit_cli(args):
    """Run BRF audit on a registered dataset or CSV file."""
    from pathlib import Path
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from .analyzer import BRFAnalyzer

    key = args.dataset
    csv_path = Path(key)
    if csv_path.suffix == '.csv' and csv_path.exists():
        # CSV file mode: simple audit
        print(f"BRF Audit: {csv_path}")
        print("  CSV file mode: use brf.registry for full metadata support")
        return

    # Registry key mode
    try:
        from .registry import REGISTRY_SOURCES
    except ImportError:
        print(f"Error: Dataset '{key}' not found. Is benchmark-reliability installed with registry?")
        return

    source = REGISTRY_SOURCES.get(key)
    if source is None:
        print(f"Unknown dataset: {key}")
        print(f"Available: {', '.join(sorted(REGISTRY_SOURCES.keys()))}")
        return

    print(f"BRF Audit: {source.display_name} ({key})")
    X_raw, y, groups, card = source.prepare()
    X = StandardScaler().fit_transform(X_raw)
    n_grp = len(np.unique(groups)) if groups is not None else 0
    print(f"  N={len(y)}, p={X.shape[1]}, G={n_grp}")

    analyzer = BRFAnalyzer(n_splits=30, n_permutations=200).fit(X, y, groups=groups)
    bv = analyzer.brf_vector
    print(f"  B={bv['B']:.4f}  I={bv['I']:.4f}  N={bv['N']:.4f}  M={bv['M']:.4f}")
    print(f"  S={bv['S']:.4f}  E={bv['E']:.4f}  ->  {bv['class']}")


def main():
    parser = argparse.ArgumentParser(
        description="BRF -- Benchmark Reliability Framework"
    )
    sub = parser.add_subparsers(dest="command", help="Command")

    # --- brf audit ---
    audit = sub.add_parser("audit", help="Run BRF audit on a dataset")
    audit.add_argument("dataset", help="Path to dataset CSV")
    audit.add_argument("--group-col", help="Group column name")
    audit.add_argument("--target-col", help="Target column name")
    audit.set_defaults(func=_audit_cli)

    # --- brf registry ---
    reg = sub.add_parser("registry", help="Manage BRF Benchmark Registry")
    reg_sub = reg.add_subparsers(dest="registry_cmd", help="Registry command")

    reg_sub.add_parser("list", help="List all datasets")

    dl = reg_sub.add_parser("download", help="Download dataset(s)")
    dl.add_argument("key", nargs="?", help="Dataset key")
    dl.add_argument("--all", action="store_true", help="Download all")

    vf = reg_sub.add_parser("verify", help="Verify checksums")
    vf.add_argument("key", nargs="?", help="Dataset key")
    vf.add_argument("--all", action="store_true", help="Verify all")

    reg_sub.add_parser("sync", help="Download + verify all datasets")

    info = reg_sub.add_parser("info", help="Show dataset metadata")
    info.add_argument("key", help="Dataset key")

    reg.set_defaults(func=_registry_cli)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
