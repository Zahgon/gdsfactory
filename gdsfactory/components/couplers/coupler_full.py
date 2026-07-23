from __future__ import annotations

__all__ = ["coupler_full"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import CrossSectionSpec, Delta

from .._schematic import coupler_schematic


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler_full(
    coupling_length: float = 40.0,
    dx: Delta = 10.0,
    dy: Delta = 4.8,
    gap: float = 0.5,
    dw: float = 0.1,
    cross_section: CrossSectionSpec = "strip",
    width: float | None = None,
) -> Component:
    pass
