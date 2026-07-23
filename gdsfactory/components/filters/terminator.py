from __future__ import annotations

__all__ = ["terminator"]

import gdsfactory as gf
from gdsfactory.add_padding import get_padding_points
from gdsfactory.component import Component
from gdsfactory.cross_section import strip
from gdsfactory.typings import CrossSectionSpec, LayerSpecs

from .._schematic import terminator_schematic


@gf.cell_with_module_name(schematic_function=terminator_schematic, tags=["filters"])
def terminator(
    length: float | None = 50,
    cross_section_input: CrossSectionSpec = strip,
    cross_section_tip: CrossSectionSpec | None = None,
    tapered_width: float = 0.2,
    doping_layers: LayerSpecs = ("NPP",),
    doping_offset: float = 1.0,
) -> gf.Component:
    pass
