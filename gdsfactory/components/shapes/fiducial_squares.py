from __future__ import annotations

__all__ = ["fiducial_squares"]

import numpy as np

import gdsfactory as gf
from gdsfactory.typings import Float2, LayerSpecs


@gf.cell_with_module_name(tags=["shapes"])
def fiducial_squares(
    layers: LayerSpecs = ("WG",), size: Float2 = (5, 5), offset: float = 0.14
) -> gf.Component:
    pass
