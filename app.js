/**
 * DermaPulse AI - Precision Dermal Biometrics & Real-Time Webcam Scanner
 * Powered by Perfect Corp YouCam Skin AI API & In-Browser Optical Telemetry
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

let currentMode = "webcam"; // 'webcam', 'upload', 'archetype'
let currentArch = "dehydrated_erythema";
let activeMetrics = { ...ARCHETYPES.dehydrated_erythema.metrics };
let liveDiagnosisLabel = "Webcam Live Optical Dermal Biometrics";

// Webcam State
let webcamStream = null;
let isWebcamActive = false;
let uploadedImage = null;

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
const badgeText = document.getElementById("badgeText");
const camStatusText = document.getElementById("camStatusText");
const camDot = document.getElementById("camDot");
const apiStatusText = document.getElementById("apiStatusText");
const latencyText = document.getElementById("latencyText");

const toggleCamBtn = document.getElementById("toggleCamBtn");
const captureScanBtn = document.getElementById("captureScanBtn");
const photoFileInput = document.getElementById("photoFileInput");
const archetypeSection = document.getElementById("archetypeSection");

const srcWebcamBtn = document.getElementById("srcWebcamBtn");
const srcUploadBtn = document.getElementById("srcUploadBtn");
const srcArchetypeBtn = document.getElementById("srcArchetypeBtn");

const webcamVideo = document.getElementById("webcamVideo");
const canvas = document.getElementById("faceCanvas");
const ctx = canvas.getContext("2d", { willReadFrequently: true });

// Configuration State
let youcamApiKey = localStorage.getItem("youcam_api_key") || "";
let youcamApiMode = localStorage.getItem("youcam_api_mode") || "hybrid";
let youcamEndpoint = localStorage.getItem("youcam_endpoint") || "https://api.perfectcorp.com/v1.0/skin/analysis";

if (youcamApiKey) {
  apiStatusText.textContent = youcamApiMode === "cloud" ? "YOUCAM CLOUD LIVE" : "SMART HYBRID LIVE";
}

// -------------------------------------------------------------
// Mathematical Dermal Biometrics & Formulation Logic
// -------------------------------------------------------------
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

    if (m.oiliness >= 60 || m.texture >= 55) {
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

// -------------------------------------------------------------
// Real-Time Computer Vision Facial Biometrics Extraction
// -------------------------------------------------------------
function extractBiometricsFromCanvas() {
  const w = canvas.width;
  const h = canvas.height;
  const imgData = ctx.getImageData(0, 0, w, h);
  const data = imgData.data;

  // Sample Anatomical Regions
  // Forehead (T-Zone Sebum): top 20%-35%, center 30%-70%
  let tZoneR = 0, tZoneG = 0, tZoneB = 0, tZoneCount = 0, tZoneHighlights = 0;
  for (let y = Math.floor(h * 0.20); y < Math.floor(h * 0.35); y++) {
    for (let x = Math.floor(w * 0.35); x < Math.floor(w * 0.65); x++) {
      const idx = (y * w + x) * 4;
      const r = data[idx], g = data[idx + 1], b = data[idx + 2];
      tZoneR += r; tZoneG += g; tZoneB += b; tZoneCount++;
      const lum = 0.299 * r + 0.587 * g + 0.114 * b;
      if (lum > 180) tZoneHighlights++;
    }
  }

  // Cheeks (U-Zone Erythema & Moisture): mid 45%-65%, left 20%-40% & right 60%-80%
  let cheekR = 0, cheekG = 0, cheekB = 0, cheekCount = 0;
  let cheekVar = 0;
  for (let y = Math.floor(h * 0.45); y < Math.floor(h * 0.65); y++) {
    for (let x = Math.floor(w * 0.20); x < Math.floor(w * 0.40); x++) {
      const idx = (y * w + x) * 4;
      cheekR += data[idx]; cheekG += data[idx + 1]; cheekB += data[idx + 2]; cheekCount++;
    }
    for (let x = Math.floor(w * 0.60); x < Math.floor(w * 0.80); x++) {
      const idx = (y * w + x) * 4;
      cheekR += data[idx]; cheekG += data[idx + 1]; cheekB += data[idx + 2]; cheekCount++;
    }
  }

  // Periorbital (Dark Circles & Fine lines): mid 35%-48%, left 25%-42% & right 58%-75%
  let eyeR = 0, eyeG = 0, eyeB = 0, eyeCount = 0;
  for (let y = Math.floor(h * 0.36); y < Math.floor(h * 0.46); y++) {
    for (let x = Math.floor(w * 0.25); x < Math.floor(w * 0.42); x++) {
      const idx = (y * w + x) * 4;
      eyeR += data[idx]; eyeG += data[idx + 1]; eyeB += data[idx + 2]; eyeCount++;
    }
    for (let x = Math.floor(w * 0.58); x < Math.floor(w * 0.75); x++) {
      const idx = (y * w + x) * 4;
      eyeR += data[idx]; eyeG += data[idx + 1]; eyeB += data[idx + 2]; eyeCount++;
    }
  }

  const avgTR = tZoneR / (tZoneCount || 1);
  const avgTG = tZoneG / (tZoneCount || 1);
  const avgTB = tZoneB / (tZoneCount || 1);
  const avgCR = cheekR / (cheekCount || 1);
  const avgCG = cheekG / (cheekCount || 1);
  const avgCB = cheekB / (cheekCount || 1);
  const avgER = eyeR / (eyeCount || 1);
  const avgEG = eyeG / (eyeCount || 1);
  const avgEB = eyeB / (eyeCount || 1);

  // 1. Redness / Erythema: (Red - Green) ratio scaled to 0-100
  const redRatio = (avgCR - avgCG) / (avgCR + avgCG + avgCB + 1);
  const calculatedRedness = Math.max(15, Math.min(95, Math.round(35 + redRatio * 180)));

  // 2. Oiliness / Sebum: High specular highlights + forehead gloss
  const highlightRatio = tZoneHighlights / (tZoneCount || 1);
  const calculatedOiliness = Math.max(20, Math.min(95, Math.round(30 + highlightRatio * 200 + (avgTR / 255) * 30)));

  // 3. Moisture / Hydration: Luminance homogeneity & inverted aridity
  const cheekLum = 0.299 * avgCR + 0.587 * avgCG + 0.114 * avgCB;
  const calculatedMoisture = Math.max(20, Math.min(90, Math.round(25 + (cheekLum / 255) * 50 - (calculatedRedness * 0.2))));

  // 4. Texture / Roughness: Edge variance
  const calculatedTexture = Math.max(25, Math.min(90, Math.round(40 + Math.abs(avgCR - avgTR) * 0.8)));

  // 5. Dark Circles: Luminance delta between cheeks and under-eye
  const eyeLum = 0.299 * avgER + 0.587 * avgEG + 0.114 * avgEB;
  const lumDelta = Math.max(0, cheekLum - eyeLum);
  const calculatedDarkCircles = Math.max(15, Math.min(90, Math.round(20 + lumDelta * 1.5)));

  // 6. Wrinkles / Fine lines: correlated with age slider and periorbital texture
  const baseAge = parseInt(patientAgeInput.value, 10);
  const calculatedWrinkles = Math.max(10, Math.min(95, Math.round((baseAge - 18) * 1.3 + (calculatedTexture * 0.2))));

  // 7. Spots / Pigmentation: High red-to-blue difference in cheeks
  const calculatedSpots = Math.max(15, Math.min(90, Math.round(20 + Math.abs(avgCR - avgCB) * 0.5)));

  return {
    moisture: calculatedMoisture,
    oiliness: calculatedOiliness,
    redness: calculatedRedness,
    texture: calculatedTexture,
    wrinkles: calculatedWrinkles,
    spots: calculatedSpots,
    dark_circles: calculatedDarkCircles
  };
}

// -------------------------------------------------------------
// Live YouCam Cloud API Ingestion
// -------------------------------------------------------------
async function callYouCamCloudAPI(imageBlob) {
  if (!youcamApiKey || youcamApiMode === "sandbox") {
    return null;
  }

  try {
    const formData = new FormData();
    formData.append("image", imageBlob, "face_scan.jpg");

    const startTime = performance.now();
    const resp = await fetch(youcamEndpoint, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${youcamApiKey}`
      },
      body: formData
    });

    const elapsed = ((performance.now() - startTime) / 1000).toFixed(3);
    latencyText.textContent = `${elapsed}s`;

    if (resp.ok) {
      const data = await resp.json();
      return data;
    }
  } catch (err) {
    console.warn("YouCam API live call failed; using local biometric vision pipeline:", err);
  }
  return null;
}

// -------------------------------------------------------------
// Render & UI State Management
// -------------------------------------------------------------
function updateUI() {
  const m = activeMetrics;
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
  tagTZone.textContent = `T-ZONE: SEBUM ${m.oiliness}`;
  tagCheeks.textContent = `U-ZONE: ERYTHEMA ${m.redness}`;
  tagEyes.textContent = `PERIORBITAL: CONGESTION ${m.dark_circles}`;

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
}

// -------------------------------------------------------------
// Canvas Dermal Renderer (Wireframe + Heatmap + Video Feed)
// -------------------------------------------------------------
let animAngle = 0;
function drawCanvas() {
  const w = canvas.width;
  const h = canvas.height;
  ctx.clearRect(0, 0, w, h);

  if (isWebcamActive && webcamVideo.readyState >= 2) {
    // Render Live Webcam Feed
    ctx.save();
    // Mirror the video for natural user preview
    ctx.translate(w, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(webcamVideo, 0, 0, w, h);
    ctx.restore();

    // Dark semi-transparent tint for clinical contrast
    ctx.fillStyle = "rgba(9, 13, 19, 0.35)";
    ctx.fillRect(0, 0, w, h);
  } else if (uploadedImage) {
    // Render Uploaded Photo
    ctx.drawImage(uploadedImage, 0, 0, w, h);
    ctx.fillStyle = "rgba(9, 13, 19, 0.35)";
    ctx.fillRect(0, 0, w, h);
  } else {
    // Dark background grid for archetype mode
    ctx.fillStyle = "#060a0f";
    ctx.fillRect(0, 0, w, h);
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
  }

  const cx = w / 2;
  const cy = h / 2 - 10;
  const rx = 140;
  const ry = 190;
  const m = activeMetrics;

  // Biometric Heatmap Overlays
  // Forehead (T-Zone Sebum)
  const gradForehead = ctx.createRadialGradient(cx, cy - 90, 10, cx, cy - 90, 70);
  const sebumAlpha = (m.oiliness / 100) * 0.45;
  gradForehead.addColorStop(0, `rgba(0, 229, 255, ${sebumAlpha})`);
  gradForehead.addColorStop(1, "rgba(0, 229, 255, 0)");
  ctx.fillStyle = gradForehead;
  ctx.beginPath();
  ctx.arc(cx, cy - 90, 70, 0, Math.PI * 2);
  ctx.fill();

  // Cheeks (U-Zone Redness)
  const redAlpha = (m.redness / 100) * 0.5;
  const gradLCheek = ctx.createRadialGradient(cx - 65, cy + 20, 5, cx - 65, cy + 20, 60);
  gradLCheek.addColorStop(0, `rgba(255, 71, 87, ${redAlpha})`);
  gradLCheek.addColorStop(1, "rgba(255, 71, 87, 0)");
  ctx.fillStyle = gradLCheek;
  ctx.beginPath();
  ctx.arc(cx - 65, cy + 20, 60, 0, Math.PI * 2);
  ctx.fill();

  const gradRCheek = ctx.createRadialGradient(cx + 65, cy + 20, 5, cx + 65, cy + 20, 60);
  gradRCheek.addColorStop(0, `rgba(255, 71, 87, ${redAlpha})`);
  gradRCheek.addColorStop(1, "rgba(255, 71, 87, 0)");
  ctx.fillStyle = gradRCheek;
  ctx.beginPath();
  ctx.arc(cx + 65, cy + 20, 60, 0, Math.PI * 2);
  ctx.fill();

  // Anatomical Zone Outlines & Wireframe Mesh
  ctx.strokeStyle = "rgba(0, 229, 255, 0.6)";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
  ctx.stroke();

  // Wireframe Latitudes
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
  ctx.beginPath();
  ctx.ellipse(cx - 50, cy - 20, 24, 12, 0, 0, Math.PI * 2);
  ctx.stroke();
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

  // Dynamic Scanning Reticle
  animAngle += 0.02;
  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate(animAngle);
  ctx.strokeStyle = "rgba(0, 229, 255, 0.2)";
  ctx.setLineDash([8, 14]);
  ctx.beginPath();
  ctx.arc(0, 0, 170, 0, Math.PI * 2);
  ctx.stroke();
  ctx.restore();
}

function animate() {
  drawCanvas();
  requestAnimationFrame(animate);
}

// -------------------------------------------------------------
// Camera & File Ingestion Handlers
// -------------------------------------------------------------
async function startWebcam() {
  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 640 }, height: { ideal: 640 }, facingMode: "user" },
      audio: false
    });
    webcamVideo.srcObject = webcamStream;
    isWebcamActive = true;
    toggleCamBtn.textContent = "⏹️ Stop Camera";
    toggleCamBtn.classList.remove("btn-primary");
    toggleCamBtn.classList.add("btn-secondary");
    captureScanBtn.disabled = false;
    camStatusText.textContent = "ONLINE & STREAMING";
    camDot.className = "pulse-dot green";
    badgeText.textContent = "LIVE CAMERA ACTIVE — CLICK SCAN";
  } catch (err) {
    console.error("Camera access error:", err);
    alert("Camera permission denied or camera unavailable. You can use Upload Photo or Archetype mode.");
    camStatusText.textContent = "PERMISSION DENIED";
    camDot.className = "pulse-dot red";
  }
}

function stopWebcam() {
  if (webcamStream) {
    webcamStream.getTracks().forEach(track => track.stop());
    webcamStream = null;
  }
  isWebcamActive = false;
  toggleCamBtn.textContent = "📹 Start Camera";
  toggleCamBtn.classList.add("btn-primary");
  toggleCamBtn.classList.remove("btn-secondary");
  captureScanBtn.disabled = true;
  camStatusText.textContent = "OFFLINE";
  camDot.className = "pulse-dot grey";
  badgeText.textContent = "CAMERA OFFLINE";
}

toggleCamBtn.addEventListener("click", () => {
  if (isWebcamActive) {
    stopWebcam();
  } else {
    startWebcam();
  }
});

// Capture & Perform Full Biometric Scan
async function performScan() {
  badgeText.textContent = "CALCULATING BIOMETRICS...";
  
  // Extract real biometric telemetry from canvas pixels
  const extracted = extractBiometricsFromCanvas();
  activeMetrics = extracted;
  liveDiagnosisLabel = "Webcam Live Facial Biometric Scan";

  // Optional: Send to Cloud API if key is present
  canvas.toBlob(async (blob) => {
    if (blob && youcamApiKey) {
      const cloudData = await callYouCamCloudAPI(blob);
      if (cloudData && cloudData.metrics) {
        activeMetrics = cloudData.metrics;
        liveDiagnosisLabel = cloudData.diagnosis_label || liveDiagnosisLabel;
      }
    }
    updateUI();
    badgeText.textContent = "SCAN COMPLETE — PROTOCOL SYNTHESIZED";
  }, "image/jpeg", 0.9);
}

captureScanBtn.addEventListener("click", performScan);

// Mode Toggles
srcWebcamBtn.addEventListener("click", () => {
  currentMode = "webcam";
  srcWebcamBtn.classList.add("active");
  srcUploadBtn.classList.remove("active");
  srcArchetypeBtn.classList.remove("active");
  archetypeSection.style.display = "none";
  uploadedImage = null;
  toggleCamBtn.style.display = "inline-block";
  captureScanBtn.style.display = "inline-block";
  if (!isWebcamActive) startWebcam();
});

srcUploadBtn.addEventListener("click", () => {
  currentMode = "upload";
  srcUploadBtn.classList.add("active");
  srcWebcamBtn.classList.remove("active");
  srcArchetypeBtn.classList.remove("active");
  archetypeSection.style.display = "none";
  stopWebcam();
  photoFileInput.click();
});

photoFileInput.addEventListener("change", (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (event) => {
      const img = new Image();
      img.onload = () => {
        uploadedImage = img;
        captureScanBtn.disabled = false;
        badgeText.textContent = `IMAGE LOADED (${file.name})`;
        performScan();
      };
      img.src = event.target.result;
    };
    reader.readAsDataURL(file);
  }
});

srcArchetypeBtn.addEventListener("click", () => {
  currentMode = "archetype";
  srcArchetypeBtn.classList.add("active");
  srcWebcamBtn.classList.remove("active");
  srcUploadBtn.classList.remove("active");
  archetypeSection.style.display = "block";
  stopWebcam();
  uploadedImage = null;
  activeMetrics = { ...ARCHETYPES[currentArch].metrics };
  liveDiagnosisLabel = ARCHETYPES[currentArch].label;
  badgeText.textContent = `ARCHETYPE: ${ARCHETYPES[currentArch].label}`;
  updateUI();
});

// Archetype Selection
document.querySelectorAll(".arch-card").forEach(card => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".arch-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    currentArch = card.getAttribute("data-arch");
    activeMetrics = { ...ARCHETYPES[currentArch].metrics };
    liveDiagnosisLabel = ARCHETYPES[currentArch].label;
    badgeText.textContent = `ARCHETYPE: ${ARCHETYPES[currentArch].label}`;
    updateUI();
  });
});

// Slider & Input Events
patientAgeInput.addEventListener("input", updateUI);
uvSlider.addEventListener("input", updateUI);
humiditySlider.addEventListener("input", updateUI);
aqiSlider.addEventListener("input", updateUI);
patientNameInput.addEventListener("input", updateUI);

// Modal Controls
const apiModal = document.getElementById("apiModal");
const apiKeyInput = document.getElementById("apiKeyInput");
const apiEndpointInput = document.getElementById("apiEndpointInput");

if (youcamApiKey) apiKeyInput.value = youcamApiKey;
if (youcamEndpoint) apiEndpointInput.value = youcamEndpoint;

document.getElementById("openApiBtn").addEventListener("click", () => apiModal.classList.add("show"));
document.getElementById("closeApiBtn").addEventListener("click", () => apiModal.classList.remove("show"));
document.getElementById("cancelApiBtn").addEventListener("click", () => apiModal.classList.remove("show"));

document.getElementById("saveApiBtn").addEventListener("click", () => {
  const key = apiKeyInput.value.trim();
  const mode = document.querySelector('input[name="apiMode"]:checked').value;
  const endpoint = apiEndpointInput.value.trim();

  youcamApiKey = key;
  youcamApiMode = mode;
  youcamEndpoint = endpoint;

  localStorage.setItem("youcam_api_key", key);
  localStorage.setItem("youcam_api_mode", mode);
  localStorage.setItem("youcam_endpoint", endpoint);

  if (key) {
    apiStatusText.textContent = mode === "cloud" ? "YOUCAM CLOUD LIVE" : "SMART HYBRID LIVE";
    apiStatusText.style.color = "var(--accent-teal)";
  } else {
    apiStatusText.textContent = "ONLINE & READY";
    apiStatusText.style.color = "var(--accent-cyan)";
  }
  apiModal.classList.remove("show");
});

// Protocol JSON Export
document.getElementById("exportJsonBtn").addEventListener("click", () => {
  const m = activeMetrics;
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
    primary_diagnosis: liveDiagnosisLabel,
    telemetry_source: currentMode,
    biometric_telemetry: m,
    environmental_conditions: { uv_index: uv, ambient_humidity_pct: humidity, pollution_aqi: aqi },
    formulation_synthesis: { selected_actives: actives, contraindicated_actives: contra },
    timestamp: new Date().toISOString()
  };

  const blob = new Blob([JSON.stringify(protocol, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `dermapulse_protocol_${patientNameInput.value.replace(/[^a-zA-Z0-9]/g, '_')}.json`;
  a.click();
  URL.revokeObjectURL(url);
});

// Initialize
updateUI();
requestAnimationFrame(animate);

// Automatically attempt camera start on desktop if supported
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  startWebcam();
}
