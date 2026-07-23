
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.typings import LayerSpec

gf.gpdk.PDK.activate()


@gf.cell
def straight_wide(
    length: float = 5.0, width: float = 1.0, layer: LayerSpec = (1, 0)
) -> gf.Component:
    pass



if __name__ == "__main__":
    c = gf.Component()

    _wg1 = straight_wide(length=10, width=1, layer=(1, 0))
    _wg2 = straight_wide(length=12, width=2, layer=(2, 0))

    wg1 = c.add_ref(_wg1)  # Using the function add_ref()
    wg2 = c << _wg2  # Using the << operator which is identical to add_ref()

    wg3 = c.add_ref(straight_wide(length=14, width=3, layer=(3, 0)))

    c.show()  # show it in Klayout
