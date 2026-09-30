/**
 * DermaPulse AI - Frontend Biometric Engine & Dermal Scanner
 */

const ARCHETYPES = {
  dehydrated_erythema: {
    id: "ARCH-01-DEHYDRATED",
    label: "Dehydrated Stratum Corneum & Erythema",
    metrics: { moisture: 32, oiliness: 68, redness: 74, texture: 58, wrinkles: 28, spots: 42, dark_circles: 35 },
    zones: {
      t_zone: { oiliness: 75, label: "T-ZONE: SEBUM 75" },
      cheeks: { redness: 82, label: "U-ZONE: ERYTHEMA 82" },
      eyes: { dark_circles: 35, label: "PERIORBITAL: CONGESTION 35" }
    }
  },
  photo_damaged_aging: {
    id: "ARCH-02-PHOTODAMAGE",
    label: "Solar Elastosis & Collagen Depletion",
    metrics: { moisture: 45, oiliness: 30, redness: 38, texture: 72, wrinkles: 78, spots: 84, dark_circles: 62 },
    zones: {
      t_zone: { oiliness: 35, label: "T-ZONE: TEXTURE 68" },
      cheeks: { redness: 40, label: "CHEEKS: HYPERPIGMENT 84" },
      eyes: { dark_circles: 62, label: "PERIORBITAL: ELASTOSIS 82" }
    }
  },
  hyper_sebaceous_acne: {
    id: "ARCH-03-SEBACEOUS",
    label: "Hyper-Sebaceous Micro-Comedonal Profile",
    metrics: { moisture: 52, oiliness: 88, redness: 65, texture: 82, wrinkles: 18, spots: 76, dark_circles: 25 },
    zones: {
      t_zone: { oiliness: 92, label: "T-ZONE: SEBUM 92 (SEVERE)" },
      cheeks: { redness: 60, label: "CHEEKS: PAPULES 60" },
      eyes: { dark_circles: 25, label: "PERIORBITAL: NORMAL 25" }
    }
  },
  reactive_rosacea: {
    id: "ARCH-04-ROSACEA",
    label: "Hyper-Reactive Neuro-Vascular Rosacea",
    metrics: { moisture: 38, oiliness: 42, redness: 92, texture: 66, wrinkles: 35, spots: 30, dark_circles: 48 },
    zones: {
      t_zone: { oiliness: 45, label: "T-ZONE: FLUSHING 45" },
      cheeks: { redness: 96, label: "U-ZONE: TELANGIECTASIA 96" },
      eyes: { dark_circles: 48, label: "PERIORBITAL: REACTIVE 48" }
    }
  }
};

let currentArch = "dehydrated_erythema";

// DOM Elements
const patientNameInput = document.getElementById("patientName");
const patientAgeInput = document.getElementById("patientAge");
const ageVal = document.getElementById("ageVal");
const uvSlider = document.getElementById("uvSlider");
const uvVal = document.getElementById("uvVal");
const humiditySlider = document.getElementById("humiditySlider");
const humidityVal = document.getElementById("humidityVal");
const aqiSlider = document.getElementById("aqiSlider");
const aqiVal = document.getElementById("aqiVal");
const envSummaryBox = document.getElementById("envSummaryBox");

const barrierScoreEl = document.getElementById("barrierScore");
const barrierStatusEl = document.getElementById("barrierStatus");
const skinAgeDisplayEl = document.getElementById("skinAgeDisplay");
const skinAgeStatusEl = document.getElementById("skinAgeStatus");
const metricsGridEl = document.getElementById("metricsGrid");
const activesListEl = document.getElementById("activesList");
const contraListEl = document.getElementById("contraList");
const activeCountEl = document.getElementById("activeCount");
const contraCountEl = document.getElementById("contraCount");
const amStepsEl = document.getElementById("amSteps");
const pmStepsEl = document.getElementById("pmSteps");

const tagTZone = document.getElementById("tagTZone");
const tagCheeks = document.getElementById("tagCheeks");
const tagEyes = document.getElementById("tagEyes");

const canvas = document.getElementById("faceCanvas");
const ctx = canvas.getContext("2d");

// Calculation Engines
function calculateBarrierIntegrity(m) {
  const moisture = m.moisture || 50;
  const redness = m.redness || 50;
  const texture = m.texture || 50;
  const oiliness = m.oiliness || 50;

  const penalty = (redness * 0.40) + (texture * 0.25) + (Math.abs(oiliness - 50) * 0.35);
  const rawScore = (moisture * 0.70) + (100 - penalty) * 0.30;
  return Math.max(0.0, Math.min(100.0, Number(rawScore.toFixed(1))));
}

function estimateBiologicalAge(chronoAge, m) {
  let penalty = 0;
  if (m.wrinkles > 50) penalty += (m.wrinkles - 50) * 0.15;
  if (m.spots > 50) penalty += (m.spots - 50) * 0.10;
  if (m.texture > 60) penalty += (m.texture - 60) * 0.08;
  if (m.moisture < 40) penalty += (40 - m.moisture) * 0.10;
  if (m.moisture > 65) penalty -= (m.moisture - 65) * 0.08;

  const ageDelta = Math.round(penalty);
  const bioAge = Math.max(18, chronoAge + ageDelta);
  let status = "Chronologically Synchronized";
  if (ageDelta >= 3) status = "Accelerated Photo-Aging";
  else if (ageDelta <= -3) status = "Preserved / Youthful Longevity";

  return { bioAge, ageDelta, status };
}

function synthesizeFormulation(barrierScore, m) {
  const actives = [];
  const contra = [];
  const isCompromised = barrierScore < 55.0;

  if (isCompromised) {
    actives.push({
      name: "Bio-Identical Ceramide Complex (NP/AP/EOP 3:1:1:1)",
      mechanism: "Lamellar Lipid Bilayer Restoration",
      concentration: "2.5%",
      rationale: "Accelerates TEWL reduction and replenishes depleted stratum corneum intercellular lipids."
    });
    actives.push({
      name: "Centella Asiatica (Madecassoside 95% Pure)",
      mechanism: "Fibroblast Stimulation & Anti-Erythema",
      concentration: "1.0%",
      rationale: "Down-regulates NF-kB inflammatory cascade and soothes micro-vascular dilation."
    });
    actives.push({
      name: "Ectoin Extremolyte Multi-Protective Shield",
      mechanism: "Cell Membrane & Protein Stabilization",
      concentration: "2.0%",
      rationale: "Protects cellular membrane fluidity under osmotic and environmental stress."
    });

    contra.push({
      name: "Retinoids / Tretinoin / Retinaldehyde",
      reason: "High irritation risk; disrupts desmosome cohesion during active epidermal barrier breakdown."
    });
    contra.push({
      name: "Alpha Hydroxy Acids (Glycolic / Lactic Acid > 5%)",
      reason: "Low pH triggers severe stinging, stratum corneum thinning, and micro-fissuring."
    });
  } else {
    if (m.wrinkles >= 40 || m.spots >= 40) {
      actives.push({
        name: "Liposomal Retinaldehyde + Copper Tripeptide-1",
        mechanism: "Pro-Collagen I/III Synthesis & Cellular Turnover",
        concentration: "0.05% Retinal + 100ppm GHK-Cu",
        rationale: "Maximizes gene transcription of procollagen without typical retinoic acid dermatitis."
      });
      actives.push({
        name: "Ascorbyl Tetraisopalmitate (Lipid-Soluble Vitamin C)",
        mechanism: "Melanogenesis Inhibition & Tyrosinase Suppression",
        concentration: "5.0%",
        rationale: "Deep dermal penetration to clear solar lentigines and scavenge singlet oxygen."
      });
    }

    if (m.oiliness >= 65 || m.texture >= 60) {
      actives.push({
        name: "Niacinamide (Vitamin B3) + Zinc PCA",
        mechanism: "Sebaceous Lipogenesis Regulation & Pore Refinement",
        concentration: "4.0% Niacinamide + 1.0% Zinc PCA",
        rationale: "Suppresses sebum excretion rate and strengthens cornified envelope."
      });
    }

    if (m.redness >= 50) {
      actives.push({
        name: "Micronized Azelaic Acid Suspension",
        mechanism: "Kallikrein-5 & LL-37 Cathelicidin Inhibition",
        concentration: "10.0%",
        rationale: "Suppresses telangiectatic flare-ups and antimicrobial hyper-reactivity."
      });
    }
  }

  return { actives, contra, barrierPriority: isCompromised ? "CRITICAL (Phase 1 Repair)" : "STANDARD (Fortification & Longevity)" };
}

// Render UI
function updateUI() {
  const data = ARCHETYPES[currentArch];
  const m = data.metrics;
  const chronoAge = parseInt(patientAgeInput.value, 10);
  const uv = parseFloat(uvSlider.value);
  const humidity = parseFloat(humiditySlider.value);
  const aqi = parseInt(aqiSlider.value, 10);

  // Update Labels
  ageVal.textContent = `${chronoAge} yrs`;
  uvVal.textContent = `UV ${uv} (${uv >= 6 ? 'High' : uv >= 3 ? 'Moderate' : 'Low'})`;
  humidityVal.textContent = `${humidity}% (${humidity < 40 ? 'Arid' : humidity > 70 ? 'Humid' : 'Optimal'})`;
  aqiVal.textContent = `AQI ${aqi} (${aqi > 100 ? 'Unhealthy' : 'Moderate / Good'})`;

  // Environmental summary
  let envText = "";
  if (uv >= 6) envText += `☀️ High Solar Irradiance (UV ${uv}) triggers Mineral ZnO SPF 50+ broad-spectrum photo-shield. `;
  else envText += `🌤️ Moderate UV (${uv}) requires Lightweight Fluid SPF 30+. `;

  if (humidity < 40) envText += `💧 Arid environment (${humidity}%) engages Squalane lipid lock. `;
  if (aqi > 100) envText += `🏭 Elevated Urban Smog (AQI ${aqi}) triggers Ectoin 2% anti-pollution barrier. `;
  envSummaryBox.textContent = envText;

  // Barrier & Skin Age
  const barrierScore = calculateBarrierIntegrity(m);
  const { bioAge, ageDelta, status: ageStatus } = estimateBiologicalAge(chronoAge, m);

  barrierScoreEl.innerHTML = `${barrierScore.toFixed(1)}<span class="score-unit">/100</span>`;
  if (barrierScore < 55) {
    barrierStatusEl.className = "score-status compromised";
    barrierStatusEl.textContent = "COMPROMISED BARRIER";
  } else {
    barrierStatusEl.className = "score-status healthy";
    barrierStatusEl.textContent = "HEALTHY CORNIFIED MATRIX";
  }

  skinAgeDisplayEl.innerHTML = `${bioAge} <span class="score-unit">yrs</span>`;
  if (ageDelta > 0) {
    skinAgeStatusEl.className = "score-status elevated";
    skinAgeStatusEl.textContent = `+${ageDelta} yrs Accelerated`;
  } else if (ageDelta < 0) {
    skinAgeStatusEl.className = "score-status healthy";
    skinAgeStatusEl.textContent = `${ageDelta} yrs Preserved`;
  } else {
    skinAgeStatusEl.className = "score-status healthy";
    skinAgeStatusEl.textContent = "Chronologically Synced";
  }

  // Zone Tags
  tagTZone.textContent = data.zones.t_zone.label;
  tagCheeks.textContent = data.zones.cheeks.label;
  tagEyes.textContent = data.zones.eyes.label;

  // 7 Biometric Bars
  metricsGridEl.innerHTML = Object.entries(m).map(([k, v]) => {
    const name = k.replace('_', ' ').toUpperCase();
    return `
      <div class="metric-card">
        <div class="metric-header">
          <span>${name}</span>
          <strong>${v}/100</strong>
        </div>
        <div class="metric-bar-bg">
          <div class="metric-bar-fill" style="width: ${v}%; background: ${v > 70 ? 'var(--accent-rose)' : v > 40 ? 'var(--accent-cyan)' : 'var(--accent-teal)'}"></div>
        </div>
      </div>
    `;
  }).join("");

  // Formulations
  const { actives, contra } = synthesizeFormulation(barrierScore, m);
  activeCountEl.textContent = `${actives.length} Actives`;
  contraCountEl.textContent = `${contra.length} Blocked`;

  activesListEl.innerHTML = actives.map(act => `
    <div class="active-card">
      <div class="active-name">
        <span>${act.name}</span>
        <span class="active-conc">${act.concentration}</span>
      </div>
      <div class="active-mech">${act.mechanism} — ${act.rationale}</div>
    </div>
  `).join("");

  contraListEl.innerHTML = contra.map(c => `
    <div class="contra-card">
      <div class="contra-name">🚫 ${c.name}</div>
      <div class="contra-reason">${c.reason}</div>
    </div>
  `).join("");

  // AM / PM Steps
  const amShield = uv >= 6.0 ? "Mineral Zinc Oxide SPF 50+ PA++++ Broad-Spectrum" : "Lightweight Fluid SPF 30+ PA+++";
  amStepsEl.innerHTML = `
    <div class="step-card">
      <div class="step-phase">Step 1: Gentle Prep</div>
      <div class="step-product">Non-Foaming Amino Acid Hydro-Cleanser (pH 5.5)</div>
    </div>
    <div class="step-card">
      <div class="step-phase">Step 2: Hydration & Soothing</div>
      <div class="step-product">Centella Asiatica + Multi-Molecular Hyaluronic Acid Essence</div>
    </div>
    <div class="step-card">
      <div class="step-phase">Step 3: Fortification Active</div>
      <div class="step-product">4% Niacinamide + Zinc PCA Sebum/Barrier Serum</div>
    </div>
    <div class="step-card">
      <div class="step-phase">Step 4: Environmental Shield</div>
      <div class="step-product">${amShield}</div>
    </div>
  `;

  const pmTarget = m.redness > 50
    ? "10% Micronized Azelaic Acid Suspension"
    : barrierScore >= 55.0
      ? "Liposomal Retinaldehyde 0.05% + Copper Peptides"
      : "Centella + Ectoin Intensive Recovery Ampoule";

  pmStepsEl.innerHTML = `
    <div class="step-card">
      <div class="step-phase">Step 1: Lipophilic Cleanse</div>
      <div class="step-product">Sunflower & Jojoba Micro-Emulsion Cleansing Balm</div>
    </div>
    <div class="step-card">
      <div class="step-phase">Step 2: Secondary Cleanse</div>
      <div class="step-product">Gentle Ceramide Hydrating Cleanser</div>
    </div>
    <div class="step-card">
      <div class="step-phase">Step 3: Target Active Matrix</div>
      <div class="step-product">${pmTarget}</div>
    </div>
    <div class="step-card">
      <div class="step-phase">Step 4: Lamellar Lipid Repair</div>
      <div class="step-product">Bio-Identical Ceramide EOP/NP/AP 3:1:1:1 Barrier Cream</div>
    </div>
  `;

  drawDermalFace(m);
}

// Draw Canvas Biometric Wireframe Face & Heatmap
let animAngle = 0;
function drawDermalFace(m) {
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  // Dark background grid
  ctx.strokeStyle = "rgba(36, 52, 77, 0.4)";
  ctx.lineWidth = 1;
  const step = 30;
  for (let x = 0; x < w; x += step) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, h);
    ctx.stroke();
  }
  for (let y = 0; y < h; y += step) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(w, y);
    ctx.stroke();
  }

  // Face Oval
  const cx = w / 2;
  const cy = h / 2 - 10;
  const rx = 140;
  const ry = 190;

  // Glowing Heatmap Blobs
  // Forehead (T-Zone Sebum)
  const gradForehead = ctx.createRadialGradient(cx, cy - 90, 10, cx, cy - 90, 70);
  const sebumAlpha = (m.oiliness / 100) * 0.5;
  gradForehead.addColorStop(0, `rgba(0, 229, 255, ${sebumAlpha})`);
  gradForehead.addColorStop(1, "rgba(0, 229, 255, 0)");
  ctx.fillStyle = gradForehead;
  ctx.beginPath();
  ctx.arc(cx, cy - 90, 70, 0, Math.PI * 2);
  ctx.fill();

  // Left & Right Cheeks (Redness / Erythema)
  const redAlpha = (m.redness / 100) * 0.6;
  // Left Cheek
  const gradLCheek = ctx.createRadialGradient(cx - 65, cy + 20, 5, cx - 65, cy + 20, 60);
  gradLCheek.addColorStop(0, `rgba(255, 71, 87, ${redAlpha})`);
  gradLCheek.addColorStop(1, "rgba(255, 71, 87, 0)");
  ctx.fillStyle = gradLCheek;
  ctx.beginPath();
  ctx.arc(cx - 65, cy + 20, 60, 0, Math.PI * 2);
  ctx.fill();

  // Right Cheek
  const gradRCheek = ctx.createRadialGradient(cx + 65, cy + 20, 5, cx + 65, cy + 20, 60);
  gradRCheek.addColorStop(0, `rgba(255, 71, 87, ${redAlpha})`);
  gradRCheek.addColorStop(1, "rgba(255, 71, 87, 0)");
  ctx.fillStyle = gradRCheek;
  ctx.beginPath();
  ctx.arc(cx + 65, cy + 20, 60, 0, Math.PI * 2);
  ctx.fill();

  // Face Contour Outline
  ctx.strokeStyle = "rgba(0, 229, 255, 0.7)";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
  ctx.stroke();

  // Facial Wireframe Latitudes & Longitudes
  ctx.strokeStyle = "rgba(0, 229, 255, 0.25)";
  ctx.lineWidth = 1;
  for (let i = -3; i <= 3; i++) {
    ctx.beginPath();
    ctx.ellipse(cx, cy + i * 40, rx * Math.cos(i * 0.3), 30, 0, 0, Math.PI * 2);
    ctx.stroke();
  }

  // Vertical Meridiens
  for (let j = -2; j <= 2; j++) {
    ctx.beginPath();
    ctx.ellipse(cx + j * 45, cy, 25, ry, 0, 0, Math.PI * 2);
    ctx.stroke();
  }

  // Eye Landmarks
  ctx.strokeStyle = "rgba(0, 230, 153, 0.8)";
  ctx.lineWidth = 2;
  // Left Eye
  ctx.beginPath();
  ctx.ellipse(cx - 50, cy - 20, 24, 12, 0, 0, Math.PI * 2);
  ctx.stroke();
  // Right Eye
  ctx.beginPath();
  ctx.ellipse(cx + 50, cy - 20, 24, 12, 0, 0, Math.PI * 2);
  ctx.stroke();

  // Nose Bridge & Base
  ctx.strokeStyle = "rgba(0, 229, 255, 0.6)";
  ctx.beginPath();
  ctx.moveTo(cx, cy - 30);
  ctx.lineTo(cx, cy + 30);
  ctx.lineTo(cx - 15, cy + 45);
  ctx.lineTo(cx + 15, cy + 45);
  ctx.closePath();
  ctx.stroke();

  // Lip Contour
  ctx.beginPath();
  ctx.ellipse(cx, cy + 90, 32, 14, 0, 0, Math.PI * 2);
  ctx.stroke();

  // Rotating Reticle
  animAngle += 0.02;
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(animAngle);
  ctx.strokeStyle = "rgba(0, 229, 255, 0.15)";
  ctx.setLineDash([6, 12]);
  ctx.beginPath();
  ctx.arc(0, 0, 170, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}

// Animation loop
function animate() {
  const data = ARCHETYPES[currentArch];
  drawDermalFace(data.metrics);
  requestAnimationFrame(animate);
}

// Event Listeners
document.querySelectorAll(".arch-card").forEach(card => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".arch-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    currentArch = card.getAttribute("data-arch");
    updateUI();
  });
});

patientAgeInput.addEventListener("input", updateUI);
uvSlider.addEventListener("input", updateUI);
humiditySlider.addEventListener("input", updateUI);
aqiSlider.addEventListener("input", updateUI);
patientNameInput.addEventListener("input", updateUI);

// Modal Controls
const apiModal = document.getElementById("apiModal");
document.getElementById("openApiBtn").addEventListener("click", () => apiModal.classList.add("show"));
document.getElementById("closeApiBtn").addEventListener("click", () => apiModal.classList.remove("show"));
document.getElementById("cancelApiBtn").addEventListener("click", () => apiModal.classList.remove("show"));
document.getElementById("saveApiBtn").addEventListener("click", () => {
  const key = document.getElementById("apiKeyInput").value.trim();
  const mode = document.querySelector('input[name="apiMode"]:checked').value;
  const statusText = document.getElementById("apiStatusText");

  if (mode === "live" && key) {
    statusText.textContent = "LIVE CLOUD CONNECTED";
    statusText.style.color = "var(--accent-teal)";
  } else {
    statusText.textContent = "SANDBOX ACTIVE";
    statusText.style.color = "var(--accent-cyan)";
  }
  apiModal.classList.remove("show");
});

// JSON Export
document.getElementById("exportJsonBtn").addEventListener("click", () => {
  const data = ARCHETYPES[currentArch];
  const m = data.metrics;
  const chronoAge = parseInt(patientAgeInput.value, 10);
  const uv = parseFloat(uvSlider.value);
  const humidity = parseFloat(humiditySlider.value);
  const aqi = parseInt(aqiSlider.value, 10);
  const barrierScore = calculateBarrierIntegrity(m);
  const { bioAge, ageDelta, status: ageStatus } = estimateBiologicalAge(chronoAge, m);
  const { actives, contra } = synthesizeFormulation(barrierScore, m);

  const protocol = {
    protocol_id: `DERMA-${patientNameInput.value.toUpperCase().replace(/[^A-Z0-9]/g, '_')}-2026`,
    patient_name: patientNameInput.value,
    chronological_age: chronoAge,
    biological_skin_age: bioAge,
    age_delta: ageDelta,
    age_status: ageStatus,
    dermal_barrier_integrity_score: barrierScore,
    primary_diagnosis: data.label,
    biometric_telemetry: m,
    environmental_conditions: { uv_index: uv, ambient_humidity_pct: humidity, pollution_aqi: aqi },
    formulation_synthesis: { selected_actives: actives, contraindicated_actives: contra },
    timestamp: new Date().toISOString()
  };

  const blob = new Blob([JSON.stringify(protocol, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `dermapulse_protocol_${currentArch}.json`;
  a.click();
  URL.revokeObjectURL(url);
});

// Init
updateUI();
requestAnimationFrame(animate);
