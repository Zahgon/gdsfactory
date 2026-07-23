
import logging
import os
from collections.abc import Sequence
from datetime import UTC, datetime
from subprocess import check_call

import klayout.db
from docopt import docopt


def check_klayout_version() -> None:
    pass


def check_layout_type(layout_path: str) -> str:
    pass


def get_top_cell_names(gds_path: str) -> list[str]:
    pass


def get_run_top_cell_name(arguments: dict[str, str], layout_path: str) -> str:
    pass


def generate_klayout_switches(
    arguments: dict[str, str], layout_path: str, netlist_path: str
) -> dict[str, str]:
    pass


def build_switches_string(sws: dict[str, str]) -> str:
    pass


def check_lvs_results(results_db_files: Sequence[str]) -> None:
    pass


def run_check(lvs_file: str, path: str, run_dir: str, sws: dict[str, str]) -> str:
    pass


def main(lvs_run_dir: str, arguments: dict[str, str]) -> None:
    pass


if __name__ == "__main__":
    arguments = docopt(__doc__, version="RUN LVS: 1.0")

    now_str = datetime.now(UTC).strftime("lvs_run_%Y_%m_%d_%H_%M_%S")

    if (
        arguments["--run_dir"] == "pwd"
        or arguments["--run_dir"] == ""
        or arguments["--run_dir"] is None
    ):
        lvs_run_dir = os.path.join(os.path.abspath(os.getcwd()), now_str)
    else:
        lvs_run_dir = os.path.abspath(arguments["--run_dir"])

    os.makedirs(lvs_run_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(os.path.join(lvs_run_dir, f"{now_str}.log")),
            logging.StreamHandler(),
        ],
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%d-%b-%Y %H:%M:%S",
    )

    main(lvs_run_dir, arguments)
