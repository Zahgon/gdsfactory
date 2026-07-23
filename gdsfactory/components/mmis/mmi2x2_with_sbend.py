__all__ = ["mmi2x2_with_sbend"]

import numpy as np
import numpy.typing as npt

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentFactory, CrossSectionSpec

from .._schematic import mmi_2x2_schematic
from ..bends.bend_s import bend_s


@gf.cell_with_module_name(schematic_function=mmi_2x2_schematic, tags=["mmis"])
def mmi2x2_with_sbend(
    with_sbend: bool = True,
    s_bend: ComponentFactory = bend_s,
    cross_section: CrossSectionSpec = "strip",
) -> Component:
    pass
