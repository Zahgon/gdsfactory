from __future__ import annotations

__all__ = ["seal_ring", "seal_ring_segmented"]

import gdsfactory as gf
from gdsfactory.snap import snap_to_grid
from gdsfactory.typings import ComponentSpec, Float2


@gf.cell_with_module_name(tags=["dies"])
def seal_ring(
    size: Float2 = (500, 500),
    seal: ComponentSpec = "via_stack",
    width: float = 10,
    padding: float = 10.0,
    with_north: bool = True,
    with_south: bool = True,
    with_east: bool = True,
    with_west: bool = True,
) -> gf.Component:
    pass


@gf.cell_with_module_name(tags=["dies"])
def seal_ring_segmented(
    size: Float2 = (500, 500),
    length_segment: float = 10,
    width_segment: float = 3,
    spacing_segment: float = 2,
    corner: ComponentSpec = "via_stack_corner45_extended",
    via_stack: ComponentSpec = "via_stack_m1_mtop",
    with_north: bool = True,
    with_south: bool = True,
    with_east: bool = True,
    with_west: bool = True,
) -> gf.Component:
    pass
