# signin-sheet-builder

[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://denisecase.github.io/signin-sheet-builder/)
[![CI Status](https://github.com/denisecase/signin-sheet-builder/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/denisecase/signin-sheet-builder/actions/workflows/ci-python-zensical.yml)
[![Python 3.14+](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](#)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

Professional Python project for transforming tabular registration data into printable sign-in sheet layouts.

# Overview

This project reads a source data file (typically CSV) and converts each input record into a **two-row sign-in sheet layout**.

Typical use case:

- start with one file containing many columns
- sort and reorganize selected fields
- expand each input row into two output rows
- split results into multiple alphabetical groups
- write output as CSV for maximum compatibility
- optionally generate formatted Excel files for printing

The project is designed so that:

- code can be published to GitHub
- private data files stay local
- transformation behavior is controlled by configuration

# Input and Output

### Input

- `.csv` preferred
- `.xlsx` optional if Excel support is enabled

Example source:

```
data/members.csv
```

### Output

Generated files appear in:

```
artifacts/
```

Outputs include:

- multiple **CSV sign-in sheets**
- optional **formatted Excel (.xlsx)** versions for printing

# Configuration

Transformation behavior is defined in a configuration file.

Public repositories should include:

```
config/config.example.toml
```

Users create their own local version:

```
config/config.toml
```

Example configuration:

```toml
split_ranges = [
  "A-F",
  "G-L",
  "M-R",
  "S-Z",
]

output_headers = [
  "Last-Address",
  "First-City",
  "Area-Zip",
  "Group-Phone",
  "Role-PhoneType",
  "Signature-OKEdits",
]

row1_fields = [
  "Last Name",
  "First Name",
  "Area",
  "Group",
  "Role",
  "",
]

row2_fields = [
  "Address",
  "City",
  "Zip",
  "Phone Number",
  "Type of Number",
  "",
]

add_spacer_row = false
sort_field = "Last Name"
```

### Split Ranges

The `split_ranges` configuration determines how records are divided into separate sign-in sheets.

Example:

```
A-F
G-L
M-R
S-Z
```

These ranges can be adjusted to balance table workloads if some letter groups contain more names.

# Working Files

```
config/                     configuration files
data/                       local input data
artifacts/                  generated outputs
docs/                       documentation
src/signin_sheet_builder/   package source code

pyproject.toml              project configuration
zensical.toml               documentation configuration
```

# Installation

Clone the repository:

```shell
git clone https://github.com/username/signin-sheet-builder
cd signin-sheet-builder
code .
```

## Step 1. Set Up the Project Environment Setup

In a VS Code terminal:

```shell
uv self update
uv python pin 3.14
uv sync --extra dev --extra docs --upgrade

uvx pre-commit install
git add -A
uvx pre-commit run --all-files
```

## Step 2. Customize the Data

Place your private data and configuration locally:

```
data/members.csv
config/config.toml
```

## Step 3. Run the Tool (On Windows)

Generate sign-in sheets from a source CSV file.
Run the full pipeline. This command performs all steps:

1. generate sign-in CSV files
2. format Excel versions
3. export PDFs for printing

```shell
uv run signin-create-all
```

Or run each step in order:

```shell
uv run signin-create-csv
uv run signin-create-xlsx
uv run signin-create-pdf
```


# Development Commands

```
uv run ruff format .
uv run ruff check . --fix
uv run zensical build

git add -A
git commit -m "update"
git push -u origin main
```

# Notes

- Keep real data out of Git.
- Local data in `data/`.
- Generated outputs in `artifacts/`.
- Excel and PDF generation are optional; depend on operating system and installed libraries.
