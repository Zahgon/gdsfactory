from __future__ import annotations

__all__ = ["resolution_test_pattern"]

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["pcms"])
def resolution_test_pattern(
    radius: float = 50.0,
    n_spokes: int = 36,
    width: float = 1.0,
    layer: LayerSpec = "WG",
) -> Component:
    pass


if __name__ == "__main__":
    c = resolution_test_pattern()
    c.show()
