
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.port import Port

gf.gpdk.PDK.activate()


@gf.cell(cache={})
def test_connect_corner(N: int = 6, config: str = "A") -> gf.Component:
    pass


if __name__ == "__main__":
    c = test_connect_corner(config="A")
    c.show()
