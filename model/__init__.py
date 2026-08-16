"""Twelve-State Capability Convergence Model (12SCCM)."""

from .dimensions import STATES, CAPABILITIES
from .recognition import recognition_intensity, recognition_level, concentration_index
from .network import effective_dependency
from .convergence import capability_deficit, dispersion
from .stability import systemic_stability

__all__ = [
    "STATES", "CAPABILITIES", "recognition_intensity", "recognition_level",
    "concentration_index", "effective_dependency", "capability_deficit",
    "dispersion", "systemic_stability",
]
