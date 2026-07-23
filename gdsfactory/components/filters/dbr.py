
from __future__ import annotations

__all__ = ["dbr", "dbr_cell"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.snap import snap_to_grid
from gdsfactory.typings import CrossSectionSpec

period = 318e-3
w0 = 0.5
dw = 100e-3
w1 = w0 - dw / 2
w2 = w0 + dw / 2


@gf.cell_with_module_name(tags=["filters"])
def dbr_cell(
    w1: float = w1,
    w2: float = w2,
    l1: float = period / 2,
    l2: float = period / 2,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["filters"])
def dbr(
    w1: float = w1,
    w2: float = w2,
    l1: float = period / 2,
    l2: float = period / 2,
    n: int = 10,
    cross_section: CrossSectionSpec = "strip",
    straight_length: float = 10e-3,
) -> Component:
    pass
