from __future__ import annotations

__all__ = ["flux_qubit", "flux_qubit_asymmetric"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["quantum"])
def flux_qubit(
    loop_width: float = 50.0,
    loop_height: float = 50.0,
    junction_width: float = 0.15,
    junction_height: float = 0.3,
    alpha_junction_width: float = 0.12,
    alpha_junction_height: float = 0.25,
    wire_width: float = 2.0,
    layer_metal: LayerSpec = (1, 0),
    layer_junction: LayerSpec = (2, 0),
    layer_alpha_junction: LayerSpec = (3, 0),
    port_type: str = "electrical",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["quantum"])
def flux_qubit_asymmetric(
    loop_width: float = 60.0,
    loop_height: float = 40.0,
    junction_width: float = 0.15,
    junction_height: float = 0.3,
    alpha_junction_width: float = 0.12,
    alpha_junction_height: float = 0.25,
    wire_width: float = 2.0,
    asymmetry_angle: float = 15.0,
    layer_metal: LayerSpec = (1, 0),
    layer_junction: LayerSpec = (2, 0),
    layer_alpha_junction: LayerSpec = (3, 0),
    port_type: str = "electrical",
) -> Component:
    pass
