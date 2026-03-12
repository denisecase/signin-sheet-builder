# ============================================================
# pipeline.py
# ============================================================
# Run the full sign-in sheet build pipeline.
# ============================================================

# === IMPORTS ===

import csv
import logging
from pathlib import Path
from typing import Any

from datafun_toolkit.logger import get_logger, log_path

from signin_sheet_builder.config import load_config
from signin_sheet_builder.split_config import (
    SplitRange,
    get_split_label,
    load_split_ranges,
)
from signin_sheet_builder.transform import build_output_headers, transform_rows

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === TYPE ALIASES ===

Row = dict[str, str]


# === PUBLIC FUNCTIONS ===


def run_pipeline(
    input_path: Path,
    config_path: Path,
    artifacts_dir: Path,
) -> None:
    """Run the full CSV-to-sign-in-sheet pipeline."""

    LOG.info("========================")
    LOG.info("START run_pipeline()")
    LOG.info("========================")

    log_path(LOG, "INPUT_FILE", input_path)
    log_path(LOG, "CONFIG_FILE", config_path)
    log_path(LOG, "ARTIFACTS_DIR", artifacts_dir)

    artifacts_dir.mkdir(parents=True, exist_ok=True)

    config: dict[str, Any] = load_config(config_path)
    split_ranges: list[SplitRange] = load_split_ranges(config)
    sort_field: str = str(config.get("sort_field", "Last Name")).strip()

    input_rows: list[Row] = read_input_csv(input_path)
    sorted_rows: list[Row] = sort_input_rows(input_rows, sort_field)
    grouped_rows: dict[str, list[Row]] = group_rows_by_split(sorted_rows, split_ranges)

    output_headers: list[str] = build_output_headers(config)
    input_stem: str = input_path.stem

    for split_range in split_ranges:
        label: str = split_range.label
        split_input_rows: list[Row] = grouped_rows.get(label, [])
        split_output_rows: list[Row] = transform_rows(split_input_rows, config)
        output_path: Path = artifacts_dir / f"{input_stem}_signin_{label}.csv"

        write_output_csv(output_path, output_headers, split_output_rows)

        LOG.info(
            f"Wrote split file '{label}' with "
            f"{len(split_input_rows)} input rows and "
            f"{len(split_output_rows)} output rows."
        )

    LOG.info("========================")
    LOG.info("END run_pipeline()")
    LOG.info("========================")


def read_input_csv(input_path: Path) -> list[Row]:
    """Read the input CSV file into a list of row dictionaries."""

    LOG.info("========================")
    LOG.info("START read_input_csv()")
    LOG.info("========================")

    with input_path.open("r", encoding="utf-8-sig", newline="") as infile:
        reader = csv.DictReader(infile)
        rows: list[Row] = []

        for row in reader:
            clean_row: Row = {}
            for key, value in row.items():
                clean_key: str = "" if key is None else str(key).strip()
                clean_value: str = "" if value is None else str(value).strip()
                clean_row[clean_key] = clean_value
            rows.append(clean_row)

    LOG.info(f"Loaded {len(rows)} input rows from CSV.")
    LOG.info("========================")
    LOG.info("END read_input_csv()")
    LOG.info("========================")

    return rows


def sort_input_rows(input_rows: list[Row], sort_field: str) -> list[Row]:
    """Sort input rows by the configured sort field."""

    LOG.info("========================")
    LOG.info("START sort_input_rows()")
    LOG.info("========================")

    sorted_rows: list[Row] = sorted(
        input_rows,
        key=lambda row: row.get(sort_field, "").strip().upper(),
    )

    LOG.info(f"Sorted {len(sorted_rows)} rows by field '{sort_field}'.")
    LOG.info("========================")
    LOG.info("END sort_input_rows()")
    LOG.info("========================")

    return sorted_rows


def group_rows_by_split(
    input_rows: list[Row],
    split_ranges: list[SplitRange],
) -> dict[str, list[Row]]:
    """Group source rows by configured alphabetical last-name ranges."""

    LOG.info("========================")
    LOG.info("START group_rows_by_split()")
    LOG.info("========================")

    grouped: dict[str, list[Row]] = {
        split_range.label: [] for split_range in split_ranges
    }

    for row in input_rows:
        last_name: str = row.get("Last Name", "").strip()
        label: str = get_split_label(last_name, split_ranges)
        grouped[label].append(row)

    for label, rows in grouped.items():
        LOG.info(f"Grouped {len(rows)} input rows into split '{label}'.")

    LOG.info("========================")
    LOG.info("END group_rows_by_split()")
    LOG.info("========================")

    return grouped


def write_output_csv(
    output_path: Path,
    output_headers: list[str],
    output_rows: list[Row],
) -> None:
    """Write the transformed output rows to a CSV file."""

    LOG.info("========================")
    LOG.info("START write_output_csv()")
    LOG.info("========================")
    log_path(LOG, "OUTPUT_FILE", output_path)

    with output_path.open("w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(
            outfile,
            fieldnames=output_headers,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(output_rows)

    LOG.info(f"Wrote output CSV file: {output_path}")
    LOG.info("========================")
    LOG.info("END write_output_csv()")
    LOG.info("========================")
