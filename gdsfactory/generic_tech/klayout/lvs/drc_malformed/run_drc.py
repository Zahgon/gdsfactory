
import logging
import os
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from subprocess import check_call

import klayout.db
from docopt import docopt


def get_rules_with_violations(results_database: str) -> set[str]:
    pass


def check_drc_results(results_db_files: list[str]) -> None:
    pass


def get_top_cell_names(gds_path: str) -> list[str]:
    pass


def get_run_top_cell_name(arguments: dict[str, str], layout_path: str) -> str:
    pass


def generate_klayout_switches(
    arguments: dict[str, str], layout_path: str
) -> dict[str, str]:
    pass


def check_klayout_version() -> None:
    pass


def check_layout_path(layout_path: str) -> str:
    pass


def build_switches_string(sws: dict[str, str]) -> str:
    pass


def run_check(
    drc_file: str, drc_name: str, path: str, run_dir: str, sws: dict[str, str]
) -> str:
    pass


def run_single_processor(
    arguments: dict[str, str],
    rule_deck_full_path: str,
    layout_path: str,
    switches: dict[str, str],
    drc_run_dir: str,
) -> None:
    pass


def main(drc_run_dir: str, now_str: str, arguments: dict[str, str]) -> None:
    pass



if __name__ == "__main__":
    arguments = docopt(__doc__, version="RUN DRC-malformed: 1.0")

    now_str = datetime.now(UTC).strftime("drc_run_%Y_%m_%d_%H_%M_%S")

    if (
        arguments["--run_dir"] == "pwd"
        or arguments["--run_dir"] == ""
        or arguments["--run_dir"] is None
    ):
        drc_run_dir = os.path.join(os.path.abspath(os.getcwd()), now_str)
    else:
        drc_run_dir = os.path.abspath(arguments["--run_dir"])

    os.makedirs(drc_run_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(drc_run_dir, f"{now_str}.log")),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    main(drc_run_dir, now_str, arguments)
