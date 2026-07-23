from __future__ import annotations

__all__ = ["mmi"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ckt_schematic


@gf.cell_with_module_name(schematic_function=ckt_schematic, tags=["mmis"])
def mmi(
    inputs: int = 1,
    outputs: int = 4,
    width: float | None = None,
    width_taper: float = 1.0,
    length_taper: float = 10.0,
    length_mmi: float = 5.5,
    width_mmi: float = 5,
    gap_input_tapers: float = 0.25,
    gap_output_tapers: float = 0.25,
    taper: ComponentSpec = "taper",
    straight: ComponentSpec = "straight",
    cross_section: CrossSectionSpec = "strip",
    input_positions: list[float] | None = None,
    output_positions: list[float] | None = None,
) -> Component:
    pass
