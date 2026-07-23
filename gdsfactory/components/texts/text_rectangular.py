from __future__ import annotations

__all__ = ["text_rectangular", "text_rectangular_multi_layer"]

from collections.abc import Callable
from functools import partial
from typing import Any

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, LayerSpec, LayerSpecs

from ..containers.copy_layers import copy_layers
from ..texts.text_rectangular_font import (
    pixel_array,
    rectangular_font,
)


@gf.cell_with_module_name(tags=["texts"])
def text_rectangular(
    text: str = "abcd",
    size: float = 10.0,
    position: tuple[float, float] = (0.0, 0.0),
    justify: str = "left",
    layer: LayerSpec | None = "WG",
    layers: LayerSpecs | None = None,
    font: Callable[..., dict[str, str]] = rectangular_font,
) -> Component:
    pass


@gf.cell_with_module_name(tags=["texts"])
def text_rectangular_multi_layer(
    text: str = "abcd",
    layers: LayerSpecs = ("WG", "M1", "M2", "MTOP"),
    text_factory: ComponentSpec = text_rectangular,
    **kwargs: Any,
) -> Component:
    pass


text_rectangular_mini = partial(text_rectangular, size=1)
