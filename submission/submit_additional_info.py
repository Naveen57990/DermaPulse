import base64
import subprocess
import time

f4_text = """DermaPulse AI is a clinical-grade dermal intelligence platform engineered for the YouCam API Skin AI & eCommerce VTO Hackathon 2026. It pairs Perfect Corp's YouCam Skin AI multi-vector diagnostic telemetry with an evidence-based formulation synthesizer.

Key Features & Functionality:
1. Real-time extraction of 7 biometric dermal vectors: Stratum Corneum Hydration, Sebaceous Sebum, Vascular Erythema, Surface Texture/Roughness, Periorbital Fine Lines, Solar Lentigines, and Periorbital Congestion.
2. Dermal Barrier Integrity Index (0-100) scoring and Biological Skin Age estimation with longevity deltas.
3. Active formulation synthesizer with strict contraindication safety gates (preventing retinoid/AHA-induced barrier damage).
4. Circadian AM/PM skincare regimen generator scaled against real-time Solar UV Index, ambient humidity %, and Air Quality Index (AQI).
5. Interactive Web Application featuring an HTML5 Canvas biometric facial wireframe scanner with dynamic zone heatmaps and one-click JSON protocol export.

Consumer & Retail Value:
Replaces subjective consumer skincare guesswork with quantitative biometric telemetry. In eCommerce and retail environments, DermaPulse AI increases consumer conversion and repeat purchase confidence by preventing irritant product returns and delivering personalized, biologically grounded regimens."""

f6_text = """The spatial granularity of the YouCam Skin AI API was remarkably precise. In particular, the ability to isolate erythema and sebum density across distinct anatomical zones (T-Zone vs U-Zone Cheeks vs Periorbital) allowed us to implement clinical-grade differential barrier scoring and prevent conflicting active ingredient prescriptions (e.g. prescribing azelaic acid for cheek erythema while applying zinc PCA to forehead seborrhea)."""

f7_text = """1. Clinical Dermatology & Post-Operative Barrier Recovery: Monitoring trans-epidermal barrier re-epithelialization following chemical peels, laser resurfacing, or microneedling.
2. Occupational Health & Environmental Bio-Monitoring: Tracking long-term skin barrier degradation for outdoor workers, athletes, and individuals in highly polluted urban environments.
3. Personalized Compounding Pharmacies: Generating real-time bespoke active ingredient concentration ratios for on-demand skincare compounding dispensers."""

f8_text = """We encountered a challenge when handling contradictory telemetry—specifically patients presenting with concurrent surface dehydration (low moisture) and compensatory hyper-seborrhea (elevated sebum). Standard recommendation algorithms often misclassify this as oily skin and prescribe drying exfoliants, exacerbating barrier destruction. We solved this by engineering a dual-vector balancing algorithm in DermalBiometricEngine that penalizes trans-epidermal moisture loss independently of sebum output and enforces barrier repair prioritizations."""

b64_f4 = base64.b64encode(f4_text.encode("utf-8")).decode("utf-8")
b64_f6 = base64.b64encode(f6_text.encode("utf-8")).decode("utf-8")
b64_f7 = base64.b64encode(f7_text.encode("utf-8")).decode("utf-8")
b64_f8 = base64.b64encode(f8_text.encode("utf-8")).decode("utf-8")

repo_url = "https://github.com/Naveen57990/DermaPulse"
social_url = "https://dermapulse.vercel.app"

js_code = f"""
(() => {{
  // Field 0: Submitter type
  const s0 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_0_value");
  if (s0) {{
    s0.value = "Individual";
    s0.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }}

  // Field 1: Country
  const s1 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_1_value");
  if (s1) {{
    s1.value = "India";
    s1.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }}

  // Field 2: App Status
  const s2 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_2_value");
  if (s2) {{
    s2.value = "New";
    s2.dispatchEvent(new Event("change", {{ bubbles: true }}));
  }}

  // Field 3: If existing
  const s3 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_3_value");
  if (s3) {{
    s3.value = "N/A - Built completely new from scratch during the hackathon.";
    s3.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}

  // Field 4: Description
  const s4 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_4_value");
  if (s4) {{
    s4.value = decodeURIComponent(escape(atob("{b64_f4}")));
    s4.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}

  // Field 5: Repo URL
  const s5 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_5_value");
  if (s5) {{
    s5.value = "{repo_url}";
    s5.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}

  // Field 6: Surprised API moment
  const s6 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_6_value");
  if (s6) {{
    s6.value = decodeURIComponent(escape(atob("{b64_f6}")));
    s6.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}

  // Field 7: Untapped industries
  const s7 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_7_value");
  if (s7) {{
    s7.value = decodeURIComponent(escape(atob("{b64_f7}")));
    s7.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}

  // Field 8: Wall technically
  const s8 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_8_value");
  if (s8) {{
    s8.value = decodeURIComponent(escape(atob("{b64_f8}")));
    s8.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}

  // Field 9: Social URL
  const s9 = document.getElementById("participants_submission_requirements_submission_field_values_attributes_9_value");
  if (s9) {{
    s9.value = "{social_url}";
    s9.dispatchEvent(new Event("input", {{ bubbles: true }}));
  }}

  // Save & Continue
  const btns = Array.from(document.querySelectorAll("button, input[type=submit]"));
  const btn = btns.find(b => (b.innerText || b.value || "").toLowerCase().includes("save & continue") || (b.innerText || b.value || "").toLowerCase().includes("save and continue"));
  if (btn) {{
    btn.click();
    return "CLICKED_SAVE_AND_CONTINUE";
  }}
  return "NO_BUTTON";
}})()
"""

with open("/tmp/dermapulse_additional.js", "w") as f:
    f.write(js_code)

applescript = 'tell application "Google Chrome" to execute active tab of front window javascript (read POSIX file "/tmp/dermapulse_additional.js" as «class utf8»)'
res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
print("Result:", res.stdout.strip() or res.stderr.strip())
