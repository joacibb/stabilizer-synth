from stabilizer_synth import synthesize_cyclic_code, verify_commutation, exhaustive_distance_search, optimize_2d_layout


def test_21_7_4_code():
    code = synthesize_cyclic_code(m=7, num_blocks=3, num_generators=2)
    assert code.n == 21
    assert code.k == 7
    assert code.distance == 4
    assert code.max_check_weight == 6
    assert abs(code.kd2_over_n - 5.3333) < 0.01

    # Commutation test
    assert verify_commutation(code)

    # Exhaustive distance verification (no logical of weight <= 3)
    logical = exhaustive_distance_search(code, max_weight=3)
    assert logical is None, f"Found unexpected logical below distance 4: {logical}"


def test_24_6_4_weight5_code():
    code = synthesize_cyclic_code(m=6, num_blocks=4, num_generators=3)
    assert code.n == 24
    assert code.k == 6
    assert code.distance == 4
    assert code.max_check_weight == 5
    assert code.kd2_over_n == 4.0

    # Commutation test
    assert verify_commutation(code)

    # Test 2D layout optimization
    layout = optimize_2d_layout(code, grid_size=5, max_steps=500, seed=42)
    assert layout["layers"] == 1
    assert len(layout["coordinates"]) == 24
    assert layout["interaction_radius"] <= 5.0
