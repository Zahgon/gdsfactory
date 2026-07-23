
from __future__ import annotations

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    c = gf.Component()
    c1 = c << gf.components.mmi2x2()
    c2 = c << gf.components.mmi2x2()
    c2.move((200, 240))

    gf.routing.route_bundle(
        c,
        [c1.ports["o3"], c1.ports["o4"]],
        [c2.ports["o2"], c2.ports["o1"]],
        waypoints=[(60, 100), (150, 200)],
        separation=5.0,
        cross_section="strip",
        sort_ports=True,
    )
    c.show()
