from __future__ import annotations

__all__ = ["ring_single_dut"]

from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.snap import assert_on_2x_grid
from gdsfactory.typings import ComponentSpec

from .._schematic import ring_single_schematic


@gf.cell_with_module_name(schematic_function=ring_single_schematic, tags=["rings"])
def ring_single_dut(
    component: ComponentSpec = "straight",
    gap: float = 0.2,
    length_x: float = 4,
    length_y: float = 0,
    radius: float | None = None,
    coupler: ComponentSpec = "coupler_ring",
    bend: ComponentSpec = "bend_euler",
    with_component: bool = True,
    port_name: str = "o1",
    length_extension: float | None = None,
    **kwargs: Any,
) -> Component:
    pass
