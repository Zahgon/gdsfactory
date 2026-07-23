
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


@gf.vcell
def snap_bends_sample() -> gf.ComponentAllAngle:
    pass


if __name__ == "__main__":
    c = snap_bends_sample()
    c.show()
