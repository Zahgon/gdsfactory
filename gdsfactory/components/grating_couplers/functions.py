from __future__ import annotations

from typing import Any

import numpy as np
import numpy.typing as npt
from numpy import sin, sqrt

import gdsfactory as gf
from gdsfactory.functions import DEG2RAD, extrude_path

neff_ridge = 2.8
neff_shallow = 2.5


def ellipse_arc(
    a: float,
    b: float,
    x0: float,
    theta_min: float,
    theta_max: float,
    angle_step: float = 0.5,
) -> npt.NDArray[np.floating[Any]]:
    pass


def grating_tooth_points(
    ap: float,
    bp: float,
    xp: float,
    width: float,
    taper_angle: float,
    spiked: bool = True,
    angle_step: float = 1.0,
) -> npt.NDArray[np.floating[Any]]:
    pass


def grating_taper_points(
    a: float,
    b: float,
    x0: float,
    taper_length: float,
    taper_angle: float,
    wg_width: float,
    angle_step: float = 1.0,
) -> npt.NDArray[np.floating[Any]]:
    pass


def get_grating_period_curved(
    fiber_angle: float = 15.0,
    wavelength: float = 1.55,
    n_slab: float = (neff_ridge + neff_shallow) / 2,
    n_clad: float = 1.0,
) -> tuple[float, float]:
    pass


def get_grating_period(
    fiber_angle: float = 13.45,
    wavelength: float = 1.55,
    neff_high: float = neff_ridge,
    neff_low: float = neff_shallow,
    n_clad: float = 1.45,
) -> float:
    pass
