from pathlib import Path

from signin_sheet_builder.config import get_title_prefix, load_config
from signin_sheet_builder.excel_writer import convert_csv_folder_to_xlsx


def main() -> None:
    config = load_config(Path("config/config.toml"))
    title_prefix = get_title_prefix(config)

    convert_csv_folder_to_xlsx(
        Path("artifacts"),
        title_prefix=title_prefix,
    )


if __name__ == "__main__":
    main()
