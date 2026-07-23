import gdsfactory as gf

gf.gpdk.PDK.activate()


@gf.cell
def mzi_with_bend(radius: float = 10) -> gf.Component:
    pass


if __name__ == "__main__":
    c = mzi_with_bend(radius=100)
    c = gf.routing.add_fiber_array(c, pitch=250, fanout_length=100)
    c.show()
