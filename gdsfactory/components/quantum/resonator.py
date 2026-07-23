from __future__ import annotations

__all__ = ["resonator_cpw", "resonator_lumped", "resonator_quarter_wave"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["quantum"])
def resonator_cpw(
    length: float = 1000.0,
    width: float = 10.0,
    gap: float = 6.0,
    meander_pitch: float = 50.0,
    meander_width: float = 200.0,
    coupling_gap: float = 5.0,
    coupling_length: float = 100.0,
    layer_metal: LayerSpec = (1, 0),
    layer_gap: LayerSpec = (2, 0),
    port_type: str = "electrical",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["quantum"])
def resonator_lumped(
    capacitor_fingers: int = 4,
    capacitor_finger_length: float = 20.0,
    capacitor_finger_gap: float = 2.0,
    capacitor_thickness: float = 5.0,
    inductor_width: float = 2.0,
    inductor_turns: int = 3,
    inductor_radius: float = 20.0,
    coupling_gap: float = 5.0,
    layer_metal: LayerSpec = (1, 0),
    port_type: str = "electrical",
) -> Component:
    pass


@gf.cell_with_module_name(tags=["quantum"])
def resonator_quarter_wave(
    length: float = 2500.0,
    width: float = 10.0,
    gap: float = 6.0,
    short_stub_length: float = 50.0,
    coupling_gap: float = 5.0,
    coupling_length: float = 100.0,
    layer_metal: LayerSpec = (1, 0),
    layer_gap: LayerSpec = (2, 0),
    port_type: str = "electrical",
) -> Component:
    pass
