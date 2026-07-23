from __future__ import annotations

__all__ = ["dash"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


def _bezier3(
    px: list[float], py: list[float], n: int = 30
) -> tuple[list[float], list[float]]:
    pass


@gf.cell_with_module_name(tags=["shapes"])
def dash(
    width: float = 10.0,
    width_end: float = 1.0,
    length: float = 20.0,
    taper_length: float = 5.0,
    tip_length: float = 2.0,
    n_bezier_points: int = 30,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = dash()
    c.show()
