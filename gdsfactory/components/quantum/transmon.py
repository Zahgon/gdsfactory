from __future__ import annotations

__all__ = ["transmon", "transmon_circular"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["quantum"])
def transmon(
    pad_width: float = 200.0,
    pad_height: float = 100.0,
    pad_gap: float = 6.0,
    junction_width: float = 0.15,
    junction_height: float = 0.3,
    island_width: float = 10.0,
    island_height: float = 4.0,
    layer_metal: LayerSpec = (1, 0),
    layer_junction: LayerSpec = (2, 0),
    layer_island: LayerSpec = (1, 0),
    port_type: str = "electrical",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["quantum"])
def transmon_circular(
    pad_radius: float = 100.0,
    pad_gap: float = 6.0,
    junction_width: float = 0.15,
    junction_height: float = 0.3,
    island_radius: float = 5.0,
    layer_metal: LayerSpec = (1, 0),
    layer_junction: LayerSpec = (2, 0),
    layer_island: LayerSpec = (1, 0),
    port_type: str = "electrical",
) -> Component:
    pass
