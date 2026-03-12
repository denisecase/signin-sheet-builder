# ============================================================
# transform.py
# ============================================================
# Transform input CSV rows into sign-in sheet output rows.
# Each input record becomes two output rows.
# ============================================================

# === IMPORTS ===

import logging
from collections.abc import Iterable, Mapping
from typing import cast

from datafun_toolkit.logger import get_logger

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === TYPE ALIASES ===

Row = dict[str, str]
ConfigMap = Mapping[str, object]


# === PUBLIC FUNCTIONS ===


def build_output_headers(config: ConfigMap) -> list[str]:
    """Build the shared output CSV header row from config."""

    LOG.info("========================")
    LOG.info("START build_output_headers()")
    LOG.info("========================")

    output_headers: list[str] = _get_string_list(config, "output_headers")

    if not output_headers:
        msg = "Config error: output_headers must not be empty."
        LOG.error(msg)
        raise ValueError(msg)

    LOG.info("Built output headers successfully.")
    LOG.info("========================")
    LOG.info("END build_output_headers()")
    LOG.info("========================")

    return output_headers


def transform_rows(
    input_rows: Iterable[Row],
    config: ConfigMap,
) -> list[Row]:
    """Transform input rows into output rows for the sign-in sheet."""

    LOG.info("========================")
    LOG.info("START transform_rows()")
    LOG.info("========================")

    output_headers: list[str] = _get_string_list(config, "output_headers")
    row1_fields: list[str] = _get_string_list(config, "row1_fields")
    row2_fields: list[str] = _get_string_list(config, "row2_fields")
    spacer_enabled: bool = bool(config.get("add_spacer_row", False))

    _validate_layout(output_headers, row1_fields, row2_fields)

    output_rows: list[Row] = []

    for input_index, input_row in enumerate(input_rows, start=1):
        LOG.info(f"Transforming input row {input_index}.")

        row1_output: Row = _build_output_row(input_row, output_headers, row1_fields)
        row2_output: Row = _build_output_row(input_row, output_headers, row2_fields)

        output_rows.append(row1_output)
        output_rows.append(row2_output)

        if spacer_enabled:
            output_rows.append(_build_blank_row(output_headers))

    LOG.info(f"Created {len(output_rows)} output rows.")
    LOG.info("========================")
    LOG.info("END transform_rows()")
    LOG.info("========================")

    return output_rows


# === PRIVATE HELPERS ===


def _build_output_row(
    input_row: Row,
    output_headers: list[str],
    source_fields: list[str],
) -> Row:
    """Build one output row from one input row."""

    output_row: Row = {}

    for output_header, source_field in zip(output_headers, source_fields, strict=True):
        if source_field == "":
            output_row[output_header] = ""
        else:
            output_row[output_header] = str(input_row.get(source_field, "")).strip()

    return output_row


def _build_blank_row(output_headers: list[str]) -> Row:
    """Build one blank spacer row."""

    return {header: "" for header in output_headers}


def _get_string_list(config: ConfigMap, key: str) -> list[str]:
    """Get a required list[str] value from config."""

    value: object | None = config.get(key)

    if value is None:
        msg = f"Config error: missing required key '{key}'."
        LOG.error(msg)
        raise ValueError(msg)

    if not isinstance(value, list):
        msg = f"Config error: '{key}' must be a list."
        LOG.error(msg)
        raise ValueError(msg)

    result: list[str] = []

    raw_items: list[object] = cast(list[object], value)
    for item in raw_items:
        if not isinstance(item, str):
            msg = f"Config error: all items in '{key}' must be strings."
            LOG.error(msg)
            raise ValueError(msg)
        result.append(item)

    return result


def _validate_layout(
    output_headers: list[str],
    row1_fields: list[str],
    row2_fields: list[str],
) -> None:
    """Validate that the configured layout is rectangular."""

    count_headers: int = len(output_headers)
    count_row1_fields: int = len(row1_fields)
    count_row2_fields: int = len(row2_fields)

    if count_headers == 0:
        msg = "Config error: output_headers must not be empty."
        LOG.error(msg)
        raise ValueError(msg)

    if count_row1_fields != count_headers:
        msg = "Config error: row1_fields and output_headers must have equal length."
        LOG.error(msg)
        raise ValueError(msg)

    if count_row2_fields != count_headers:
        msg = "Config error: row2_fields and output_headers must have equal length."
        LOG.error(msg)
        raise ValueError(msg)

    LOG.info("Validated transform layout successfully.")
