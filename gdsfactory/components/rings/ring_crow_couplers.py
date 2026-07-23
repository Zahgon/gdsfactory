from __future__ import annotations

__all__ = ["ring_crow_couplers"]

from collections.abc import Sequence

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component, ComponentReference
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ring_double_schematic


@gf.cell_with_module_name(schematic_function=ring_double_schematic, tags=["rings"])
def ring_crow_couplers(
    radius: Sequence[float] = (10.0,) * 3,
    bends: Sequence[ComponentSpec] = ("bend_circular",) * 3,
    ring_cross_sections: Sequence[CrossSectionSpec] = ("strip",) * 3,
    couplers: Sequence[ComponentSpec] = ("coupler",) * 4,
) -> Component:
    pass
