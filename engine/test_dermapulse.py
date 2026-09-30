"""
Deterministic Test Suite for DermaPulse AI
Verifies YouCam Skin AI client, Dermal Biometric Engine, Formulation Synthesizer,
and Circadian Regimen Planner modules.
Target Execution Time: 0.000s (sub-millisecond deterministic execution).
"""

import time
import unittest
from dermapulse.engine.youcam_skin_client import YouCamSkinClient
from dermapulse.engine.dermal_biometric_engine import DermalBiometricEngine
from dermapulse.engine.formulation_synthesizer import FormulationSynthesizer
from dermapulse.engine.circadian_regimen_planner import CircadianRegimenPlanner


class TestDermaPulseEngine(unittest.TestCase):
    """Deterministic verification for DermaPulse AI."""

    def setUp(self):
        self.client = YouCamSkinClient(use_sandbox=True)
        self.biometric_engine = DermalBiometricEngine()
        self.formulation_engine = FormulationSynthesizer()
        self.planner = CircadianRegimenPlanner(use_sandbox=True)

    def test_youcam_archetype_retrieval(self):
        """Test retrieving YouCam Skin AI telemetry archetypes."""
        data = self.client.analyze_image(archetype_id="dehydrated_erythema")
        self.assertEqual(data["status"], "success")
        self.assertIn("metrics", data)
        self.assertEqual(data["metrics"]["redness"], 74)

    def test_barrier_integrity_calculation(self):
        """Test Dermal Barrier Integrity Index calculation."""
        metrics_healthy = {"moisture": 80.0, "redness": 10.0, "texture": 15.0, "oiliness": 50.0}
        score_healthy = self.biometric_engine.calculate_barrier_integrity(metrics_healthy)
        self.assertGreater(score_healthy, 85.0)

        metrics_compromised = {"moisture": 25.0, "redness": 85.0, "texture": 70.0, "oiliness": 85.0}
        score_compromised = self.biometric_engine.calculate_barrier_integrity(metrics_compromised)
        self.assertLess(score_compromised, 40.0)

    def test_biological_skin_age_estimation(self):
        """Test biological skin age estimation and status labeling."""
        metrics_aged = {"wrinkles": 80.0, "spots": 85.0, "texture": 75.0}
        age, delta, status = self.biometric_engine.estimate_biological_skin_age(28, metrics_aged)
        self.assertGreater(age, 28)
        self.assertIn("Accelerated", status)

    def test_zone_priorities_detection(self):
        """Test detecting high priority facial zone issues."""
        zones = {
            "t_zone": {"oiliness": 85, "texture": 75, "pore_congestion": "severe"},
            "u_zone_cheeks": {"moisture": 25, "redness": 85, "barrier_state": "compromised"},
            "periorbital": {"dark_circles": 65, "fine_lines": 55}
        }
        priorities = self.biometric_engine.evaluate_zone_priorities(zones)
        self.assertEqual(len(priorities), 3)
        zones_identified = [p["zone"] for p in priorities]
        self.assertTrue(any("T-Zone" in z for z in zones_identified))
        self.assertTrue(any("U-Zone" in z for z in zones_identified))

    def test_formulation_barrier_repair_priority(self):
        """Test that compromised barrier triggers Ceramide repair and contraindicates Retinoids/AHAs."""
        metrics = {"moisture": 30.0, "redness": 75.0, "texture": 60.0, "oiliness": 65.0, "wrinkles": 60.0, "spots": 60.0}
        formulation = self.formulation_engine.synthesize_actives(barrier_integrity=35.0, metrics=metrics)
        self.assertEqual(formulation["barrier_safety_status"], "LIPID_REPAIR_MANDATORY")
        active_names = [a["name"] for a in formulation["selected_actives"]]
        self.assertTrue(any("Ceramide" in n for n in active_names))
        self.assertTrue(any("Centella" in n for n in active_names))
        self.assertGreaterEqual(len(formulation["contraindicated_actives"]), 2)

    def test_formulation_healthy_barrier_tolerance(self):
        """Test that healthy barrier permits collagen-stimulating Retinaldehyde and L-Ascorbic Acid."""
        metrics = {"moisture": 75.0, "redness": 20.0, "texture": 25.0, "oiliness": 50.0, "wrinkles": 65.0, "spots": 55.0}
        formulation = self.formulation_engine.synthesize_actives(barrier_integrity=82.0, metrics=metrics)
        self.assertEqual(formulation["barrier_safety_status"], "OPTIMAL_ACTIVE_TOLERANCE")
        active_names = [a["name"] for a in formulation["selected_actives"]]
        self.assertTrue(any("Retinaldehyde" in n for n in active_names))

    def test_environmental_circadian_scaling(self):
        """Test environmental climate modifiers for UV and Aridity."""
        protocol = self.planner.generate_full_protocol(
            patient_name="Elena Rostova",
            chronological_age=34,
            archetype_id="dehydrated_erythema",
            uv_index=8.5,
            ambient_humidity_pct=25.0,
            pollution_aqi=125
        )
        env_mods = protocol["environmental_conditions"]["active_environmental_modifiers"]
        self.assertEqual(len(env_mods), 3)
        self.assertTrue(any("SPF 50+" in m for m in env_mods))
        self.assertTrue(any("Squalane" in m for m in env_mods))
        self.assertTrue(any("Ectoin" in m for m in env_mods))

    def test_end_to_end_circadian_protocol(self):
        """Test full end-to-end clinical protocol generation."""
        protocol = self.planner.generate_full_protocol(
            patient_name="Marcus Vance",
            chronological_age=42,
            archetype_id="photo_damaged_aging"
        )
        self.assertIn("DERMA-", protocol["protocol_id"])
        self.assertGreaterEqual(len(protocol["circadian_regimen"]["morning_photoprotective_shield"]), 4)
        self.assertGreaterEqual(len(protocol["circadian_regimen"]["evening_cellular_lipid_repair"]), 4)
        self.assertIn("clinical_summary", protocol)


if __name__ == "__main__":
    start = time.perf_counter()
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDermaPulseEngine)
    result = runner.run(suite)
    elapsed = time.perf_counter() - start
    print(f"\n⚡ Total Deterministic Test Execution Time: {elapsed:.3f}s")
