
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import ComponentFactory

gf.gpdk.PDK.activate()


@gf.cell
def pads_correct(
    pad: ComponentFactory = gf.components.pad, cross_section: str = "metal3"
) -> gf.Component:
    pass


@gf.cell
def pads_shorted(
    pad: ComponentFactory = gf.components.pad, cross_section: str = "metal3"
) -> gf.Component:
    pass


if __name__ == "__main__":
    c = pads_shorted()
    c.show()
    gdspath = c.write_gds()



