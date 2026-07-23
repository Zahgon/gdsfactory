from __future__ import annotations

__all__ = ["straight_heater_meander"]

from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Floats, LayerSpec, Port

from .._schematic import straight_schematic


@gf.cell_with_module_name(schematic_function=straight_schematic, tags=["waveguides"])
def straight_heater_meander(
    length: float = 300.0,
    spacing: float = 2.0,
    cross_section: CrossSectionSpec = "strip",
    heater_width: float = 2.5,
    extension_length: float = 15.0,
    layer_heater: LayerSpec = "HEATER",
    radius: float | None = None,
    via_stack: ComponentSpec | None = "via_stack_heater_mtop",
    port_orientation1: float | None = None,
    port_orientation2: float | None = None,
    heater_taper_length: float = 10.0,
    straight_widths: Floats | None = None,
    taper_length: float = 10.0,
    n: int | None = 3,
) -> Component:
    pass


if __name__ == "__main__":
    c = straight_heater_meander(port_orientation1=None, port_orientation2=90)
    c.show()
