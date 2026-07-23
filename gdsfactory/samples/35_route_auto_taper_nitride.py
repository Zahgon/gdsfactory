
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.routing.auto_taper import auto_taper_to_cross_section

gf.gpdk.PDK.activate()


@gf.cell
def silicon_nitride_strip(width_nitride: float = 1) -> gf.Component:
    pass


if __name__ == "__main__":
    c = silicon_nitride_strip(width_nitride=1)
    c.show()
