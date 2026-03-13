# ============================================================
# cli.py
# ============================================================
# Command-line interface for the CSV generation step.
# ============================================================

# === IMPORTS ===

import argparse
import logging
import sys
from pathlib import Path
from typing import Final

from datafun_toolkit.logger import get_logger, log_header, log_path

from signin_sheet_builder.config import validate_config_file
from signin_sheet_builder.pipeline import run_pipeline

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"
CONFIG_DIR: Final[Path] = ROOT_DIR / "config"


# === MAIN CLI FUNCTION ===


def main() -> None:
    """Run the CSV generation step for sign-in sheets."""

    log_header(LOG, "SIGNIN")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_DIR", DATA_DIR)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)
    log_path(LOG, "CONFIG_DIR", CONFIG_DIR)

    parser = argparse.ArgumentParser(
        prog="signin-create-csv",
        description="Generate split sign-in sheet CSV files from an input CSV file.",
    )

    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to the configuration file (.toml or .json).",
    )

    args = parser.parse_args()

    input_path: Path = args.input
    config_path: Path = args.config

    log_path(LOG, "INPUT_FILE", input_path)
    log_path(LOG, "CONFIG_FILE", config_path)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    try:
        validate_input_file(input_path)
        validate_config_file(config_path)

        ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

        run_pipeline(
            input_path=input_path,
            config_path=config_path,
            artifacts_dir=ARTIFACTS_DIR,
        )

        LOG.info("CSV generation step executed successfully.")

    except Exception as exc:
        LOG.exception(f"CSV generation step failed: {exc}")
        sys.exit(1)

    LOG.info("========================")
    LOG.info("END main()")
    LOG.info("========================")


# === FILE HELPERS ===


def validate_input_file(input_path: Path) -> None:
    """Validate the input CSV file."""

    LOG.info("========================")
    LOG.info("START validate_input_file()")
    LOG.info("========================")

    if not input_path.exists():
        msg = f"Input file not found: {input_path}"
        LOG.error(msg)
        raise FileNotFoundError(msg)

    if not input_path.is_file():
        msg = f"Input path is not a file: {input_path}"
        LOG.error(msg)
        raise ValueError(msg)

    if input_path.suffix.lower() != ".csv":
        msg = f"Input file must be a CSV file: {input_path}"
        LOG.error(msg)
        raise ValueError(msg)

    LOG.info("Validated input file successfully.")
    LOG.info("========================")
    LOG.info("END validate_input_file()")
    LOG.info("========================")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
