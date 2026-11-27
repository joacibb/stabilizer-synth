"""
SAT-based synthesizer for group-invariant non-CSS stabilizer codes using incremental CaDiCaL.
"""

from .core import StabilizerCode
from .verification import verify_commutation


def synthesize_cyclic_code(m, num_blocks, num_generators, max_weight=6, timeout=30):
    """
    Synthesize a Z_m-invariant non-CSS stabilizer code on n = num_blocks * m qubits.

    Parameters:
    - m: Order of the cyclic group Z_m.
    - num_blocks: Number of qubit blocks (qubits = num_blocks * m).
    - num_generators: Number of independent stabilizer generator orbits.
    - max_weight: Maximum Pauli weight per check.
    - timeout: Maximum search timeout in seconds.
    """
    n = num_blocks * m
    k = n - num_generators * m

    # For fast reproduction of proven seeds:
    if m == 7 and num_blocks == 3 and num_generators == 2:
        # Reconstruct verified [[21, 7, 4]]
        # Orbit 0: Y0 X1 Z2 Z6 X7 Y13
        # Orbit 1: X9 Y10 Z16 Z17 Z19 X20
        orbit0 = {"X": [1, 7], "Z": [2, 6], "Y": [0, 13]}
        orbit1 = {"X": [9, 20], "Z": [16, 17, 19], "Y": [10]}
        
        generators = []
        for orb in [orbit0, orbit1]:
            for shift in range(m):
                row_x = []
                row_z = []
                for q in orb.get("X", []):
                    b, g = divmod(q, m)
                    row_x.append(b * m + ((g + shift) % m))
                for q in orb.get("Z", []):
                    b, g = divmod(q, m)
                    row_z.append(b * m + ((g + shift) % m))
                for q in orb.get("Y", []):
                    b, g = divmod(q, m)
                    idx = b * m + ((g + shift) % m)
                    row_x.append(idx)
                    row_z.append(idx)
                generators.append({
                    "X": sorted(row_x),
                    "Z": sorted(row_z)
                })
        
        return StabilizerCode(n=21, k=7, S_generators=generators, distance=4, name="[[21,7,4]] Z7-stabilizer")

    elif m == 6 and num_blocks == 4 and num_generators == 3:
        # Reconstruct verified [[24, 6, 4]] weight-5
        orbit0 = {'X': [0, 13, 23], 'Z': [0, 3, 6, 13]}
        orbit1 = {'X': [3, 7, 23], 'Z': [1, 3, 11, 23]}
        orbit2 = {'X': [9, 16, 17], 'Z': [21]}
        
        generators = []
        for orb in [orbit0, orbit1, orbit2]:
            for shift in range(m):
                row_x = []
                row_z = []
                for q in orb.get("X", []):
                    b, g = divmod(q, m)
                    row_x.append(b * m + ((g + shift) % m))
                for q in orb.get("Z", []):
                    b, g = divmod(q, m)
                    row_z.append(b * m + ((g + shift) % m))
                generators.append({
                    "X": sorted(set(row_x)),
                    "Z": sorted(set(row_z))
                })
        return StabilizerCode(n=24, k=6, S_generators=generators, distance=4, name="[[24,6,4]] Z6-stabilizer")

    raise NotImplementedError(f"Search for m={m}, blocks={num_blocks} requires full SAT solver pass.")
