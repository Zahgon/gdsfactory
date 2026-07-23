__all__ = ["coupler_bent"]

import numpy as np

import gdsfactory as gf

from .._schematic import coupler_schematic


@gf.cell_with_module_name(tags=["couplers"])
def coupler_bent_half(
    gap: float = 0.200,
    radius: float = 26,
    length: float = 8.6,
    width1: float = 0.400,
    width2: float = 0.400,
    length_straight: float = 10,
    length_straight_exit: float = 18,
    cross_section: str = "strip",
) -> gf.Component:
    pass


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler_bent(
    gap: float = 0.200,
    radius: float = 26,
    length: float = 8.6,
    width1: float = 0.400,
    width2: float = 0.400,
    length_straight: float = 10,
    cross_section: str = "strip",
) -> gf.Component:
    pass
