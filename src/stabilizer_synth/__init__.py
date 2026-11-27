"""
stabilizer-synth: Synthesis and verification of non-CSS quantum stabilizer codes via SAT solvers.
"""

from .core import StabilizerCode
from .synthesis import synthesize_cyclic_code
from .verification import verify_commutation, exhaustive_distance_search, milp_exact_distance
from .layout import optimize_2d_layout

__version__ = "0.1.0"
__all__ = [
    "StabilizerCode",
    "synthesize_cyclic_code",
    "verify_commutation",
    "exhaustive_distance_search",
    "milp_exact_distance",
    "optimize_2d_layout",
]
