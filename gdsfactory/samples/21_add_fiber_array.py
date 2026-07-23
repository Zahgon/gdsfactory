
from __future__ import annotations

import gdsfactory as gf
from gdsfactory.samples.big_device import big_device

gf.gpdk.PDK.activate()


@gf.cell
def big_device_with_gratings() -> gf.Component:
    pass


def test_big_device() -> None:
    pass


if __name__ == "__main__":
    c = big_device_with_gratings()
    c.show()
