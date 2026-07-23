
from __future__ import annotations

__all__ = ["straight_heater_meander_doped"]

from collections.abc import Iterable
from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference
from gdsfactory.cross_section import Section
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Floats, LayerSpecs, Port

from .._schematic import straight_schematic
from ..vias.via import via
from ..vias.via_stack import via_stack

_via_stack = partial(
    via_stack,
    size=(1.5, 1.5),
    layers=("M1", "M2"),
    vias=(
        partial(
            via,
            layer="VIAC",
            size=(0.1, 0.1),
            pitch=0.2,
            enclosure=0.1,
        ),
        partial(
            via,
            layer="VIA1",
            size=(0.1, 0.1),
            pitch=0.2,
            enclosure=0.1,
        ),
    ),
)


@gf.cell_with_module_name(schematic_function=straight_schematic, tags=["waveguides"])
def straight_heater_meander_doped(
    length: float = 300.0,
    spacing: float = 2.0,
    cross_section: CrossSectionSpec = "strip",
    heater_width: float = 1.5,
    extension_length: float = 15.0,
    layers_doping: LayerSpecs = ("P", "PP", "PPP"),
    radius: float = 5.0,
    via_stack: ComponentSpec | None = _via_stack,
    port_orientation1: float | None = None,
    port_orientation2: float | None = None,
    straight_widths: Floats = (0.8, 0.9, 0.8),
    taper_length: float = 10,
) -> Component:
    pass
