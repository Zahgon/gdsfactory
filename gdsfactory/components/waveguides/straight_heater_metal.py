from __future__ import annotations

__all__ = [
    "straight_heater_metal",
    "straight_heater_metal_90_90",
    "straight_heater_metal_simple",
    "straight_heater_metal_undercut",
    "straight_heater_metal_undercut_90_90",
]

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import straight_schematic
from ..containers.component_sequence import component_sequence


@gf.cell_with_module_name(schematic_function=straight_schematic, tags=["waveguides"])
def straight_heater_metal_undercut(
    length: float = 320.0,
    length_undercut_spacing: float = 6.0,
    length_undercut: float = 30.0,
    length_straight: float = 0.1,
    length_straight_input: float = 15.0,
    cross_section: CrossSectionSpec = "strip",
    cross_section_heater: CrossSectionSpec = "heater_metal",
    cross_section_waveguide_heater: CrossSectionSpec = "strip_heater_metal",
    cross_section_heater_undercut: CrossSectionSpec = "strip_heater_metal_undercut",
    with_undercut: bool = True,
    via_stack: ComponentSpec | None = "via_stack_heater_mtop",
    port_orientation1: int | None = None,
    port_orientation2: int | None = None,
    heater_taper_length: float = 5.0,
    ohms_per_square: float | None = None,
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=straight_schematic, tags=["waveguides"])
def straight_heater_metal_simple(
    length: float = 320.0,
    cross_section_heater: CrossSectionSpec = "heater_metal",
    cross_section_waveguide_heater: CrossSectionSpec = "strip_heater_metal",
    via_stack: ComponentSpec | None = "via_stack_heater_mtop",
    port_orientation1: int | None = None,
    port_orientation2: int | None = None,
    heater_taper_length: float = 5.0,
    ohms_per_square: float | None = None,
) -> Component:
    pass


straight_heater_metal = partial(
    straight_heater_metal_undercut,
    with_undercut=False,
    length_straight_input=0.1,
    length_undercut=5,
    length_undercut_spacing=0,
)
straight_heater_metal_90_90 = partial(
    straight_heater_metal,
    port_orientation1=90,
    port_orientation2=90,
)
straight_heater_metal_undercut_90_90 = partial(
    straight_heater_metal_undercut,
    port_orientation1=90,
    port_orientation2=90,
)
