
from __future__ import annotations

__all__ = ["ge_detector_straight_si_contacts"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import photodiode_schematic


@gf.cell_with_module_name(schematic_function=photodiode_schematic, tags=["detectors"])
def ge_detector_straight_si_contacts(
    length: float = 40.0,
    cross_section: CrossSectionSpec = "pn_ge_detector_si_contacts",
    via_stack: ComponentSpec = "via_stack_slab_m3",
    via_stack_width: float = 10.0,
    via_stack_spacing: float = 5.0,
    via_stack_offset: float = 0.0,
    taper_length: float = 20.0,
    taper_width: float = 0.8,
    taper_cros_section: CrossSectionSpec = "strip",
) -> Component:
    pass
