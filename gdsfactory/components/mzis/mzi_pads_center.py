from __future__ import annotations

__all__ = ["mzi_pads_center"]

from typing import Any

import gdsfactory as gf
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import ckt_schematic


@gf.cell_with_module_name(schematic_function=ckt_schematic, tags=["mzis"])
def mzi_pads_center(
    ps_top: ComponentSpec = "straight_heater_metal",
    ps_bot: ComponentSpec = "straight_heater_metal",
    mzi: ComponentSpec = "mzi",
    pad: ComponentSpec = "pad_small",
    length_x: float = 500,
    length_y: float = 40,
    mzi_sig_top: str | None = "top_r_e2",
    mzi_gnd_top: str | None = "top_l_e2",
    mzi_sig_bot: str | None = "bot_l_e2",
    mzi_gnd_bot: str | None = "bot_r_e2",
    pad_sig_bot: str = "e1_1_1",
    pad_sig_top: str = "e3_1_3",
    pad_gnd_bot: str = "e4_1_2",
    pad_gnd_top: str = "e2_1_2",
    delta_length: float = 40.0,
    cross_section: CrossSectionSpec = "strip",
    cross_section_metal: CrossSectionSpec = "metal_routing",
    pad_pitch: float | str = "pad_pitch",
    auto_taper: bool = False,
    **kwargs: Any,
) -> gf.Component:
    pass
