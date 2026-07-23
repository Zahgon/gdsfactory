from __future__ import annotations

__all__ = ["coupler_capacitive", "coupler_interdigital", "coupler_tunable"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["quantum"])
def coupler_capacitive(
    pad_width: float = 20.0,
    pad_height: float = 50.0,
    gap: float = 2.0,
    feed_width: float = 10.0,
    feed_length: float = 30.0,
    layer_metal: LayerSpec = (1, 0),
    port_type: str = "electrical",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["quantum"])
def coupler_interdigital(
    fingers: int = 6,
    finger_length: float = 30.0,
    finger_width: float = 2.0,
    finger_gap_vertical: float = 2.0,
    finger_gap_horizontal: float = 3.0,
    feed_width: float = 10.0,
    feed_length: float = 30.0,
    layer_metal: LayerSpec = (1, 0),
    port_type: str = "electrical",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["quantum"])
def coupler_tunable(
    pad_width: float = 30.0,
    pad_height: float = 40.0,
    gap: float = 3.0,
    tuning_pad_width: float = 15.0,
    tuning_pad_height: float = 20.0,
    tuning_gap: float = 1.0,
    feed_width: float = 10.0,
    feed_length: float = 30.0,
    layer_metal: LayerSpec = (1, 0),
    layer_tuning: LayerSpec = (3, 0),
    port_type: str = "electrical",
) -> Component:
    pass
