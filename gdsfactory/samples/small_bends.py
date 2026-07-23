import sys
from pathlib import Path

import numpy as np

import gdsfactory as gf

_LAYER = gf.gpdk.LAYER.WG

_CALLS: list[tuple[list[tuple[float, float]], float, float]] = [
    (
        [(0.0, 7.5), (0.0, 38.5), (-4.0, 38.5), (-6.0, 38.5), (-6.0, 43.0)],
        1.0,
        0.5,
    ),
    (
        [(0.0, 7.5), (0.0, -4.0), (0.0, -5.0), (1.0, -6.0)],
        1.0,
        0.5,
    ),
    (
        [
            (0.0, 0.0),
            (0.0, -2.5),
            (-2.5, -4.0),
            (-2.5, -7.5),
            (-1.5, -9.0),
            (-1.5, -9.5),
        ],
        1.5,
        0.5,
    ),
    (
        [(0.0, -11.0), (0.0, -38.5), (4.0, -38.5), (6.0, -38.5), (6.0, -43.0)],
        1.0,
        0.5,
    ),
]


def _smooth_path(
    points: list[tuple[float, float]],
    width: float,
    radius: float,
) -> gf.Component:
    pass


def _main() -> None:
    pass


if __name__ == "__main__":
    gf.gpdk.PDK.activate()
    _main()
