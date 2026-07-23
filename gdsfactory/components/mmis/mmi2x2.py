from __future__ import annotations

__all__ = ["mmi2x2"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import mmi_2x2_schematic
from ..tapers.taper import taper as taper_function
from ..waveguides.straight import straight as straight_function


@gf.cell_with_module_name(schematic_function=mmi_2x2_schematic, tags=["mmis"])
def mmi2x2(
    width: float | None = None,
    width_taper: float = 1.0,
    length_taper: float = 10.0,
    length_mmi: float = 5.5,
    width_mmi: float = 2.5,
    gap_mmi: float = 0.25,
    taper: ComponentSpec = taper_function,
    straight: ComponentSpec = straight_function,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
