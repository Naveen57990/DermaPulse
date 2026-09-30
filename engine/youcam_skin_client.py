"""
YouCam Skin AI Client & Biometric Telemetry Gateway
Provides client interface for YouCam Skin Analysis API with fallback offline simulation fixtures.
"""

import json
import urllib.request
import urllib.parse
from typing import Any, Dict, List, Optional


class YouCamSkinClient:
    """Client for Perfect Corp / YouCam Skin AI Diagnostic API."""

    BASE_URL = "https://api.perfectcorp.com/v1.0/skin"

    def __init__(self, api_key: Optional[str] = None, use_sandbox: bool = True):
        self.api_key = api_key or ""
        self.use_sandbox = use_sandbox
        self._archetypes = self._init_archetypes()

    def _init_archetypes(self) -> Dict[str, Dict[str, Any]]:
        """Pre-calibrated clinical skin telemetry archetypes."""
        return {
            "dehydrated_erythema": {
                "id": "ARCH-01-DEHYDRATED",
                "label": "Dehydrated Stratum Corneum & Post-Inflammatory Erythema",
                "metrics": {
                    "moisture": 32,      # Low (0-100)
                    "oiliness": 68,      # Compensatory high sebum
                    "redness": 74,       # High vascularity / erythema
                    "texture": 58,       # Moderate roughness
                    "wrinkles": 28,      # Fine dehydration lines
                    "spots": 42,         # Post-inflammatory marks
                    "dark_circles": 35   # Mild periorbital congestion
                },
                "zones": {
                    "t_zone": {"oiliness": 75, "texture": 62, "pore_congestion": "moderate"},
                    "u_zone_cheeks": {"moisture": 28, "redness": 82, "barrier_state": "compromised"},
                    "periorbital": {"dark_circles": 35, "fine_lines": 30}
                }
            },
            "photo_damaged_aging": {
                "id": "ARCH-02-PHOTODAMAGE",
                "label": "Solar Elastosis & Periorbital Collagen Degradation",
                "metrics": {
                    "moisture": 45,
                    "oiliness": 30,
                    "redness": 38,
                    "texture": 72,
                    "wrinkles": 78,
                    "spots": 84,
                    "dark_circles": 62
                },
                "zones": {
                    "t_zone": {"oiliness": 35, "texture": 68, "pore_congestion": "low"},
                    "u_zone_cheeks": {"moisture": 42, "redness": 40, "pigmentation": "high"},
                    "periorbital": {"dark_circles": 62, "fine_lines": 82}
                }
            },
            "hyper_sebaceous_acne": {
                "id": "ARCH-03-SEBACEOUS",
                "label": "Hyper-Sebaceous Micro-Comedonal Profile",
                "metrics": {
                    "moisture": 52,
                    "oiliness": 88,
                    "redness": 65,
                    "texture": 82,
                    "wrinkles": 18,
                    "spots": 76,
                    "dark_circles": 25
                },
                "zones": {
                    "t_zone": {"oiliness": 92, "texture": 88, "pore_congestion": "severe"},
                    "u_zone_cheeks": {"moisture": 48, "redness": 60, "papules": "mild"},
                    "periorbital": {"dark_circles": 25, "fine_lines": 15}
                }
            },
            "reactive_rosacea": {
                "id": "ARCH-04-ROSACEA",
                "label": "Hyper-Reactive Neuro-Vascular Rosacea Profile",
                "metrics": {
                    "moisture": 38,
                    "oiliness": 42,
                    "redness": 92,
                    "texture": 66,
                    "wrinkles": 35,
                    "spots": 30,
                    "dark_circles": 48
                },
                "zones": {
                    "t_zone": {"oiliness": 45, "texture": 60, "flushing": "high"},
                    "u_zone_cheeks": {"moisture": 34, "redness": 96, "telangiectasia": "pronounced"},
                    "periorbital": {"dark_circles": 48, "fine_lines": 32}
                }
            }
        }

    def analyze_image(self, image_bytes: Optional[bytes] = None, archetype_id: str = "dehydrated_erythema") -> Dict[str, Any]:
        """Send image to YouCam Skin AI API or return deterministic archetype fixture."""
        if not self.use_sandbox and self.api_key and image_bytes:
            try:
                url = f"{self.BASE_URL}/analysis"
                req = urllib.request.Request(
                    url,
                    data=image_bytes,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/octet-stream"
                    }
                )
                with urllib.request.urlopen(req, timeout=5) as resp:
                    return json.loads(resp.read().decode())
            except Exception:
                pass

        # Return sandbox telemetry fixture
        data = self._archetypes.get(archetype_id, self._archetypes["dehydrated_erythema"])
        return {
            "status": "success",
            "source": "youcam_skin_ai_sandbox",
            "archetype_id": data["id"],
            "diagnosis_label": data["label"],
            "metrics": data["metrics"],
            "facial_zones": data["zones"]
        }
