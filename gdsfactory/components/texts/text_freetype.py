from __future__ import annotations

__all__ = ["text_freetype"]

import pathlib
import warnings

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.config import PATH
from gdsfactory.constants import _glyph, _indent, _width
from gdsfactory.typings import LayerSpec, LayerSpecs, PathType


@gf.cell_with_module_name(tags=["texts"])
def text_freetype(
    text: str = "a",
    size: int = 10,
    justify: str = "left",
    font: PathType = PATH.font_ocr,
    layer: LayerSpec = "WG",
    layers: LayerSpecs | None = None,
) -> Component:
    pass
