from __future__ import annotations

__all__ = ["mmi_tapered"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentFactory, CrossSectionSpec

from .._schematic import mmi_1x2_schematic
from ..tapers.taper import taper as taper_function


@gf.cell_with_module_name(schematic_function=mmi_1x2_schematic, tags=["mmis"])
def mmi_tapered(
    inputs: int = 1,
    outputs: int = 2,
    width: float | None = None,
    width_taper_in: float = 2.0,
    length_taper_in: float = 1.0,
    width_taper_out: float | None = None,
    length_taper_out: float | None = None,
    width_taper: float = 1.0,
    length_taper: float = 10.0,
    length_taper_start: float | None = None,
    length_taper_end: float | None = None,
    length_mmi: float = 5.5,
    width_mmi: float = 5,
    width_mmi_inner: float | None = None,
    gap_input_tapers: float = 0.25,
    gap_output_tapers: float = 0.25,
    taper: ComponentFactory = taper_function,
    cross_section: CrossSectionSpec = "strip",
    input_positions: list[float] | None = None,
    output_positions: list[float] | None = None,
) -> Component:
    pass
