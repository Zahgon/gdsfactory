
from __future__ import annotations

__all__ = ["pad_gs", "pad_gsg", "pad_gsg_open", "pad_gsg_short"]

from functools import partial
from typing import cast

import kfactory as kf

import gdsfactory as gf
from gdsfactory.typings import ComponentSpec, Float2, LayerSpec

from .._schematic import pad_schematic


@gf.cell_with_module_name(tags=["pads"])
def pad_gsg_short(
    size: Float2 = (22, 7),
    layer_metal: LayerSpec = "MTOP",
    metal_spacing: float = 5.0,
    short: bool = True,
    pad: ComponentSpec = "pad",
    pad_pitch: float = 150,
    route_xsize: float = 50,
) -> gf.Component:
    pass


pad_gsg_open = partial(pad_gsg_short, short=False)


@gf.cell_with_module_name(schematic_function=pad_schematic, tags=["pads"])
def pad_gsg(length: float = 100, cross_section: str = "gsg") -> gf.Component:
    pass


@gf.cell_with_module_name(tags=["pads"])
def pad_gs(length: float = 100, cross_section: str = "gs") -> gf.Component:
    pass


if __name__ == "__main__":
    c = pad_gs()
    c.show()
