import gdsfactory as gf

gf.gpdk.PDK.activate()


@gf.cell
def demo_route_astar_electrical() -> gf.Component:
    pass


if __name__ == "__main__":
    c = demo_route_astar_electrical()
    c.show()
