from __future__ import annotations

__all__ = ["mmi_90degree_hybrid"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ckt_schematic
from ..tapers.taper import taper as taper_function


@gf.cell_with_module_name(schematic_function=ckt_schematic, tags=["mmis"])
def mmi_90degree_hybrid(
    width: float = 0.5,
    width_taper: float = 1.7,
    length_taper: float = 40.0,
    length_mmi: float = 175.0,
    width_mmi: float = 10.0,
    gap_mmi: float = 0.8,
    straight: ComponentSpec = "straight",
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
