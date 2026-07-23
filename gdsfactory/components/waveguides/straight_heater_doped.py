from __future__ import annotations

__all__ = ["straight_heater_doped_rib", "straight_heater_doped_strip"]

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference
from gdsfactory.snap import snap_to_grid
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Size

from .._schematic import straight_schematic


@gf.cell_with_module_name(schematic_function=straight_schematic, tags=["waveguides"])
def straight_heater_doped_rib(
    length: float = 320.0,
    nsections: int = 3,
    cross_section: CrossSectionSpec = "strip_rib_tip",
    cross_section_heater: CrossSectionSpec = "rib_heater_doped",
    via_stack: ComponentSpec | None = "via_stack_slab_npp_m3",
    via_stack_metal: ComponentSpec | None = "via_stack_m1_mtop",
    via_stack_metal_size: Size = (10.0, 10.0),
    via_stack_size: Size = (10.0, 10.0),
    taper: ComponentSpec | None = "taper_cross_section",
    heater_width: float = 2.0,
    heater_gap: float = 0.8,
    via_stack_gap: float = 0.0,
    width: float = 0.5,
    xoffset_tip1: float = 0.2,
    xoffset_tip2: float = 0.4,
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=straight_schematic, tags=["waveguides"])
def straight_heater_doped_strip(
    length: float = 320.0,
    nsections: int = 3,
    cross_section: CrossSectionSpec = "strip_heater_doped",
    cross_section_heater: CrossSectionSpec = "rib_heater_doped",
    via_stack: ComponentSpec | None = "via_stack_npp_m1",
    via_stack_metal: ComponentSpec | None = "via_stack_m1_mtop",
    via_stack_metal_size: Size = (10.0, 10.0),
    via_stack_size: Size = (10.0, 10.0),
    taper: ComponentSpec | None = "taper_cross_section",
    heater_width: float = 2.0,
    heater_gap: float = 0.8,
    via_stack_gap: float = 0.0,
    width: float = 0.5,
    xoffset_tip1: float = 0.2,
    xoffset_tip2: float = 0.4,
) -> Component:
    pass
