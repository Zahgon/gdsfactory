
from __future__ import annotations

__all__ = ["crossing", "crossing45", "crossing_etched", "crossing_linear_taper"]

import numpy as np
from kfactory.conf import CheckInstances

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Delta, LayerSpec

from .._schematic import crossing_schematic
from ..bends.bend_s import (
    bezier,
    find_min_curv_bezier_control_points,
)


@gf.cell_with_module_name(tags=["waveguides"])
def crossing_arm(
    r1: float = 3.0,
    r2: float = 1.1,
    w: float = 1.2,
    L: float = 3.4,
    layer_slab: LayerSpec = "SLAB150",
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=crossing_schematic, tags=["waveguides"])
def crossing(
    arm: ComponentSpec = crossing_arm,
) -> gf.Component:
    pass


@gf.cell_with_module_name(schematic_function=crossing_schematic, tags=["waveguides"])
def crossing_linear_taper(
    width1: float = 2.5,
    width2: float = 0.5,
    length: float = 3,
    cross_section: CrossSectionSpec = "strip",
    taper: ComponentSpec = "taper",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=crossing_schematic, tags=["waveguides"])
def crossing_etched(
    width: float = 0.5,
    r1: float = 3.0,
    r2: float = 1.1,
    w: float = 1.2,
    L: float = 3.4,
    layer_wg: LayerSpec = "WG",
    layer_slab: LayerSpec = "SLAB150",
) -> Component:
    pass


@gf.cell(
    check_instances=CheckInstances.IGNORE,
    with_module_name=True,
    schematic_function=crossing_schematic,
    tags=["waveguides"],
)
def crossing45(
    crossing: ComponentSpec = crossing,
    port_spacing: float = 40.0,
    dx: Delta | None = None,
    alpha: float = 0.08,
    npoints: int = 101,
    cross_section: CrossSectionSpec = "strip",
    cross_section_bends: CrossSectionSpec = "strip",
) -> Component:
    pass


__all__ = [
    "crossing",
    "crossing45",
    "crossing_etched",
    "crossing_linear_taper",
]
