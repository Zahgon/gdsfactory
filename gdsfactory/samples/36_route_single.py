
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    cell_names = [
        "loop_mirror",
        "mzi_pads_center",
        "straight_heater_meander",
        "straight_heater_meander_doped",
    ]
    c = gf.pack([gf.get_component(name) for name in cell_names])[0]
    c.show()
