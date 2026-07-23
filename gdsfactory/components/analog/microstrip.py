
from __future__ import annotations

from collections.abc import Sequence

from numpy import exp, log, pi, sinh, sqrt


def _validate_positive(name: str, value: float) -> None:
    pass


def _G_integrand(xip: float, B: float) -> float:
    pass


def _G(xi: float, B: float) -> float:
    pass


def _microstrip_Z(
    wire_width: float, dielectric_thickness: float, eps_r: float
) -> tuple[float, float]:
    pass


def _microstrip_LC_per_meter(
    wire_width: float, dielectric_thickness: float, eps_r: float
) -> tuple[float, float]:
    pass


def _microstrip_Z_with_Lk(
    wire_width: float, dielectric_thickness: float, eps_r: float, Lk_per_sq: float
) -> float:
    pass


def _microstrip_v_with_Lk(
    wire_width: float, dielectric_thickness: float, eps_r: float, Lk_per_sq: float
) -> float:
    pass


def _find_microstrip_wire_width(
    Z_target: float, dielectric_thickness: float, eps_r: float, Lk_per_sq: float
) -> float:
    pass
