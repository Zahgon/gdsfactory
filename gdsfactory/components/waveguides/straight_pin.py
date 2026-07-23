
from __future__ import annotations

__all__ = ["straight_pin", "straight_pn"]

from functools import partial

import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.cross_section import pin
from gdsfactory.typings import ComponentSpec, CrossSectionSpec

from .._schematic import modulator_schematic


@gf.cell_with_module_name(schematic_function=modulator_schematic, tags=["waveguides"])
def straight_pin(
    length: float = 500.0,
    cross_section: CrossSectionSpec = pin,
    via_stack: ComponentSpec = "via_stack_slab_m3",
    via_stack_width: float = 10.0,
    via_stack_spacing: float = 2,
    taper: ComponentSpec | None = "taper_strip_to_ridge",
) -> Component:
    pass


straight_pn = partial(straight_pin, cross_section="pn", length=2000)

if __name__ == "__main__":
    c = straight_pin()
    c.show()
