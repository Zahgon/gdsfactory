
import gdsfactory as gf

gf.gpdk.PDK.activate()


@gf.cell
def sample_routing_auto_taper_slot() -> gf.Component:
    pass


@gf.cell
def sample_routing_auto_taper_trenches() -> gf.Component:
    pass


if __name__ == "__main__":
    c = sample_routing_auto_taper_trenches()
    c.show()
