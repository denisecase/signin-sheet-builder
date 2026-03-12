# Changelog

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

## [Unreleased]

## [0.1.0] - 2026-03-12

### Added

- Initial public release
- CLI tool for transforming tabular data into sign-in sheet layouts
- Configurable field mapping using TOML or JSON
- Alphabetical split ranges for generating multiple check-in sheets
- CSV output for maximum compatibility
- Optional Excel generation with borders, header styling, and print layout
- Documentation site using Zensical
- Packaging via `pyproject.toml`
- Privacy-first design (data and configs excluded from Git)
- Ruff linting and pre-commit hooks
- CI/CD via GitHub Actions for checks and docs

## Notes on versioning and releases

- This project follows **Semantic Versioning (SemVer)**:
  - **MAJOR** – breaking changes to configuration schema or behavior
  - **MINOR** – backward-compatible features
  - **PATCH** – documentation, tooling, or internal improvements

- Versions are tagged in Git using `vX.Y.Z`.

Example:

```shell
# as needed
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0

git tag v0.1.0 -m "0.1.0"
git push origin v0.1.0
```

[Unreleased]: https://github.com/denisecase/signin-sheet-builder/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/denisecase/signin-sheet-builder/releases/tag/v0.1.0
