
from __future__ import annotations

__all__ = [
    "wire_corner",
    "wire_corner45",
    "wire_corner45_straight",
    "wire_corner_sections",
]

from typing import Any

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.cross_section import (
    port_names_electrical,
    port_types_electrical,
)
from gdsfactory.typings import CrossSectionSpec, LayerSpec, PortNames, PortTypes


@gf.cell_with_module_name(tags=["waveguides"])
def wire_corner(
    cross_section: CrossSectionSpec = "metal_routing",
    port_names: PortNames = port_names_electrical,
    port_types: PortTypes = port_types_electrical,
    width: float | None = None,
    radius: float | None = None,
) -> Component:
    pass


@gf.cell(tags=["waveguides"])
def wire_corner45_straight(
    width: float | None = None,
    radius: float | None = None,
    cross_section: CrossSectionSpec = "metal_routing",
) -> gf.Component:
    pass


@gf.cell_with_module_name(tags=["waveguides"])
def wire_corner45(
    cross_section: CrossSectionSpec = "metal_routing",
    radius: float = 10,
    width: float | None = None,
    layer: LayerSpec | None = None,
    with_corner90_ports: bool = True,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["waveguides"])
def wire_corner_sections(
    cross_section: CrossSectionSpec = "metal_routing",
    port_type: str = "electrical",
    **kwargs: Any,
) -> Component:
    pass
