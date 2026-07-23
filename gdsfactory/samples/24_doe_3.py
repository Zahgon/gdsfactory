
import gdsfactory as gf

gf.gpdk.PDK.activate()


if __name__ == "__main__":
    c = gf.components.pack_doe_grid(
        gf.components.straight,
        settings={"length": (5, 5)},
        function=gf.routing.add_fiber_array,
    )
    c.show()
