# src/signin_sheet_builder/pretty.py

from pathlib import Path

from signin_sheet_builder.excel_writer import convert_csv_folder_to_xlsx

convert_csv_folder_to_xlsx(Path("artifacts"))
