
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


@gf.cell
def mzi_with_bend(radius: float = 10) -> gf.Component:
    pass


if __name__ == "__main__":
    c = mzi_with_bend(radius=50)
    c.show()
