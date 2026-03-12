# ============================================================
# split_config.py
# ============================================================
# Load and validate alphabetical split ranges for output files.
# ============================================================

# === IMPORTS ===

import logging
import re
from dataclasses import dataclass
from typing import cast

from datafun_toolkit.logger import get_logger

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === CONSTANTS ===

ALPHABET: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
RANGE_PATTERN: re.Pattern[str] = re.compile(r"^\s*([A-Za-z])\s*-\s*([A-Za-z])\s*$")


# === DATA CLASSES ===


@dataclass(frozen=True)
class SplitRange:
    """Represent one inclusive alphabetical split range."""

    label: str
    start_letter: str
    end_letter: str


# === PUBLIC FUNCTIONS ===


def load_split_ranges(config: dict[str, object]) -> list[SplitRange]:
    """Load and validate split ranges from config."""

    LOG.info("========================")
    LOG.info("START load_split_ranges()")
    LOG.info("========================")

    raw_ranges: list[str] = _get_required_string_list(config, "split_ranges")
    split_ranges: list[SplitRange] = parse_split_ranges(raw_ranges)

    validate_split_ranges(split_ranges)

    LOG.info(f"Loaded {len(split_ranges)} split ranges successfully.")
    LOG.info("========================")
    LOG.info("END load_split_ranges()")
    LOG.info("========================")

    return split_ranges


def parse_split_ranges(raw_ranges: list[str]) -> list[SplitRange]:
    """Parse split range strings like A-H into SplitRange objects."""

    LOG.info("========================")
    LOG.info("START parse_split_ranges()")
    LOG.info("========================")

    split_ranges: list[SplitRange] = []

    for raw_range in raw_ranges:
        match: re.Match[str] | None = RANGE_PATTERN.match(raw_range)

        if match is None:
            msg = (
                f"Invalid split range format: '{raw_range}'. "
                "Expected format like 'A-H'."
            )
            LOG.error(msg)
            raise ValueError(msg)

        start_letter: str = match.group(1).upper()
        end_letter: str = match.group(2).upper()

        if start_letter > end_letter:
            msg = (
                f"Invalid split range '{raw_range}': "
                f"start letter '{start_letter}' must not come after "
                f"end letter '{end_letter}'."
            )
            LOG.error(msg)
            raise ValueError(msg)

        split_ranges.append(
            SplitRange(
                label=f"{start_letter}-{end_letter}",
                start_letter=start_letter,
                end_letter=end_letter,
            )
        )

    LOG.info(f"Parsed {len(split_ranges)} split ranges.")
    LOG.info("========================")
    LOG.info("END parse_split_ranges()")
    LOG.info("========================")

    return split_ranges


def validate_split_ranges(split_ranges: list[SplitRange]) -> None:
    """Validate that split ranges fully and exactly cover A-Z."""

    LOG.info("========================")
    LOG.info("START validate_split_ranges()")
    LOG.info("========================")

    if not split_ranges:
        msg = "Config error: split_ranges must not be empty."
        LOG.error(msg)
        raise ValueError(msg)

    covered_letters: dict[str, str] = {}

    for split_range in split_ranges:
        current_letters: list[str] = expand_split_range(split_range)

        for letter in current_letters:
            if letter in covered_letters:
                msg = (
                    f"Config error: overlapping split ranges detected for letter "
                    f"'{letter}'. It appears in both '{covered_letters[letter]}' "
                    f"and '{split_range.label}'."
                )
                LOG.error(msg)
                raise ValueError(msg)

            covered_letters[letter] = split_range.label

    missing_letters: list[str] = [
        letter for letter in ALPHABET if letter not in covered_letters
    ]

    if missing_letters:
        msg = (
            "Config error: split_ranges do not fully cover A-Z. "
            f"Missing letters: {', '.join(missing_letters)}."
        )
        LOG.error(msg)
        raise ValueError(msg)

    LOG.info("Validated split ranges successfully.")
    LOG.info("========================")
    LOG.info("END validate_split_ranges()")
    LOG.info("========================")


def expand_split_range(split_range: SplitRange) -> list[str]:
    """Expand one split range into the list of letters it covers."""

    start_index: int = ALPHABET.index(split_range.start_letter)
    end_index: int = ALPHABET.index(split_range.end_letter)

    return list(ALPHABET[start_index : end_index + 1])


def get_split_label(last_name: str, split_ranges: list[SplitRange]) -> str:
    """Return the matching split label for a last name."""

    first_letter: str = extract_last_name_initial(last_name)

    for split_range in split_ranges:
        if split_range.start_letter <= first_letter <= split_range.end_letter:
            return split_range.label

    msg = (
        f"No configured split range found for last name '{last_name}' "
        f"(initial '{first_letter}')."
    )
    LOG.error(msg)
    raise ValueError(msg)


def extract_last_name_initial(last_name: str) -> str:
    """Extract the first alphabetical character from a last name."""

    cleaned: str = last_name.strip()

    for char in cleaned:
        if char.isalpha():
            return char.upper()

    msg = (
        f"Cannot determine alphabetical split for last name '{last_name}'. "
        "Expected at least one letter."
    )
    LOG.error(msg)
    raise ValueError(msg)


# === PRIVATE HELPERS ===


def _get_required_string_list(config: dict[str, object], key: str) -> list[str]:
    """Get a required list of strings from config."""

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
