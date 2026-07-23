from __future__ import annotations

__all__ = ["coupler_adiabatic"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import CrossSectionSpec

from .._schematic import coupler_schematic
from ..bends.bend_s import bezier


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler_adiabatic(
    length1: float = 20.0,
    length2: float = 50.0,
    length3: float = 30.0,
    wg_sep: float = 1.0,
    input_wg_sep: float = 3.0,
    output_wg_sep: float = 3.0,
    dw: float = 0.1,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
