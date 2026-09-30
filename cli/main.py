#!/usr/bin/env python3
"""
DermaPulse AI - Precision Skincare & Dermal Biometrics Tactical CLI
Integrates YouCam Skin AI Telemetry, Barrier Integrity Analysis, and Circadian Regimens.
"""

import sys
import os
import argparse
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from dermapulse.engine.youcam_skin_client import YouCamSkinClient
from dermapulse.engine.dermal_biometric_engine import DermalBiometricEngine
from dermapulse.engine.formulation_synthesizer import FormulationSynthesizer
from dermapulse.engine.circadian_regimen_planner import CircadianRegimenPlanner


def print_banner():
    print("=" * 72)
    print("  🔬 DERMAPULSE AI - Clinical Dermal Biometrics & Circadian Engine")
    print("  Powered by YouCam Skin AI Diagnostic Telemetry & Formulation Synthesizer")
    print("=" * 72)


def handle_analyze(args):
    print_banner()
    client = YouCamSkinClient(api_key=args.api_key, use_sandbox=True)
    biometric_engine = DermalBiometricEngine()

    print(f"\n[+] Fetching YouCam Skin AI Biometrics for archetype: '{args.archetype}'...")
    raw = client.analyze_image(archetype_id=args.archetype)
    metrics = raw["metrics"]
    barrier_score = biometric_engine.calculate_barrier_integrity(metrics)
    skin_age, delta, status = biometric_engine.estimate_biological_skin_age(args.age, metrics)
    zones = biometric_engine.evaluate_zone_priorities(raw["facial_zones"])

    if args.json:
        result = {
            "archetype": args.archetype,
            "diagnosis": raw["diagnosis_label"],
            "barrier_integrity_score": barrier_score,
            "chronological_age": args.age,
            "biological_skin_age": skin_age,
            "skin_age_status": status,
            "metrics": metrics,
            "zone_priorities": zones
        }
        print(json.dumps(result, indent=2))
        return

    print(f"\n📊 PRIMARY DIAGNOSIS: {raw['diagnosis_label']}")
    print(f"🛡️  BARRIER INTEGRITY INDEX : {barrier_score:.1f}/100")
    print(f"⏳ BIOLOGICAL SKIN AGE     : {skin_age} yrs ({status}, Δ: {delta:+d} yrs)")
    print("\n--- Biometric Metric Vectors ---")
    for k, v in metrics.items():
        bar = "█" * int(v / 5) + "░" * (20 - int(v / 5))
        print(f"  • {k.replace('_', ' ').capitalize():<18}: {v:>3}/100 [{bar}]")

    print("\n--- Facial Zone Priority Assessment ---")
    for z in zones:
        print(f"  • Zone: {z['zone'].upper()} | Critical Issue: {z['issue'].upper()} | Severity: {z['severity']}")


def handle_formulate(args):
    print_banner()
    client = YouCamSkinClient(api_key=args.api_key, use_sandbox=True)
    biometric_engine = DermalBiometricEngine()
    formulation_engine = FormulationSynthesizer()

    raw = client.analyze_image(archetype_id=args.archetype)
    metrics = raw["metrics"]
    barrier_score = biometric_engine.calculate_barrier_integrity(metrics)
    formulation = formulation_engine.synthesize_actives(barrier_score, metrics)

    if args.json:
        print(json.dumps(formulation, indent=2))
        return

    print(f"\n🧬 FORMULATION SYNTHESIS FOR: {raw['diagnosis_label']}")
    print(f"🛡️  Barrier Integrity Score: {barrier_score:.1f}/100 (Repair Priority: {formulation['barrier_repair_priority']})")
    print(f"\n✅ PRESCRIBED ACTIVE INGREDIENTS ({len(formulation['selected_actives'])}):")
    for act in formulation["selected_actives"]:
        print(f"  • [{act['mechanism'].upper()}] {act['name']} ({act['concentration']})")
        print(f"    RATIONALE: {act['rationale']}")

    if formulation["contraindicated_actives"]:
        print(f"\n🚫 CONTRAINDICATED INGREDIENTS ({len(formulation['contraindicated_actives'])}):")
        for c in formulation["contraindicated_actives"]:
            print(f"  • {c['name']} - REASON: {c['reason']}")


def handle_regimen(args):
    print_banner()
    planner = CircadianRegimenPlanner(youcam_api_key=args.api_key, use_sandbox=True)
    protocol = planner.generate_full_protocol(
        patient_name=args.patient,
        chronological_age=args.age,
        archetype_id=args.archetype,
        uv_index=args.uv,
        ambient_humidity_pct=args.humidity,
        pollution_aqi=args.aqi
    )

    if args.json:
        print(json.dumps(protocol, indent=2))
        return

    print(f"\n📋 PROTOCOL ID: {protocol['protocol_id']}")
    print(f"👤 Patient: {protocol['patient_name']} (Age: {protocol['chronological_age']} | Bio Skin Age: {protocol['biological_skin_age']} | Status: {protocol['age_status']})")
    print(f"🛡️  Barrier Integrity: {protocol['dermal_barrier_integrity_score']:.1f}/100")
    print(f"🌡️  Environmental Scale: UV {args.uv} | Humidity {args.humidity}% | AQI {args.aqi}")

    print("\n☀️  MORNING PHOTOPROTECTIVE REGIMEN (Shield & Fortify):")
    for step in protocol["circadian_regimen"]["morning_photoprotective_shield"]:
        print(f"  [{step['phase']}] -> {step['product']}")

    print("\n🌙  EVENING CELLULAR REPAIR REGIMEN (Restore & Nourish):")
    for step in protocol["circadian_regimen"]["evening_cellular_lipid_repair"]:
        print(f"  [{step['phase']}] -> {step['product']}")

    print(f"\n📝 Clinical Summary: {protocol['clinical_summary']}")


def main():
    parser = argparse.ArgumentParser(description="DermaPulse AI - Dermal Biometric & Circadian Prescription CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommand to execute")

    # Analyze
    p_analyze = subparsers.add_parser("analyze", help="Analyze skin biometrics from archetype")
    p_analyze.add_argument("--archetype", default="dehydrated_erythema", choices=["dehydrated_erythema", "photo_damaged_aging", "hyper_sebaceous_acne", "reactive_rosacea"])
    p_analyze.add_argument("--age", type=int, default=32, help="Chronological age")
    p_analyze.add_argument("--api-key", default=None, help="YouCam API key (optional)")
    p_analyze.add_argument("--json", action="store_true", help="Output raw JSON")

    # Formulate
    p_form = subparsers.add_parser("formulate", help="Synthesize active ingredients and check contraindications")
    p_form.add_argument("--archetype", default="dehydrated_erythema", choices=["dehydrated_erythema", "photo_damaged_aging", "hyper_sebaceous_acne", "reactive_rosacea"])
    p_form.add_argument("--api-key", default=None, help="YouCam API key (optional)")
    p_form.add_argument("--json", action="store_true", help="Output raw JSON")

    # Regimen
    p_reg = subparsers.add_parser("regimen", help="Generate full circadian environmental protocol")
    p_reg.add_argument("--patient", default="Elena Rostova", help="Patient name")
    p_reg.add_argument("--age", type=int, default=34, help="Patient chronological age")
    p_reg.add_argument("--archetype", default="dehydrated_erythema", choices=["dehydrated_erythema", "photo_damaged_aging", "hyper_sebaceous_acne", "reactive_rosacea"])
    p_reg.add_argument("--uv", type=float, default=7.5, help="Ambient UV index")
    p_reg.add_argument("--humidity", type=float, default=28.0, help="Ambient relative humidity percentage")
    p_reg.add_argument("--aqi", type=int, default=115, help="Air Quality Index")
    p_reg.add_argument("--api-key", default=None, help="YouCam API key (optional)")
    p_reg.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "analyze":
        handle_analyze(args)
    elif args.command == "formulate":
        handle_formulate(args)
    elif args.command == "regimen":
        handle_regimen(args)


if __name__ == "__main__":
    main()
