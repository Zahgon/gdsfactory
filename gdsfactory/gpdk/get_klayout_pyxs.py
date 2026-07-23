
from __future__ import annotations

import pathlib

from gdsfactory.gpdk import LAYER

nm = 1e-3


def layer_to_string(layer: tuple[int, int]) -> str:
    pass


def get_klayout_pyxs(
    t_box: float = 1.0,
    t_slab: float = 90 * nm,
    t_si: float = 0.22,
    t_ge: float = 0.4,
    t_nitride: float = 0.4,
    h_etch1: float = 0.07,
    h_etch2: float = 0.06,
    h_etch3: float = 0.09,
    t_clad: float = 0.6,
    t_m1: float = 0.5,
    t_m2: float = 0.5,
    t_m3: float = 2.0,
    gap_m1_m2: float = 0.6,
    gap_m2_m3: float = 0.3,
    t_heater: float = 0.1,
    gap_oxide_nitride: float = 0.82,
    t_m1_oxide: float = 0.6,
    t_m2_oxide: float = 2.0,
    t_m3_oxide: float = 0.5,
    layer_wg: tuple[int, int] = LAYER.WG,
    layer_fc: tuple[int, int] = LAYER.SLAB150,
    layer_rib: tuple[int, int] = LAYER.SLAB90,
    layer_n: tuple[int, int] = LAYER.N,
    layer_np: tuple[int, int] = LAYER.NP,
    layer_npp: tuple[int, int] = LAYER.NPP,
    layer_p: tuple[int, int] = LAYER.P,
    layer_pp: tuple[int, int] = LAYER.PP,
    layer_ppp: tuple[int, int] = LAYER.PPP,
    layer_PDPP: tuple[int, int] = LAYER.GEP,
    layer_nitride: tuple[int, int] = LAYER.WGN,
    layer_Ge: tuple[int, int] = LAYER.GE,
    layer_GePPp: tuple[int, int] = LAYER.GEP,
    layer_GeNPP: tuple[int, int] = LAYER.GEN,
    layer_viac: tuple[int, int] = LAYER.VIAC,
    layer_viac_slot: tuple[int, int] = LAYER.VIAC,
    layer_m1: tuple[int, int] = LAYER.M1,
    layer_mh: tuple[int, int] = LAYER.HEATER,
    layer_via1: tuple[int, int] = LAYER.VIA1,
    layer_m2: tuple[int, int] = LAYER.M2,
    layer_via2: tuple[int, int] = LAYER.VIA2,
    layer_m3: tuple[int, int] = LAYER.M3,
    layer_open: tuple[int, int] = LAYER.PADOPEN,
) -> str:
    pass


if __name__ == "__main__":
    script = get_klayout_pyxs(
        t_box=2.0,
        t_slab=110 * nm,
        t_si=220 * nm,
        t_ge=400 * nm,
        t_nitride=400 * nm,
        h_etch1=0.07,
        h_etch2=0.06,
        h_etch3=0.09,
        t_clad=0.6,
        t_m1=0.5,
        t_m2=0.5,
        t_m3=2.0,
        gap_m1_m2=0.6,
        gap_m2_m3=0.3,
        t_heater=0.1,
        gap_oxide_nitride=0.82,
        t_m1_oxide=0.6,
        t_m2_oxide=2.0,
        t_m3_oxide=0.5,
        layer_wg=LAYER.WG,
        layer_fc=LAYER.SLAB150,
        layer_rib=LAYER.SLAB90,
        layer_n=LAYER.N,
        layer_np=LAYER.NP,
        layer_npp=LAYER.NPP,
        layer_p=LAYER.P,
        layer_pp=LAYER.PP,
        layer_ppp=LAYER.PPP,
        layer_PDPP=LAYER.GEP,
        layer_nitride=LAYER.WGN,
        layer_Ge=LAYER.GE,
        layer_GePPp=LAYER.GEP,
        layer_GeNPP=LAYER.GEN,
        layer_viac=LAYER.VIAC,
        layer_viac_slot=LAYER.VIAC,
        layer_m1=LAYER.M1,
        layer_mh=LAYER.HEATER,
        layer_via1=LAYER.VIA1,
        layer_m2=LAYER.M2,
        layer_via2=LAYER.VIA2,
        layer_m3=LAYER.M3,
        layer_open=LAYER.PADOPEN,
    )

    script_path = (
        pathlib.Path(__file__).parent.absolute()
        / "klayout"
        / "tech"
        / "xsection_planarized.pyxs"
    )
    print(script_path)
    script_path.write_text(script)
    print(script)
