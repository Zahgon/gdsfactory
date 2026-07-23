
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


@gf.cell
def test_north_to_south(layer: tuple[int, int] = (1, 0)) -> gf.Component:
    pass


if __name__ == "__main__":
    c = test_north_to_south()
    c.show()
