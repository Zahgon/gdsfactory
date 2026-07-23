
from __future__ import annotations

__all__ = ["splitter_tree", "switch_tree"]

from functools import partial

import numpy as np

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec, Spacing

from ..mzis import mzi1x2_2x2


@gf.cell_with_module_name(tags=["containers"])
def splitter_tree(
    coupler: ComponentSpec = "mmi1x2",
    noutputs: int = 4,
    spacing: Spacing = (90.0, 50.0),
    bend_s: ComponentSpec | None = "bend_s",
    bend_s_xsize: float | None = None,
    cross_section: CrossSectionSpec = "strip",
) -> gf.Component:
    pass


_mzi1x2_2x2 = partial(
    mzi1x2_2x2,
    combiner="mmi2x2",
    delta_length=0,
    straight_x_top="straight_heater_metal",
    length_x=None,
)

switch_tree = partial(
    splitter_tree,
    coupler=_mzi1x2_2x2,
    spacing=(500, 100),
)
