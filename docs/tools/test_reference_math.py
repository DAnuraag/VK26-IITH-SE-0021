"""Tests of documentation examples, not physical/software acceptance results."""
import unittest
from reference_math import (
    PowerPoint, power_w, shunt_values, ina226_scaling, irradiance_w_m2,
    shortfall_fraction, energy_interval, persistence_series, raw_storage_bytes,
    thermal_limit_c_per_w, cantilever_screen, confusion_metrics,
    waiting_time_reduction,
)


class DocumentationArithmeticTests(unittest.TestCase):
    def point(self, t, p=60.0, valid=True, boot="reference-boot", node="reference-node"):
        return PowerPoint(node, boot, t, p, valid)

    def test_hmi_power_fixture(self):
        self.assertAlmostEqual(power_w(21.6, 3.2), 69.12)

    def test_power_rejects_nonfinite(self):
        with self.assertRaises(ValueError):
            power_w(float("nan"), 1)

    def test_power_rejects_boolean(self):
        with self.assertRaises(ValueError):
            power_w(True, 1)

    def test_shunt_drop_at_five_amperes(self):
        self.assertAlmostEqual(shunt_values(5)["voltage_v"], 0.050)

    def test_shunt_dissipation_at_five_amperes(self):
        self.assertAlmostEqual(shunt_values(5)["dissipation_w"], 0.25)

    def test_ina_calibration_scaling(self):
        self.assertAlmostEqual(ina226_scaling()["cal_ideal"], 2048)

    def test_ina_power_lsb(self):
        self.assertAlmostEqual(ina226_scaling()["power_lsb_w"], 0.00625)

    def test_nominal_pyranometer_conversion(self):
        self.assertAlmostEqual(irradiance_w_m2(160), 800)

    def test_hmi_shortfall_fixture(self):
        self.assertAlmostEqual(shortfall_fraction(88.3, 69.12, 1), 0.2172140430)

    def test_denominator_floor_gates_analysis(self):
        self.assertIsNone(shortfall_fraction(0.5, 0.2, 1))

    def test_one_hour_constant_power(self):
        result = energy_interval(self.point(0), self.point(3600), 3600)
        self.assertAlmostEqual(result["wh"], 60)
        self.assertEqual(result["reason"], "valid")

    def test_trapezoid_example(self):
        result = energy_interval(self.point(0, 60), self.point(5, 80), 5)
        self.assertAlmostEqual(result["wh"], 70 * 5 / 3600)

    def test_invalid_endpoint_excludes_elapsed_time(self):
        result = energy_interval(self.point(0), self.point(1, None, False))
        self.assertEqual(result["wh"], 0)
        self.assertEqual(result["excluded_s"], 1)
        self.assertEqual(result["reason"], "invalid_endpoint")

    def test_long_gap_is_not_interpolated(self):
        result = energy_interval(self.point(0), self.point(10), 2)
        self.assertEqual(result["excluded_s"], 10)
        self.assertEqual(result["reason"], "gap_exceeds_policy")

    def test_boot_boundary_is_not_bridged(self):
        result = energy_interval(self.point(0), self.point(1, boot="new-boot"))
        self.assertEqual(result["reason"], "identity_discontinuity")

    def test_node_boundary_is_not_bridged(self):
        result = energy_interval(self.point(0), self.point(1, node="other-node"))
        self.assertEqual(result["reason"], "identity_discontinuity")

    def test_nonpositive_time_adds_no_energy(self):
        result = energy_interval(self.point(10), self.point(9))
        self.assertEqual(result["reason"], "nonpositive_time")
        self.assertEqual(result["wh"], 0)

    def test_first_qualifying_sample_starts_at_zero(self):
        result = persistence_series([120], [0.20], [True])
        self.assertEqual(result[0]["persistence_s"], 0)
        self.assertFalse(result[0]["qualified_alert"])

    def test_180_seconds_reached_at_300(self):
        times = list(range(120, 301))
        result = persistence_series(times, [0.20] * len(times), [True] * len(times))
        self.assertFalse(result[-2]["qualified_alert"])
        self.assertTrue(result[-1]["qualified_alert"])
        self.assertEqual(result[-1]["persistence_s"], 180)

    def test_gate_loss_resets_reference_timer(self):
        result = persistence_series([0, 1, 2], [0.2] * 3, [True, False, True])
        self.assertEqual(result[-1]["persistence_s"], 0)

    def test_gap_resets_reference_timer(self):
        result = persistence_series([0, 1, 10], [0.2] * 3, [True] * 3)
        self.assertEqual(result[-1]["persistence_s"], 0)

    def test_threshold_is_strictly_greater_than(self):
        result = persistence_series([0, 1], [0.15, 0.15], [True, True])
        self.assertFalse(any(r["qualified_alert"] for r in result))

    def test_raw_retention_model(self):
        self.assertEqual(raw_storage_bytes(), 5_184_000_000)

    def test_verbose_payload_changes_capacity(self):
        self.assertEqual(raw_storage_bytes(payload_bytes=400), 10_368_000_000)

    def test_effective_thermal_screen(self):
        self.assertAlmostEqual(thermal_limit_c_per_w(), 20 / 3)

    def test_cantilever_stress(self):
        self.assertAlmostEqual(cantilever_screen()["stress_mpa"], 6.6666666667)

    def test_cantilever_deflection(self):
        self.assertAlmostEqual(cantilever_screen()["deflection_mm"], 0.0085882984)

    def test_confusion_fixture_is_not_a_validation_result(self):
        result = confusion_metrics(18, 2, 3, 77)
        self.assertAlmostEqual(result["precision"], 0.90)
        self.assertAlmostEqual(result["recall"], 18 / 21)

    def test_no_events_has_undefined_rates(self):
        self.assertTrue(all(v is None for v in confusion_metrics(0, 0, 0, 0).values()))

    def test_negative_event_counts_rejected(self):
        with self.assertRaises(ValueError):
            confusion_metrics(-1, 0, 0, 0)

    def test_modeled_wait_reduction(self):
        self.assertAlmostEqual(waiting_time_reduction(), 0.9708333333333333)

    def test_invalid_assumptions_rejected(self):
        for calculation in [
            lambda: shunt_values(1, 0),
            lambda: ina226_scaling(0, 0.010),
            lambda: irradiance_w_m2(100, 0),
            lambda: thermal_limit_c_per_w(0),
            lambda: waiting_time_reduction(0),
        ]:
            with self.subTest(calculation=calculation):
                with self.assertRaises(ValueError):
                    calculation()


if __name__ == "__main__":
    unittest.main()
