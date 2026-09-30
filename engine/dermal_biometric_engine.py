"""
Dermal Biometric Engine
Computes quantitative Dermal Barrier Integrity (0-100), biological skin age discrepancy,
and zone-specific physiological diagnostics.
"""

from typing import Any, Dict, List, Tuple


class DermalBiometricEngine:
    """Quantitative analyzer for biometric skin health telemetry."""

    @staticmethod
    def calculate_barrier_integrity(metrics: Dict[str, float]) -> float:
        """
        Calculate Dermal Barrier Integrity Index (0.0 to 100.0).
        High moisture + low erythema/redness + smooth texture + balanced sebum = high barrier health.
        """
        moisture = metrics.get("moisture", 50.0)
        redness = metrics.get("redness", 30.0)
        texture = metrics.get("texture", 30.0)
        oiliness = metrics.get("oiliness", 50.0)

        # Sebum balance factor (penalty for severe deviation from optimal 50)
        sebum_balance = max(0.0, 100.0 - abs(oiliness - 50.0) * 1.5)

        barrier_score = (
            (moisture * 0.35) +
            ((100.0 - redness) * 0.30) +
            ((100.0 - texture) * 0.20) +
            (sebum_balance * 0.15)
        )
        return round(max(0.0, min(100.0, barrier_score)), 1)

    @staticmethod
    def estimate_biological_skin_age(
        chronological_age: int, metrics: Dict[str, float]
    ) -> Tuple[int, int, str]:
        """
        Estimate biological skin age based on photo-aging metrics (wrinkles, spots, elasticity/texture).
        Returns: (estimated_skin_age, age_delta, status_label)
        """
        wrinkles = metrics.get("wrinkles", 30.0)
        spots = metrics.get("spots", 30.0)
        texture = metrics.get("texture", 30.0)

        photo_aging_index = (wrinkles * 0.45) + (spots * 0.35) + (texture * 0.20)

        # Baseline expected photo-aging for chronological age
        expected_index = max(10.0, min(90.0, (chronological_age - 18) * 1.5 + 15.0))
        delta = int(round((photo_aging_index - expected_index) / 3.0))

        estimated_age = max(18, chronological_age + delta)

        if delta <= -3:
            status = "Preserved / Youthful Longevity"
        elif abs(delta) <= 2:
            status = "Chronologically Synchronized"
        else:
            status = "Accelerated Photo-Aging Detected"

        return estimated_age, delta, status

    def evaluate_zone_priorities(self, zones: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify critical localized dermal priorities across facial zones."""
        priorities = []
        t_zone = zones.get("t_zone", {})
        if t_zone.get("oiliness", 0) > 70:
            priorities.append({
                "zone": "T-Zone (Forehead & Nasal Bridge)",
                "issue": "Sebaceous Hyper-Activity",
                "severity": "HIGH",
                "target_intervention": "Lipophilic BHA / Zinc PCA Sebum Regulation"
            })

        u_zone = zones.get("u_zone_cheeks", {})
        if u_zone.get("redness", 0) > 70 or u_zone.get("barrier_state") == "compromised":
            priorities.append({
                "zone": "U-Zone (Cheeks & Jawline)",
                "issue": "Vascular Erythema & Trans-Epidermal Water Loss",
                "severity": "CRITICAL",
                "target_intervention": "Bio-Identical Ceramide Complex & Centella Asiatica"
            })

        periorbital = zones.get("periorbital", {})
        if periorbital.get("dark_circles", 0) > 50 or periorbital.get("fine_lines", 0) > 50:
            priorities.append({
                "zone": "Periorbital Contour",
                "issue": "Micro-Vascular Congestion & Dynamic Fine Lines",
                "severity": "MODERATE",
                "target_intervention": "Caffeine Peptide Matrix & Multi-Weight Hyaluronate"
            })

        return priorities
