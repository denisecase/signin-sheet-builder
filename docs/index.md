# Signin Sheet Builder

Tool for transforming member data into printable sign-in sheets.

## Quick Start

1. Copy the example config:

```bash
copy config\config.example.toml config\config.toml
```

2. Put your private input file in:

```text
data/
```

For example:

```text
data/members.csv
```

3. Run the tool:

```bash
uv run signin-sheet --input data/members.csv --config config/config.toml
```

4. Find generated output files in:

```text
artifacts/
```

5. Optionally generate formatted Excel files for printing:

```bash
uv run python -m signin_sheet_builder.pretty
```

## Notes

- Keep real member data out of Git.
- Edit `config/config.toml` to match actual input columns and preferred split ranges.
- The public repo should include `config/config.example.toml`, not the private `config/config.toml`.
