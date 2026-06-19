"""Command-line interface."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
import json
from pathlib import Path
import sys

from .normalizer import OUTPUT_FIELDS, normalize_rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def normalize_command(args: argparse.Namespace) -> int:
    try:
        rate = Decimal(args.rate) if args.rate is not None else None
    except InvalidOperation:
        print("error: --rate must be numeric", file=sys.stderr)
        return 2
    rows = normalize_rows(read_csv(args.input), default_currency=args.default_currency, target_currency=args.target_currency, rate=rate, mask_identifiers=args.mask_identifiers)
    write_csv(args.output, rows)
    invalid = sum(bool(row["validation_errors"]) for row in rows)
    print(f"normalized {len(rows)} rows; {invalid} rows need review")
    return 2 if args.strict and invalid else 0


def summarize_command(args: argparse.Namespace) -> int:
    rows = read_csv(args.input)
    categories = Counter(row.get("category", "") or "unknown" for row in rows)
    conditions = Counter(row.get("condition", "") or "unknown" for row in rows)
    currencies = Counter(row.get("currency", "") or "unknown" for row in rows)
    invalid = sum(bool(row.get("validation_errors", "")) for row in rows)
    result = {"rows": len(rows), "rows_needing_review": invalid, "categories": dict(sorted(categories.items())), "conditions": dict(sorted(conditions.items())), "currencies": dict(sorted(currencies.items()))}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reuse-trade", description="Normalize multilingual second-hand inventory CSV files.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    normalize = subparsers.add_parser("normalize", help="normalize a CSV file")
    normalize.add_argument("input", type=Path)
    normalize.add_argument("output", type=Path)
    normalize.add_argument("--default-currency", default="JPY")
    normalize.add_argument("--target-currency")
    normalize.add_argument("--rate", help="source-to-target conversion rate")
    normalize.add_argument("--mask-identifiers", action="store_true")
    normalize.add_argument("--strict", action="store_true")
    normalize.set_defaults(func=normalize_command)
    summarize = subparsers.add_parser("summarize", help="summarize normalized CSV")
    summarize.add_argument("input", type=Path)
    summarize.set_defaults(func=summarize_command)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
