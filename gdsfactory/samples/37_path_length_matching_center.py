
from __future__ import annotations

import kfactory as kf

import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    xs = gf.get_cross_section("strip")
    layer = gf.get_layer(xs.sections[0].layer)

    start_ports = [
        gf.Port(
            name=f"start_{i}",
            center=(i * 300, -i * 150),
            orientation=90,
            layer=layer,
            width=0.5,
        )
        for i in range(3)
    ]
    end_ports = [
        gf.Port(
            name=f"end_{i}",
            center=(x, 500),
            orientation=270,
            layer=layer,
            width=0.5,
        )
        for i, x in enumerate([230, 700, 1000])
    ]

    c = gf.Component()
    gf.routing.route_bundle(
        c,
        start_ports,
        end_ports,
        start_straight_length=300,
        cross_section="strip",
        name="match_center",
        constraints=[
            kf.schematic.PathLengthMatch(
                route_names=["match_center"],
                element=1,
                loop_side=gf.routing.LoopSide.center,
                loops=2,
                loop_position=gf.routing.LoopPosition.center,
                all=True,
            )
        ],
    )

    c.show()
