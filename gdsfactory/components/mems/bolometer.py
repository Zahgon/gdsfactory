from __future__ import annotations

__all__ = ["bolometer"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["mems"])
def bolometer(
    absorber_width: float = 20.0,
    absorber_length: float = 20.0,
    leg_width: float = 0.5,
    leg_length: float = 15.0,
    n_legs: int = 4,
    pad_width: float = 5.0,
    pad_length: float = 5.0,
    layer: LayerSpec = "WG",
    port_type: str = "electrical",
) -> Component:
    pass


if __name__ == "__main__":
    c = bolometer()
    c.show()
