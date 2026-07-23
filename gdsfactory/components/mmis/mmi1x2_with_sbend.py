__all__ = ["mmi1x2_with_sbend", "mmi_widths"]

from typing import cast

import numpy as np
import numpy.typing as npt

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentFactory, CrossSectionSpec

from .._schematic import mmi_1x2_schematic
from ..bends.bend_s import bend_s


def mmi_widths(t: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    pass


@gf.cell_with_module_name(schematic_function=mmi_1x2_schematic, tags=["mmis"])
def mmi1x2_with_sbend(
    with_sbend: bool = True,
    s_bend: ComponentFactory = bend_s,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
