
from __future__ import annotations

from functools import partial
from typing import Any

import gdsfactory as gf

gf.gpdk.PDK.activate()


def straight_wide1(width: float = 10, **kwargs: Any) -> gf.Component:
    pass


straight_wide2 = partial(gf.components.straight, width=10)


if __name__ == "__main__":
    c = straight_wide2()
    c.show()
