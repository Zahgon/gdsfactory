from __future__ import annotations

__all__ = ["pixel", "qrcode", "version_stamp"]

import datetime
import platform

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import LayerSpec

from ..texts.text import text


@gf.cell_with_module_name(tags=["pcms"])
def pixel(size: int = 1, layer: LayerSpec = "WG") -> Component:
    pass


@gf.cell_with_module_name(tags=["pcms"])
def qrcode(data: str = "mask01", psize: int = 1, layer: LayerSpec = "WG") -> Component:
    pass


@gf.cell_with_module_name(tags=["pcms"])
def version_stamp(
    labels: tuple[str, ...] = ("demo_label",),
    with_qr_code: bool = False,
    layer: LayerSpec = "WG",
    pixel_size: int = 1,
    version: str | None = None,
    text_size: int = 10,
) -> Component:
    pass
