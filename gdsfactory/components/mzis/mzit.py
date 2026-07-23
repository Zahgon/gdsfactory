from __future__ import annotations

__all__ = ["mzit", "mzit_lattice"]

from collections.abc import Sequence

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, Delta

from .._schematic import mzi_2x2_schematic


@gf.cell_with_module_name(schematic_function=mzi_2x2_schematic, tags=["mzis"])
def mzit(
    w0: float = 0.5,
    w1: float = 0.45,
    w2: float = 0.55,
    dy: Delta = 2.0,
    delta_length: float = 10.0,
    length: float = 1.0,
    coupler_length1: float = 5.0,
    coupler_length2: float = 10.0,
    coupler_gap1: float = 0.2,
    coupler_gap2: float = 0.3,
    taper: ComponentSpec = "taper",
    taper_length: float = 5.0,
    bend90: ComponentSpec = "bend_euler",
    straight: ComponentSpec = "straight",
    coupler1: ComponentSpec | None = "coupler",
    coupler2: ComponentSpec = "coupler",
    cross_section: str = "strip",
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=mzi_2x2_schematic, tags=["mzis"])
def mzit_lattice(
    coupler_lengths: Sequence[float] = (10.0, 20.0),
    coupler_gaps: Sequence[float] = (0.2, 0.3),
    delta_lengths: Sequence[float] = (10.0,),
    mzi: ComponentSpec = mzit,
) -> Component:
    pass
