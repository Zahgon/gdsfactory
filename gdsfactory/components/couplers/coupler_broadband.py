from __future__ import annotations

__all__ = ["coupler_broadband"]

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import coupler_schematic


@gf.cell_with_module_name(schematic_function=coupler_schematic, tags=["couplers"])
def coupler_broadband(
    w_sc: float = 0.5,  # width of waveguides in the symmetric coupler section
    gap_sc: float = 0.2,  # gap size between the waveguides in the symmetric coupler section
    w_top: float = 0.6,  # width of the top waveguide in the phase control section
    gap_pc: float = 0.3,  # gap size in the phase control section
    legnth_taper: float = 1.0,  # length of the tapers
    bend: ComponentSpec = "bend_euler",
    coupler_straight: ComponentSpec = "coupler_straight",
    length_coupler_straight: float = 12.4,  # optimal L_1 from the 3d fdtd analysis
    lenght_coupler_big_gap: float = 4.7,  # optimal L_2 from the 3d fdtd analysis
    cross_section: CrossSectionSpec = "strip",
    radius: float = 10.0,
) -> Component:
    pass
