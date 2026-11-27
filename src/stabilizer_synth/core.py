import json
import numpy as np


class StabilizerCode:
    """
    Representation of an [[n, k, d]] quantum stabilizer code over the Pauli group.
    """

    def __init__(self, n, k, S_generators, distance=None, layout=None, name=""):
        self.n = int(n)
        self.k = int(k)
        self.S_generators = list(S_generators)  # list of dicts with 'X' and 'Z' indices
        self.distance = distance
        self.layout = layout or {}
        self.name = name or f"[[{self.n},{self.k},{self.distance or '?' }]]"

    @property
    def max_check_weight(self):
        """Maximum Pauli weight across all generators."""
        weights = [len(set(g.get("X", []) + g.get("Z", []))) for g in self.S_generators]
        return max(weights) if weights else 0

    @property
    def rate(self):
        """Logical information rate k / n."""
        return self.k / self.n if self.n > 0 else 0.0

    @property
    def kd2_over_n(self):
        """Operational efficiency kd^2 / n."""
        if self.distance and self.n > 0:
            return self.k * (self.distance ** 2) / self.n
        return 0.0

    def to_dict(self):
        """Convert to dictionary matching the QEC challenge schema."""
        doc = {
            "schema_version": "0.7",
            "name": self.name,
            "code_type": "stabilizer",
            "n": self.n,
            "k": self.k,
            "checks": {
                "S": self.S_generators
            },
            "provenance": {
                "harness": "stabilizer-synth",
                "novelty": "unknown"
            }
        }
        if self.distance:
            doc["distance"] = {
                "d": self.distance,
                "P": {
                    "value": self.distance,
                    "confidence": "upper_bound"
                }
            }
        if self.layout:
            doc["locality"] = self.layout
        return doc

    def to_json(self, indent=1):
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_binary_symplectic(self):
        """
        Returns binary symplectic matrix S = (A | B) of shape (num_generators, 2*n).
        """
        m = len(self.S_generators)
        mat = np.zeros((m, 2 * self.n), dtype=np.uint8)
        for i, g in enumerate(self.S_generators):
            for q in g.get("X", []):
                mat[i, q] = 1
            for q in g.get("Z", []):
                mat[i, q + self.n] = 1
        return mat
