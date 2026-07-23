from __future__ import annotations

__all__ = ["coupler_bend", "coupler_ring_bend", "ring_single_bend_coupler"]

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import AnyComponentFactory, ComponentSpec, CrossSectionSpec

from .._schematic import (
    coupler_ring_schematic,
    coupler_schematic,
    ring_single_schematic,
)
from ..bends.bend_circular import bend_circular_all_angle


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["rings"])
def coupler_bend(
    radius: float | None = None,
    coupler_gap: float = 0.2,
    coupling_angle_coverage: float = 120.0,
    cross_section_inner: CrossSectionSpec = "strip",
    cross_section_outer: CrossSectionSpec = "strip",
    bend: AnyComponentFactory = bend_circular_all_angle,
    bend_output: ComponentSpec = "bend_euler",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=coupler_ring_schematic, tags=["rings"])
def coupler_ring_bend(
    radius: float | None = None,
    coupler_gap: float = 0.2,
    coupling_angle_coverage: float = 90.0,
    length_x: float = 0.0,
    cross_section_inner: CrossSectionSpec = "strip",
    cross_section_outer: CrossSectionSpec = "strip",
    bend: AnyComponentFactory = bend_circular_all_angle,
    bend_output: ComponentSpec = "bend_euler",
    straight: ComponentSpec = "straight",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=ring_single_schematic, tags=["rings"])
def ring_single_bend_coupler(
    radius: float = 5.0,
    gap: float = 0.2,
    coupling_angle_coverage: float = 180.0,
    bend_all_angle: AnyComponentFactory = bend_circular_all_angle,
    bend: ComponentSpec = "bend_circular",
    bend_output: ComponentSpec = "bend_euler",
    length_x: float = 0.6,
    length_y: float = 0.6,
    cross_section_inner: CrossSectionSpec = "strip",
    cross_section_outer: CrossSectionSpec = "strip",
    **kwargs: Any,
) -> Component:
    pass
