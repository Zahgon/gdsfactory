from __future__ import annotations

__all__ = ["fractal"]

from typing import Literal

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


def _sierpinski_triangle(depth: int, size: float) -> list[list[tuple[float, float]]]:
    pass


def _sierpinski_carpet(depth: int, size: float) -> list[list[tuple[float, float]]]:
    pass


def _vicsek_cross(depth: int, size: float) -> list[list[tuple[float, float]]]:
    pass


def _vicsek_saltire(depth: int, size: float) -> list[list[tuple[float, float]]]:
    pass


@gf.cell_with_module_name(tags=["shapes"])
def fractal(
    fractal_type: Literal[
        "sierpinski_triangle",
        "sierpinski_carpet",
        "vicsek_cross",
        "vicsek_saltire",
    ] = "sierpinski_triangle",
    depth: int = 4,
    size: float = 100.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = fractal()
    c.show()
