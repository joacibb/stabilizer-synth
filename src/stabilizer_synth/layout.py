import math
import random
import numpy as np


def optimize_2d_layout(code, grid_size=5, max_steps=20000, seed=42):
    """
    Simulated annealing to assign n qubits to integer (x, y) coordinates on a 2D grid
    minimizing the maximum interaction radius of the stabilizer generators.
    """
    n = code.n
    random.seed(seed)
    np.random.seed(seed)

    # Grid positions: (x, y) in range(grid_size)
    available = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    if len(available) < n:
        grid_size = math.ceil(math.sqrt(n))
        available = [(x, y) for x in range(grid_size) for y in range(grid_size)]

    # Initial random assignment
    coords = random.sample(available, n)

    # Precompute generator supports (qubits in each generator)
    supports = [list(set(g.get("X", []) + g.get("Z", []))) for g in code.S_generators]

    def max_diameter(current_coords):
        max_d2 = 0.0
        for sup in supports:
            for i in range(len(sup)):
                q1 = sup[i]
                x1, y1 = current_coords[q1]
                for j in range(i + 1, len(sup)):
                    q2 = sup[j]
                    x2, y2 = current_coords[q2]
                    d2 = (x1 - x2)**2 + (y1 - y2)**2
                    if d2 > max_d2:
                        max_d2 = d2
        return math.sqrt(max_d2)

    best_coords = list(coords)
    best_rad = max_diameter(coords)
    curr_rad = best_rad

    temp = 1.0
    cooling = 0.9995

    for step in range(max_steps):
        # Swap two random qubit positions
        i, j = random.sample(range(n), 2)
        coords[i], coords[j] = coords[j], coords[i]
        new_rad = max_diameter(coords)

        delta = new_rad - curr_rad
        if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-6)):
            curr_rad = new_rad
            if curr_rad < best_rad:
                best_rad = curr_rad
                best_coords = list(coords)
        else:
            coords[i], coords[j] = coords[j], coords[i]

        temp *= cooling

    layout_doc = {
        "coordinates": [[int(x), int(y)] for x, y in best_coords],
        "layers": 1,
        "interaction_radius": round(best_rad, 4)
    }
    code.layout = layout_doc
    return layout_doc
