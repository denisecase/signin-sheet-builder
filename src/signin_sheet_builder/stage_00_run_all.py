from signin_sheet_builder import (
    stage_01_to_csv,
    stage_02_to_xlsx,
    stage_03_to_pdf,
)


def main() -> None:
    print("Step 1: Generate CSV sign-in sheets")
    stage_01_to_csv.main()

    print("Step 2: Generate XLSX sheets")
    stage_02_to_xlsx.main()

    print("Step 3: Generate PDF sheets")
    stage_03_to_pdf.main()

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
