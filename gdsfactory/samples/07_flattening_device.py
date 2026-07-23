
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component

gf.gpdk.PDK.activate()


@gf.cell
def flatten_device() -> Component:
    pass


if __name__ == "__main__":
    c = flatten_device()
    c.show()
