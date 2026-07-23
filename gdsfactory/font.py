
from __future__ import annotations

from typing import Any

import freetype
import numpy as np
import numpy.typing as npt
from matplotlib import font_manager
from matplotlib.path import Path

from gdsfactory.boolean import boolean
from gdsfactory.component import Component

_cached_fonts: dict[str, freetype.Face] = {}

try:
    import freetype
except ImportError:
    import warnings

    warnings.warn(
        "gdsfactory requires freetype to use real fonts. "
        "Either use the default DEPLOF font or install the freetype package:"
        "\n\n $ pip install freetype-py"
        "\n\n (Note: Windows users may have to find and replace the 'libfreetype.dll' "
        "file in their Python package directory /freetype/ with the correct one"
        "from here: https://github.com/ubawurinna/freetype-windows-binaries"
        " -- be sure to rename 'freetype.dll' to 'libfreetype.dll') ",
        stacklevel=2,
    )


def _get_font_by_file(file: str) -> freetype.Face:
    pass


def _get_font_by_name(name: str) -> freetype.Face:
    pass


def _get_glyph(font: freetype.Face, letter: str) -> tuple[Component, float, float]:
    pass


def _polygon_orientation(vertices: npt.NDArray[np.float64]) -> int:
    pass
