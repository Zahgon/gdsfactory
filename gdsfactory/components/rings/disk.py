from __future__ import annotations

__all__ = ["disk", "disk_heater"]

import math

import gdsfactory as gf
from gdsfactory import Component
from gdsfactory.component import ComponentReference
from gdsfactory.cross_section import CrossSection
from gdsfactory.typings import (
    AngleInDegrees,
    ComponentSpec,
    CrossSectionSpec,
    LayerSpec,
)

from .._schematic import ring_single_schematic


def _compute_parameters(
    xs_bend: CrossSection, wrap_angle_deg: float, radius: float
) -> tuple[float, float, float, float]:
    pass


def _generate_bends(
    c: Component,
    r_bend: float,
    wrap_angle_deg: float,
    cross_section: CrossSectionSpec,
) -> tuple[
    Component,
    ComponentReference | None,
    ComponentReference | None,
    ComponentReference | None,
]:
    pass


def _generate_straights(
    c: Component,
    bus_length: float,
    size_x: float,
    bend_input: ComponentReference | None,
    bend_output: ComponentReference | None,
    cross_section: CrossSectionSpec,
) -> tuple[Component, ComponentReference, ComponentReference]:
    pass


@gf.cell_with_module_name(schematic_function=ring_single_schematic, tags=["rings"])
def disk(
    radius: float = 10.0,
    gap: float = 0.2,
    wrap_angle_deg: float = 180.0,
    parity: int = 1,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=ring_single_schematic, tags=["rings"])
def disk_heater(
    radius: float = 10.0,
    gap: float = 0.2,
    wrap_angle_deg: float = 180.0,
    parity: int = 1,
    cross_section: CrossSectionSpec = "strip",
    heater_layer: LayerSpec = "HEATER",
    via_stack: ComponentSpec = "via_stack_heater_mtop",
    heater_width: float = 5.0,
    heater_extent: float = 2.0,
    via_width: float = 10.0,
    port_orientation: AngleInDegrees | None = 90,
) -> Component:
    pass
