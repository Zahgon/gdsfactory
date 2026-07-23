from __future__ import annotations

__all__ = ["ring_double_heater", "ring_single_heater"]

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import AngleInDegrees, ComponentSpec, CrossSectionSpec, Float2

from .._schematic import ring_double_schematic


@gf.cell_with_module_name(schematic_function=ring_double_schematic, tags=["rings"])
def ring_double_heater(
    gap: float = 0.2,
    gap_top: float | None = None,
    gap_bot: float | None = None,
    radius: float | None = None,
    length_x: float = 1.0,
    length_y: float = 0.01,
    coupler_ring: ComponentSpec = "coupler_ring",
    coupler_ring_top: ComponentSpec | None = None,
    straight: ComponentSpec = "straight",
    bend: ComponentSpec = "bend_euler",
    cross_section_heater: CrossSectionSpec = "heater_metal",
    cross_section_waveguide_heater: CrossSectionSpec = "strip_heater_metal",
    cross_section: CrossSectionSpec = "strip",
    via_stack: ComponentSpec = "via_stack_heater_mtop_mini",
    port_orientation: AngleInDegrees | None = None,
    via_stack_offset: Float2 = (1, 0),
    via_stack_size: Float2 | None = None,
    with_drop: bool = True,
    length_extension: float | None = None,
    length_extension_top: float | None = None,
    length_extension_bot: float | None = None,
) -> Component:
    pass


ring_single_heater = partial(ring_double_heater, with_drop=False)
