from __future__ import annotations

__all__ = ["dbr_tapered"]

from typing import cast

import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.snap import snap_to_grid2x
from gdsfactory.typings import CrossSectionSpec, Size


def _generate_fins(
    c: Component,
    fin_size: Size,
    taper_length: float,
    length: float,
    cross_section: CrossSectionSpec,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["filters"])
def dbr_tapered(
    length: float = 10.0,
    period: float = 0.85,
    dc: float = 0.5,
    w1: float = 0.4,
    w2: float = 1.0,
    taper_length: float = 20.0,
    fins: bool = False,
    fin_size: Size = (0.2, 0.05),
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
