from __future__ import annotations

__all__ = ["ring_double_pn", "ring_single_pn"]

from functools import partial
from typing import Any

import numpy as np

import gdsfactory as gf
from gdsfactory.cross_section import Section, rib
from gdsfactory.typings import (
    ComponentSpec,
    CrossSectionFactory,
    CrossSectionSpec,
    LayerSpec,
)

from .._schematic import ring_double_schematic, ring_single_schematic
from ..vias.via import via
from ..vias.via_stack import via_stack

cross_section_rib = partial(
    gf.cross_section.strip,
    sections=(Section(width=2 * 2.425, layer="SLAB90", name="slab"),),
)
cross_section_pn = partial(
    gf.cross_section.pn,
    width_doping=2.425,
    width_slab=2 * 2.425,
    layer_via="VIAC",
    width_via=0.5,
    layer_metal="M1",
    width_metal=0.5,
)
_heater_vias = partial(
    via_stack,
    size=(0.5, 0.5),
    layers=("M1", "M2", "M3"),
    vias=(
        partial(via, layer="VIAC", size=(0.1, 0.1), enclosure=0.01, pitch=0.2),
        partial(
            via,
            layer="VIA1",
            size=(0.1, 0.1),
            enclosure=0.01,
            pitch=0.2,
        ),
        None,
    ),
    correct_size=True,
)


@gf.cell_with_module_name(schematic_function=ring_double_schematic, tags=["rings"])
def ring_double_pn(
    add_gap: float = 0.3,
    drop_gap: float = 0.3,
    radius: float = 5.0,
    doping_angle: float = 85,
    cross_section: CrossSectionFactory = rib,
    pn_cross_section: CrossSectionFactory = cross_section_pn,
    doped_heater: bool = True,
    doped_heater_angle_buffer: float = 10,
    doped_heater_layer: LayerSpec = "NPP",
    doped_heater_width: float = 0.5,
    doped_heater_waveguide_offset: float = 2.175,
    heater_vias: ComponentSpec = _heater_vias,
    with_drop: bool = True,
    **kwargs: Any,
) -> gf.Component:
    pass


@gf.cell_with_module_name(schematic_function=ring_single_schematic, tags=["rings"])
def ring_single_pn(
    gap: float = 0.3,
    radius: float = 5.0,
    doping_angle: float = 250,
    cross_section: CrossSectionSpec = rib,
    pn_cross_section: CrossSectionSpec = cross_section_pn,
    doped_heater: bool = True,
    doped_heater_angle_buffer: float = 10,
    doped_heater_layer: LayerSpec = "NPP",
    doped_heater_width: float = 0.5,
    doped_heater_waveguide_offset: float = 1.175,
    heater_vias: ComponentSpec = _heater_vias,
    pn_vias: ComponentSpec = "via_stack_slab_m3",
    pn_vias_width: float = 3,
) -> gf.Component:
    pass


if __name__ == "__main__":
    c = ring_single_pn()
    c.show()
