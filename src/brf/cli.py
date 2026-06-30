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
    """Run BRF audit on a dataset file."""
    print(f"BRF Audit: {args.dataset} (not yet implemented)")
    print("  This will run BRFAnalyzer on the input file.")


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
