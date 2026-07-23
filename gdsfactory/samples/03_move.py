
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    c = gf.Component(name="demo")

    wg1 = c << gf.components.straight(length=10, width=1)
    wg2 = c << gf.components.straight(length=10, width=2)

    c.show()
