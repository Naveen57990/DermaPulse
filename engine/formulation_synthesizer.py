"""
Formulation Synthesizer
Active ingredient synergy and chemical contraindication matrix.
"""

from typing import Any, Dict, List, Tuple


class FormulationSynthesizer:
    """Synthesizes compatible active ingredient formulations based on biometric dermal telemetry."""

    ACTIVE_INGREDIENT_DATABASE: Dict[str, Dict[str, Any]] = {
        "Ceramide_NP_Complex": {
            "name": "Bio-Identical Ceramide NP/AP/EOP (3:1:1:1 Ratio)",
            "primary_function": "Lipid Lamellar Barrier Repair & TEWL Reduction",
            "safe_for_compromised_barrier": True,
            "ph_range": (5.0, 6.5),
            "synergies": ["Hyaluronic_Acid", "Centella_Asiatica", "Niacinamide", "Ectoin"],
            "contraindications": []
        },
        "Centella_Asiatica_Madecassoside": {
            "name": "Centella Asiatica (95% Pure Madecassoside & Asiaticoside)",
            "primary_function": "Neuro-Vascular Anti-Inflammatory & Erythema Quenching",
            "safe_for_compromised_barrier": True,
            "ph_range": (4.5, 7.0),
            "synergies": ["Ceramide_NP_Complex", "Azelaic_Acid_Micronized", "Niacinamide"],
            "contraindications": []
        },
        "Niacinamide_Vitamin_B3": {
            "name": "Niacinamide (4% Optimized Concentration)",
            "primary_function": "Ceramide Synthesis Stimulation & Melanosome Transfer Inhibition",
            "safe_for_compromised_barrier": True,
            "ph_range": (5.5, 6.5),
            "synergies": ["Ceramide_NP_Complex", "Zinc_PCA", "Centella_Asiatica"],
            "contraindications": []
        },
        "Azelaic_Acid_Micronized": {
            "name": "Micronized Azelaic Acid (10% Suspension)",
            "primary_function": "Anti-Microbial & Post-Inflammatory Erythema Resolution",
            "safe_for_compromised_barrier": True,
            "ph_range": (4.0, 5.0),
            "synergies": ["Niacinamide_Vitamin_B3", "Centella_Asiatica_Madecassoside"],
            "contraindications": ["High_Potency_Glycolic_Acid"]
        },
        "Zinc_PCA": {
            "name": "Zinc Pyrrolidone Carboxylic Acid (1% Zinc PCA)",
            "primary_function": "5-Alpha Reductase Sebum Inhibition & P. acnes Control",
            "safe_for_compromised_barrier": True,
            "ph_range": (4.5, 6.0),
            "synergies": ["Niacinamide_Vitamin_B3", "Salicylic_Acid_Encapsulated"],
            "contraindications": []
        },
        "Encapsulated_Retinaldehyde": {
            "name": "Liposomal Encapsulated Retinaldehyde (0.05%)",
            "primary_function": "Collagen Synthesis Stimulation & Cellular Turnover Acceleration",
            "safe_for_compromised_barrier": False,
            "ph_range": (6.0, 6.8),
            "synergies": ["Ceramide_NP_Complex", "Copper_Tripeptide_1"],
            "contraindications": ["L_Ascorbic_Acid_Raw", "High_Potency_Glycolic_Acid"]
        },
        "L_Ascorbic_Acid_Raw": {
            "name": "L-Ascorbic Acid (15% Pure Vitamin C + Ferulic Acid)",
            "primary_function": "Free Radical Neutralization & Photoprotection Boost",
            "safe_for_compromised_barrier": False,
            "ph_range": (2.8, 3.2),
            "synergies": ["Vitamin_E_Tocopherol", "Ferulic_Acid"],
            "contraindications": ["Encapsulated_Retinaldehyde", "Compromised_Barrier_State"]
        }
    }

    def synthesize_actives(
        self, barrier_integrity: float, metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Select optimal active ingredients based on barrier health and specific clinical priorities.
        """
        selected_actives: List[Dict[str, Any]] = []
        contraindicated_actives: List[Dict[str, str]] = []

        # Rule 1: Compromised barrier priority (< 55.0)
        if barrier_integrity < 55.0:
            selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Ceramide_NP_Complex"])
            selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Centella_Asiatica_Madecassoside"])
            contraindicated_actives.append({
                "active": "Raw L-Ascorbic Acid & High % AHAs",
                "reason": f"Dermal Barrier Integrity ({barrier_integrity}/100) is compromised. Low pH acids risk acute chemical dermatitis."
            })
            contraindicated_actives.append({
                "active": "Direct Retinol > 0.3%",
                "reason": "Retinoids are temporarily contraindicated until stratum corneum lipid matrix is restored."
            })
        else:
            # Healthy barrier can tolerate collagen stimulators
            if metrics.get("wrinkles", 0) > 50 or metrics.get("spots", 0) > 50:
                selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Encapsulated_Retinaldehyde"])
                selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["L_Ascorbic_Acid_Raw"])

        # Rule 2: High Redness / Vascularity
        if metrics.get("redness", 0) > 50:
            if self.ACTIVE_INGREDIENT_DATABASE["Centella_Asiatica_Madecassoside"] not in selected_actives:
                selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Centella_Asiatica_Madecassoside"])
            selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Azelaic_Acid_Micronized"])

        # Rule 3: High Sebum / Texture
        if metrics.get("oiliness", 0) > 65:
            selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Niacinamide_Vitamin_B3"])
            selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Zinc_PCA"])

        # Ensure Niacinamide is included if empty
        if not selected_actives:
            selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Ceramide_NP_Complex"])
            selected_actives.append(self.ACTIVE_INGREDIENT_DATABASE["Niacinamide_Vitamin_B3"])

        return {
            "selected_actives": selected_actives,
            "contraindicated_actives": contraindicated_actives,
            "barrier_safety_status": "LIPID_REPAIR_MANDATORY" if barrier_integrity < 55.0 else "OPTIMAL_ACTIVE_TOLERANCE"
        }
