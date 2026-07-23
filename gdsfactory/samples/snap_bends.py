
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    c = gf.Component()
    b1 = c << gf.c.bend_euler(angle=37)
    b2 = c << gf.c.bend_euler(angle=37)
    b2.connect("o1", b1.ports["o2"])
    c.show()
