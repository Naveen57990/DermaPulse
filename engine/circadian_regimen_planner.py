"""
Circadian Regimen Planner
Generates personalized AM/PM multi-phase skincare regimens with real-time environmental scaling.
"""

from typing import Any, Dict, List, Optional
from .youcam_skin_client import YouCamSkinClient
from .dermal_biometric_engine import DermalBiometricEngine
from .formulation_synthesizer import FormulationSynthesizer


class CircadianRegimenPlanner:
    """Orchestrates circadian skincare prescriptions with environmental telemetry."""

    def __init__(self, youcam_api_key: Optional[str] = None, use_sandbox: bool = True):
        self.client = YouCamSkinClient(api_key=youcam_api_key, use_sandbox=use_sandbox)
        self.biometric_engine = DermalBiometricEngine()
        self.formulation_engine = FormulationSynthesizer()

    def generate_full_protocol(
        self,
        patient_name: str,
        chronological_age: int,
        archetype_id: str = "dehydrated_erythema",
        uv_index: float = 6.5,
        ambient_humidity_pct: float = 35.0,
        pollution_aqi: int = 85
    ) -> Dict[str, Any]:
        """
        Executes end-to-end clinical dermal prescription:
        1. Biometric skin telemetry from YouCam Skin AI API.
        2. Barrier integrity and biological skin age computation.
        3. Active formulation synthesis & contraindication screening.
        4. Environmental circadian regimen generation (AM Shield vs PM Repair).
        """
        raw_telemetry = self.client.analyze_image(archetype_id=archetype_id)
        metrics = raw_telemetry["metrics"]
        zones = raw_telemetry["facial_zones"]

        # Step 2: Compute Barrier Health & Biological Age
        barrier_integrity = self.biometric_engine.calculate_barrier_integrity(metrics)
        skin_age, age_delta, age_status = self.biometric_engine.estimate_biological_skin_age(
            chronological_age, metrics
        )
        zone_priorities = self.biometric_engine.evaluate_zone_priorities(zones)

        # Step 3: Active Formulation Synthesis
        formulation = self.formulation_engine.synthesize_actives(barrier_integrity, metrics)

        # Step 4: Environmental Modifiers
        env_shield = []
        if uv_index >= 6.0:
            env_shield.append(f"High Solar Irradiance (UV {uv_index}): Mineral Zinc Oxide SPF 50+ PA++++ Broad-Spectrum")
        else:
            env_shield.append(f"Moderate UV ({uv_index}): Lightweight Fluid SPF 30+ PA+++")

        if ambient_humidity_pct < 40.0:
            env_shield.append(f"Arid Climate ({ambient_humidity_pct}% Humidity): 100% Plant-Derived Squalane Occlusive Lock")

        if pollution_aqi > 100:
            env_shield.append(f"Urban Particle Smog (AQI {pollution_aqi}): 2% Ectoin Anti-Adhesion Radical Scavenger")

        # Step 5: AM / PM Circadian Steps
        am_steps = [
            {"phase": "Step 1: Gentle Prep", "product": "Non-Foaming Amino Acid Hydro-Cleanser (pH 5.5)"},
            {"phase": "Step 2: Hydration & Soothing", "product": "Centella Asiatica + Multi-Molecular Hyaluronic Acid Essence"},
            {"phase": "Step 3: Active Fortification", "product": "4% Niacinamide + Zinc PCA Sebum/Barrier Serum"},
            {"phase": "Step 4: Environmental Shield", "product": env_shield[0]}
        ]

        pm_steps = [
            {"phase": "Step 1: Lipophilic Cleanse", "product": "Sunflower & Jojoba Micro-Emulsion Cleansing Balm"},
            {"phase": "Step 2: Secondary Cleanse", "product": "Gentle Ceramide Hydrating Cleanser"},
            {"phase": "Step 3: Target Active Matrix", "product": (
                "10% Micronized Azelaic Acid Suspension" if metrics.get("redness", 0) > 50
                else "Liposomal Retinaldehyde 0.05% + Copper Peptides" if barrier_integrity >= 55.0
                else "Centella + Ectoin Intensive Recovery Ampoule"
            )},
            {"phase": "Step 4: Lamellar Lipid Repair", "product": "Bio-Identical Ceramide EOP/NP/AP 3:1:1:1 Barrier Cream"}
        ]

        return {
            "protocol_id": f"DERMA-{patient_name.upper().replace(' ', '_')}-2026",
            "patient_name": patient_name,
            "chronological_age": chronological_age,
            "biological_skin_age": skin_age,
            "age_delta": age_delta,
            "age_status": age_status,
            "dermal_barrier_integrity_score": barrier_integrity,
            "primary_diagnosis": raw_telemetry["diagnosis_label"],
            "biometric_telemetry": metrics,
            "zone_priorities": zone_priorities,
            "formulation_synthesis": formulation,
            "environmental_conditions": {
                "uv_index": uv_index,
                "ambient_humidity_pct": ambient_humidity_pct,
                "pollution_aqi": pollution_aqi,
                "active_environmental_modifiers": env_shield
            },
            "circadian_regimen": {
                "morning_photoprotective_shield": am_steps,
                "evening_cellular_lipid_repair": pm_steps
            },
            "clinical_summary": (
                f"Biometric analysis for {patient_name} (Age {chronological_age}) indicates a Dermal Barrier Integrity of {barrier_integrity}/100 "
                f"with biological skin age estimated at {skin_age} ({age_status}). "
                f"{len(formulation['selected_actives'])} active complexes prescribed with {len(formulation['contraindicated_actives'])} contraindication safety gates."
            )
        }
