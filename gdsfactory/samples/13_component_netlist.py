from __future__ import annotations

import gdsfactory as gf
from gdsfactory.component import Component

gf.gpdk.PDK.activate()


@gf.cell
def netlist_yaml() -> Component:
    pass


def test_netlist_yaml_sample() -> None:
    pass


if __name__ == "__main__":
    c = netlist_yaml()
    c.show()
