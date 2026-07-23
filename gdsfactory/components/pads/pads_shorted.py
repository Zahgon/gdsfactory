from __future__ import annotations

__all__ = ["pads_shorted"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, LayerSpec


@gf.cell_with_module_name(tags=["pads"])
def pads_shorted(
    pad: ComponentSpec = "pad",
    columns: int = 8,
    pad_pitch: float = 150.0,
    layer_metal: LayerSpec = "MTOP",
    metal_width: float = 10,
) -> Component:
    pass
