from pathlib import Path

from signin_sheet_builder.pipeline import run_pipeline


def main() -> None:
    run_pipeline(
        input_path=Path("data/members.csv"),
        config_path=Path("config/config.toml"),
        artifacts_dir=Path("artifacts"),
    )


if __name__ == "__main__":
    main()
