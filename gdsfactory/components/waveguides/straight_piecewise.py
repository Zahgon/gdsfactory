__all__ = ["straight_piecewise"]

from collections.abc import Sequence
from typing import Any

import numpy as np
import numpy.typing as npt

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.cross_section import Section
from gdsfactory.path import Path
from gdsfactory.typings import LayerSpec


@gf.cell_with_module_name(tags=["waveguides"])
def straight_piecewise(
    x: Sequence[float] | Path,
    widths: Sequence[float],
    layer: LayerSpec,
    sections: Sequence[Section] | None = None,
    port_names: tuple[str | None, str | None] = ("o1", "o2"),
    name: str = "core",
    **kwargs: Any,
) -> Component:
    pass
