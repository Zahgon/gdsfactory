from __future__ import annotations

__all__ = ["coupler_pulley"]

from typing import Any

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import CrossSectionSpec, LayerSpec


def _cubic_bezier(
    p0: tuple[float, float],
    p1: tuple[float, float],
    p2: tuple[float, float],
    p3: tuple[float, float],
    n_points: int = 64,
) -> np.ndarray[Any, np.dtype[Any]]:
    pass


@gf.cell_with_module_name(tags=["couplers"])
def coupler_pulley(
    radius: float = 10.0,
    ring_width: float | None = None,
    gap: float = 0.2,
    coupling_angle: float = 60.0,
    wg_length: float = 40.0,
    wg_height: float = 10.0,
    n_segments: int = 128,
    cross_section: CrossSectionSpec = "strip",
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = coupler_pulley()
    c.pprint_ports()
    c.show()
