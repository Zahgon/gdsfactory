from __future__ import annotations

__all__ = [
    "spiral_racetrack",
    "spiral_racetrack_fixed_length",
    "spiral_racetrack_heater_doped",
    "spiral_racetrack_heater_metal",
]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.routing.route_bundle import route_bundle
from gdsfactory.typings import (
    ComponentSpec,
    CrossSectionSpec,
    Floats,
    Port,
)

from .._schematic import spiral_schematic
from ..bends.bend_euler import bend_euler
from ..bends.bend_s import get_min_sbend_size
from ..waveguides.straight import straight


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def spiral_racetrack(
    min_radius: float | None = None,
    straight_length: float = 20.0,
    spacings: Floats = (2, 2, 3, 3, 2, 2),
    straight: ComponentSpec = straight,
    bend: ComponentSpec = bend_euler,
    bend_s: ComponentSpec = "bend_s",
    cross_section: CrossSectionSpec = "strip",
    cross_section_s: CrossSectionSpec | None = None,
    extra_90_deg_bend: bool = False,
    allow_min_radius_violation: bool = False,
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def spiral_racetrack_fixed_length(
    length: float = 1000,
    in_out_port_spacing: float = 150,
    n_straight_sections: int = 8,
    min_radius: float | None = None,
    min_spacing: float = 5.0,
    straight: ComponentSpec = straight,
    bend: ComponentSpec = "bend_circular",
    bend_s: ComponentSpec = "bend_s",
    cross_section: CrossSectionSpec = "strip",
    cross_section_s: CrossSectionSpec | None = None,
) -> Component:
    pass


def _req_straight_len(
    length: float = 1000,
    in_out_port_spacing: float = 100,
    min_radius: float | None = None,
    spacings: Floats = (1.0, 1.0),
    bend: ComponentSpec = bend_euler,
    bend_s: ComponentSpec = "bend_s",
    cross_section: CrossSectionSpec = "strip",
    cross_section_s_bend: CrossSectionSpec = "strip",
) -> float:
    pass


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def spiral_racetrack_heater_metal(
    min_radius: float | None = None,
    straight_length: float = 30,
    spacing: float = 2,
    num: int = 8,
    straight: ComponentSpec = straight,
    bend: ComponentSpec = bend_euler,
    bend_s: ComponentSpec = "bend_s",
    waveguide_cross_section: CrossSectionSpec = "strip",
    heater_cross_section: CrossSectionSpec = "heater_metal",
    via_stack: ComponentSpec | None = "via_stack_heater_mtop",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=spiral_schematic, tags=["spirals"])
def spiral_racetrack_heater_doped(
    min_radius: float | None = None,
    straight_length: float = 30,
    spacing: float = 2,
    num: int = 8,
    straight: ComponentSpec = straight,
    bend: ComponentSpec = bend_euler,
    bend_s: ComponentSpec = "bend_s",
    waveguide_cross_section: CrossSectionSpec = "strip",
    heater_cross_section: CrossSectionSpec = "npp",
) -> Component:
    pass
