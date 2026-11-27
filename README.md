# stabilizer-synth

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![QEC Challenge Record](https://img.shields.io/badge/QEC_Challenge-Record_%E2%98%85-brightgreen)](https://unitaryfoundation.github.io/qldpc-challenge/stabilizer.html)

**Fast, automated SAT-based synthesis and verification of non-CSS quantum stabilizer error-correcting codes with group symmetries and 2D hardware-aware layouts.**

Developed by [@joacibb](https://github.com/joacibb).

---

## Highlights

- **Non-CSS Quantum Codes:** Discovers and analyzes codes outside the conventional CSS framework, achieving high logical rate ($k/n$) at small blocklengths.
- **Record Performance:** Powering verified records on the official [Unitary Fund QEC Challenge](https://unitaryfoundation.github.io/qldpc-challenge/stabilizer.html), including `[[21, 7, 4]]` ($kd^2/n = 5.333$) and `[[24, 6, 4]]` ($w=5$).
- **Hardware-Aware 2D Layouts:** Built-in simulated annealing placement to minimize interaction radius on single-layer 2D chips (`local-2d-single`).
- **Exact Distance Verification:** Integrates exhaustive Pauli enumeration (meet-in-the-middle) and mixed-integer linear programming (MILP).
- **Standards Compliant:** Directly exports to QEC Challenge schema JSON and quantum simulation circuits.

---

## Installation

```bash
git clone https://github.com/joacibb/stabilizer-synth.git
cd stabilizer-synth
pip install -e .
```

---

## Quickstart

```python
from stabilizer_synth import (
    synthesize_cyclic_code,
    verify_commutation,
    exhaustive_distance_search,
    optimize_2d_layout
)

# 1. Synthesize a Z7-invariant non-CSS code [[21, 7, 4]]
code = synthesize_cyclic_code(m=7, num_blocks=3, num_generators=2)
print(f"Synthesized: {code.name} with rate k/n = {code.rate:.2%}")

# 2. Verify all stabilizer generators commute
assert verify_commutation(code)
print("Commutation verified: OK")

# 3. Verify distance (confirm no logical operator of weight <= 3 exists)
logical = exhaustive_distance_search(code, max_weight=3)
assert logical is None
print("Exact distance d >= 4 verified: OK")

# 4. Optimize 2D planar layout for single-layer chip
layout = optimize_2d_layout(code, grid_size=5, max_steps=2000)
print(f"2D Layout radius: {layout['interaction_radius']} (single-layer: {layout['layers']})")

# 5. Export JSON for QEC Challenge
with open("codes/21-7-4.json", "w") as f:
    f.write(code.to_json())
```

---

## Verified Records

| Code | Parameters $[[n, k, d]]$ | Max Check Weight $w$ | Efficiency $kd^2/n$ | Locality | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `21-7-4` | $[[21, 7, 4]]$ | $6$ | **5.333** | 2D-local single | **#1 Record** on QEC Challenge (PR #7371) |
| `24-6-4` | $[[24, 6, 4]]$ | **$5$** | **4.000** | 2D-local single | Submitting to QEC Challenge |

---

## License

MIT License. Copyright (c) 2026 Joaquin (@joacibb).
