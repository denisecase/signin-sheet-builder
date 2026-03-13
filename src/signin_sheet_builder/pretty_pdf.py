# src/signin_sheet_builder/pretty_pdf.py

from pathlib import Path

from signin_sheet_builder.pdf_writer import export_xlsx_folder_to_pdf


def main() -> None:
    """Export formatted Excel sign-in sheets to PDF."""

    export_xlsx_folder_to_pdf(Path("artifacts"))


if __name__ == "__main__":
    main()
