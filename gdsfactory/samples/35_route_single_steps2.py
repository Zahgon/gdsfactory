
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    c = gf.Component()
    mmi1 = c << gf.components.mmi1x2()
    mmi2 = c << gf.components.mmi1x2()
    mmi2.move((200, 50))

    gf.routing.route_single(
        c,
        mmi1.ports["o2"],
        mmi2.ports["o1"],
        steps=[{"dx": 100}],
        cross_section="strip",
    )
    c.show()
