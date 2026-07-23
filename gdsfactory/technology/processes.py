from pydantic.dataclasses import dataclass

from gdsfactory.technology.layer_views import Layer


@dataclass(kw_only=True)
class ProcessStep:

    name: str | None


@dataclass(kw_only=True)
class Lithography(ProcessStep):

    layer: Layer | None = None
    layers_or: list[Layer] | None = None
    layers_diff: list[Layer] | None = None
    layers_and: list[Layer] | None = None
    layers_xor: list[Layer] | None = None
    resist_thickness: float | None = 0
    positive_tone: bool = True
    planarization_height: float | None = None


@dataclass(kw_only=True)
class Grow(Lithography):

    thickness: float
    material: str
    type: str
    rate: float | None = None


@dataclass(kw_only=True)
class Etch(Lithography):

    material: str
    depth: float
    type: str = "anisotropic"
    rate: float | None = None


@dataclass(kw_only=True)
class ImplantPhysical(Lithography):

    ion: str
    energy: float
    dose: float
    tilt: float | None = None
    twist: float | None = None
    rotation: float | None = None


@dataclass(kw_only=True)
class ImplantGaussian(Lithography):

    ion: str
    peak_conc: float
    range: float
    vertical_straggle: float | None = None
    lateral_straggle: float | None = None


@dataclass(kw_only=True)
class DopingConstant(Lithography):

    ion: str
    peak_conc: float
    zmin: float
    zmax: float | None = None
    into_materials: list[str]


@dataclass(kw_only=True)
class Anneal(ProcessStep):

    time: float
    temperature: float


@dataclass(kw_only=True)
class Planarize(ProcessStep):

    height: float = 0


@dataclass(kw_only=True)
class ArbitraryStep(ProcessStep):

    info: str
