from __future__ import annotations

__all__ = ["mzi_lattice", "mzi_lattice_mmi"]

from collections.abc import Sequence
from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference

from .._schematic import mzi_2x2_schematic


@gf.cell_with_module_name(schematic_function=mzi_2x2_schematic, tags=["mzis"])
def mzi_lattice(
    coupler_lengths: Sequence[float] = (10.0, 20.0),
    coupler_gaps: Sequence[float] = (0.2, 0.3),
    delta_lengths: Sequence[float] = (10.0,),
    mzi: str = "mzi_coupler",
    splitter: str = "coupler",
    **kwargs: Any,
) -> Component:
    pass


@gf.cell_with_module_name(schematic_function=mzi_2x2_schematic, tags=["mzis"])
def mzi_lattice_mmi(
    coupler_widths: tuple[float | None, float | None] = (None, None),
    coupler_widths_tapers: tuple[float, ...] = (
        1.0,
        1.0,
    ),
    coupler_lengths_tapers: tuple[float, ...] = (
        10.0,
        10.0,
    ),
    coupler_lengths_mmis: tuple[float, ...] = (
        5.5,
        5.5,
    ),
    coupler_widths_mmis: tuple[float, ...] = (
        2.5,
        2.5,
    ),
    coupler_gaps_mmis: tuple[float, ...] = (
        0.25,
        0.25,
    ),
    taper_functions_mmis: tuple[str, ...] = (
        "taper",
        "taper",
    ),
    straight_functions_mmis: tuple[str, ...] = ("straight", "straight"),
    cross_sections_mmis: tuple[str, ...] = ("strip", "strip"),
    delta_lengths: tuple[float, ...] = (10.0,),
    mzi: str = "mzi2x2_2x2",
    splitter: str = "mmi2x2",
    **kwargs: Any,
) -> Component:
    pass
