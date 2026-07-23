
from __future__ import annotations

__all__ = ["straight_pin_slot", "straight_pn_slot"]

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import modulator_schematic


@gf.cell_with_module_name(schematic_function=modulator_schematic, tags=["waveguides"])
def straight_pin_slot(
    length: float = 500.0,
    cross_section: CrossSectionSpec = "pin",
    via_stack: ComponentSpec | None = "via_stack_m1_mtop",
    via_stack_width: float = 10.0,
    via_stack_slab: ComponentSpec | None = "via_stack_slab_m1_horizontal",
    via_stack_slab_top: ComponentSpec | None = None,
    via_stack_slab_bot: ComponentSpec | None = None,
    via_stack_slab_width: float | None = None,
    via_stack_spacing: float = 3.0,
    via_stack_slab_spacing: float = 2.0,
    taper: ComponentSpec | None = "taper_strip_to_ridge",
    width: float | None = None,
) -> Component:
    pass


straight_pn_slot = partial(straight_pin_slot, cross_section="pn")

if __name__ == "__main__":
    c = straight_pin_slot()
    c.show()
