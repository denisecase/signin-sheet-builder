# ============================================================
# pdf_writer.py
# ============================================================
# Export formatted Excel sign-in sheets to PDF using Excel on
# Windows via COM automation.
# ============================================================

# === IMPORTS ===

import logging
from pathlib import Path
from typing import Final

# pyright: reportMissingImports=false
import win32com.client  # type: ignore[import-not-found]
from datafun_toolkit.logger import get_logger, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P6", level="DEBUG")

# === EXCEL CONSTANTS ===

XL_TYPE_PDF: Final[int] = 0
XL_QUALITY_STANDARD: Final[int] = 0


# === PUBLIC FUNCTIONS ===


def export_xlsx_folder_to_pdf(
    xlsx_dir: Path,
    *,
    pattern: str = "*.xlsx",
    output_dir: Path | None = None,
) -> list[Path]:
    """Export all matching XLSX files in a folder to PDF."""

    LOG.info("========================")
    LOG.info("START export_xlsx_folder_to_pdf()")
    LOG.info("========================")
    log_path(LOG, "XLSX_DIR", xlsx_dir)

    validate_xlsx_dir(xlsx_dir)

    if output_dir is None:
        output_dir = xlsx_dir / "pdfs"

    output_dir.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "PDF_DIR", output_dir)

    excel = win32com.client.DispatchEx("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    written_paths: list[Path] = []

    try:
        for xlsx_path in sorted(xlsx_dir.glob(pattern)):
            if not xlsx_path.is_file():
                continue

            pdf_path: Path = output_dir / build_pdf_filename(xlsx_path)
            written_path: Path = export_one_workbook_to_pdf(
                excel,
                xlsx_path=xlsx_path,
                pdf_path=pdf_path,
            )
            written_paths.append(written_path)

    finally:
        excel.Quit()

    LOG.info(f"Exported {len(written_paths)} PDF files.")
    LOG.info("========================")
    LOG.info("END export_xlsx_folder_to_pdf()")
    LOG.info("========================")

    return written_paths


def export_one_workbook_to_pdf(
    excel_app: object,
    *,
    xlsx_path: Path,
    pdf_path: Path,
) -> Path:
    """Export one Excel workbook to one PDF file."""

    LOG.info("========================")
    LOG.info("START export_one_workbook_to_pdf()")
    LOG.info("========================")
    log_path(LOG, "XLSX_FILE", xlsx_path)
    log_path(LOG, "PDF_FILE", pdf_path)

    validate_xlsx_file(xlsx_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    workbook = None

    try:
        workbook = excel_app.Workbooks.Open(str(xlsx_path.resolve()))
        workbook.ExportAsFixedFormat(
            XL_TYPE_PDF,
            str(pdf_path.resolve()),
            XL_QUALITY_STANDARD,
            True,  # IncludeDocProperties
            False,  # IgnorePrintAreas
        )
    finally:
        if workbook is not None:
            workbook.Close(SaveChanges=False)

    LOG.info(f"Exported PDF file: {pdf_path}")
    LOG.info("========================")
    LOG.info("END export_one_workbook_to_pdf()")
    LOG.info("========================")

    return pdf_path


# === FILE HELPERS ===


def build_pdf_filename(xlsx_path: Path) -> str:
    """Build the output PDF filename from the XLSX filename."""

    stem: str = xlsx_path.stem
    label: str = extract_split_label_from_stem(stem)
    return f"SIGN_IN_Last_Name_{label}.pdf"


def extract_split_label_from_stem(stem: str) -> str:
    """Extract the final split label from a generated filename stem."""

    parts: list[str] = stem.split("_")
    if parts:
        return parts[-1]
    return stem


def validate_xlsx_dir(xlsx_dir: Path) -> None:
    """Validate the XLSX directory path."""

    if not xlsx_dir.exists():
        msg = f"XLSX directory not found: {xlsx_dir}"
        LOG.error(msg)
        raise FileNotFoundError(msg)

    if not xlsx_dir.is_dir():
        msg = f"XLSX path is not a directory: {xlsx_dir}"
        LOG.error(msg)
        raise ValueError(msg)


def validate_xlsx_file(xlsx_path: Path) -> None:
    """Validate the XLSX file path."""

    if not xlsx_path.exists():
        msg = f"XLSX file not found: {xlsx_path}"
        LOG.error(msg)
        raise FileNotFoundError(msg)

    if not xlsx_path.is_file():
        msg = f"XLSX path is not a file: {xlsx_path}"
        LOG.error(msg)
        raise ValueError(msg)

    if xlsx_path.suffix.lower() != ".xlsx":
        msg = f"Expected a .xlsx file: {xlsx_path}"
        LOG.error(msg)
        raise ValueError(msg)
