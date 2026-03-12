# ============================================================
# config.py
# ============================================================
# Load and validate configuration for the signin-sheet-builder.
# ============================================================

# === IMPORTS ===

import json
import logging
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Any, cast

from datafun_toolkit.logger import get_logger, log_path

from signin_sheet_builder.split_config import load_split_ranges

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === TYPE ALIASES ===

ConfigDict = dict[str, Any]
ConfigMap = Mapping[str, object]

# === REQUIRED CONFIG KEYS ===

REQUIRED_KEYS: tuple[str, ...] = (
    "output_headers",
    "row1_fields",
    "row2_fields",
    "split_ranges",
)


# === PUBLIC FUNCTIONS ===


def load_config(config_path: Path) -> ConfigDict:
    """Load config from TOML or JSON and validate required structure."""

    LOG.info("========================")
    LOG.info("START load_config()")
    LOG.info("========================")
    log_path(LOG, "CONFIG_FILE", config_path)

    validate_config_file(config_path)

    suffix: str = config_path.suffix.lower()

    if suffix == ".toml":
        with config_path.open("rb") as infile:
            config: ConfigDict = tomllib.load(infile)
    elif suffix == ".json":
        with config_path.open("r", encoding="utf-8", newline="") as infile:
            config = json.load(infile)
    else:
        msg = f"Unsupported config file type: {config_path}"
        LOG.error(msg)
        raise ValueError(msg)

    validate_config_dict(config)

    LOG.info("Loaded config successfully.")
    LOG.info("========================")
    LOG.info("END load_config()")
    LOG.info("========================")

    return config


def validate_config_file(config_path: Path) -> None:
    """Validate the configuration file path."""

    LOG.info("========================")
    LOG.info("START validate_config_file()")
    LOG.info("========================")

    if not config_path.exists():
        msg = f"Config file not found: {config_path}"
        LOG.error(msg)
        raise FileNotFoundError(msg)

    if not config_path.is_file():
        msg = f"Config path is not a file: {config_path}"
        LOG.error(msg)
        raise ValueError(msg)

    if config_path.suffix.lower() not in {".toml", ".json"}:
        msg = f"Config file must be .toml or .json: {config_path}"
        LOG.error(msg)
        raise ValueError(msg)

    LOG.info("Validated config file successfully.")
    LOG.info("========================")
    LOG.info("END validate_config_file()")
    LOG.info("========================")


def validate_config_dict(config: ConfigMap) -> None:
    """Validate required config keys and layout consistency."""

    LOG.info("========================")
    LOG.info("START validate_config_dict()")
    LOG.info("========================")

    for key in REQUIRED_KEYS:
        _require_string_list(config, key)

    output_headers: list[str] = _require_string_list(config, "output_headers")
    row1_fields: list[str] = _require_string_list(config, "row1_fields")
    row2_fields: list[str] = _require_string_list(config, "row2_fields")

    if not output_headers:
        msg = "Config error: output_headers must not be empty."
        LOG.error(msg)
        raise ValueError(msg)

    if len(row1_fields) != len(output_headers):
        msg = "Config error: row1_fields and output_headers must have equal length."
        LOG.error(msg)
        raise ValueError(msg)

    if len(row2_fields) != len(output_headers):
        msg = "Config error: row2_fields and output_headers must have equal length."
        LOG.error(msg)
        raise ValueError(msg)

    add_spacer_row: object = config.get("add_spacer_row", False)
    if not isinstance(add_spacer_row, bool):
        msg = "Config error: add_spacer_row must be true or false."
        LOG.error(msg)
        raise ValueError(msg)

    sort_field: object = config.get("sort_field", "Last Name")
    if not isinstance(sort_field, str) or not sort_field.strip():
        msg = "Config error: sort_field must be a non-empty string."
        LOG.error(msg)
        raise ValueError(msg)

    load_split_ranges(dict(config))

    LOG.info("Validated config dictionary successfully.")
    LOG.info("========================")
    LOG.info("END validate_config_dict()")
    LOG.info("========================")


# === PRIVATE HELPERS ===


def _require_string_list(config: ConfigMap, key: str) -> list[str]:
    """Require a config key to be present and contain a list of strings."""

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
