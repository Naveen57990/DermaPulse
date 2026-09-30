#!/usr/bin/env python3
"""
DermaPulse AI Studio Demo Video Generator
Generates a 1080p demo video with natural voiceover and cyberdeck HUD slides.
"""

import os
import subprocess
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEMO_DIR = BASE_DIR / "demo"
ASSETS_DIR = BASE_DIR / "assets"
OUT_VIDEO = DEMO_DIR / "dermapulse_demo.mp4"

SECTIONS = [
    {
        "title": "DermaPulse AI: Precision Dermal Biometrics",
        "subtitle": "Powered by YouCam Skin AI Diagnostic Telemetry & Formulation Synthesizer",
        "text": "Welcome to DermaPulse AI. Standard skincare advice relies on subjective self-reporting and guesswork. DermaPulse AI combines Perfect Corp's YouCam Skin AI diagnostic API with clinical dermal biometrics to calculate barrier integrity, biological skin age, and active molecular formulas tailored to your circadian biology.",
        "accent": "#00e5ff",
        "metrics": "YouCam Skin AI API • 7 Diagnostic Vectors • Circadian Regimens"
    },
    {
        "title": "Dermal Barrier Integrity & Biological Skin Age",
        "subtitle": "Continuous Epidermal Health Scoring & Photo-Aging Regression",
        "text": "Using seven multi-zone dermal biomarkers—including stratum corneum hydration, sebaceous lipids, vascular erythema, texture, and periorbital fine lines—DermaPulse computes a continuous Barrier Integrity Index from zero to one hundred, alongside biological skin age differentials.",
        "accent": "#00e699",
        "metrics": "Barrier Integrity Index (0-100) • Biological Skin Age • Zone Mapping"
    },
    {
        "title": "Molecular Formulation & Safety Contraindications",
        "subtitle": "Intelligent Active Synthesis with Automated Barrier Protection Gates",
        "text": "Our formulation synthesizer matches cellular deficiencies to clinical actives like bio-identical ceramides, centella, and retinaldehyde. When barrier integrity is compromised, the safety gate automatically blocks high-irritation retinoids and chemical exfoliants to prevent dermal damage.",
        "accent": "#ffb800",
        "metrics": "Bio-Identical Actives • Automatic Safety Gates • Zero Retinoid Stinging"
    },
    {
        "title": "Circadian Regimens with Environmental Scaling",
        "subtitle": "Adapting to UV Index, Humidity & Smog • Live on Vercel Production",
        "text": "DermaPulse AI generates targeted AM photoprotective shields and PM lamellar lipid repair regimens, dynamically scaling active ingredients against real-time solar UV, humidity, and pollution. Explore our live interactive console at dermapulse.vercel.app.",
        "accent": "#2f80ed",
        "metrics": "8/8 Tests in 0.001s • Live Production Console: dermapulse.vercel.app"
    }
]


def generate_tts_audio(text: str, out_path: str):
    subprocess.run(["say", "-v", "Samantha", "-r", "175", text, "-o", out_path])


def render_slide(section, out_img_path):
    title = section["title"]
    sub = section["subtitle"]
    metrics = section["metrics"]
    accent = section["accent"]
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                margin: 0;
                width: 1920px;
                height: 1080px;
                background: radial-gradient(circle at top right, #0d1726 0%, #060a12 100%);
                color: #f8fafc;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                padding: 80px 100px;
                box-sizing: border-box;
                overflow: hidden;
            }}
            .header {{
                display: flex;
                align-items: center;
                gap: 20px;
            }}
            .badge {{
                background: rgba(0, 229, 255, 0.15);
                color: #00e5ff;
                border: 1px solid rgba(0, 229, 255, 0.4);
                padding: 6px 18px;
                border-radius: 9999px;
                font-family: monospace;
                font-size: 18px;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            .main-content {{
                margin-top: 40px;
            }}
            h1 {{
                font-size: 56px;
                font-weight: 800;
                margin: 0 0 16px 0;
                letter-spacing: -1px;
                background: linear-gradient(135deg, #ffffff 30%, {accent} 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            h2 {{
                font-size: 28px;
                font-weight: 500;
                color: #94a3b8;
                margin: 0 0 35px 0;
            }}
            .metrics-box {{
                display: inline-block;
                background: rgba(17, 23, 34, 0.9);
                border: 1px solid rgba(0, 229, 255, 0.25);
                border-radius: 16px;
                padding: 16px 30px;
                font-family: monospace;
                font-size: 22px;
                color: {accent};
                box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
            }}
            .footer {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
                padding-top: 25px;
                font-family: monospace;
                font-size: 16px;
                color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="badge">DERMAPULSE CLINICAL CORE</div>
            <span style="font-family: monospace; color: #64748b; font-size: 18px;">YOUCAM API SKIN AI & ECOMMERCE VTO HACKATHON 2026</span>
        </div>
        <div class="main-content">
            <h1>{title}</h1>
            <h2>{sub}</h2>
            <div class="metrics-box">{metrics}</div>
        </div>
        <div class="footer">
            <span>DETERMINISTIC BIOMETRIC SYNTHESIZER (0.001s)</span>
            <span>LIVE CONSOLE: dermapulse.vercel.app</span>
        </div>
    </body>
    </html>
    """
    
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        tmp_html = f.name
        
    subprocess.run([
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--headless",
        "--disable-gpu",
        "--screenshot=" + out_img_path,
        "--window-size=1920,1080",
        f"file://{tmp_html}"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    os.unlink(tmp_html)


def main():
    print("[*] Generating DermaPulse AI 1080p Studio Demo Video...")
    DEMO_DIR.mkdir(exist_ok=True)
    
    temp_clips = []
    
    for idx, sec in enumerate(SECTIONS):
        print(f"  -> Rendering Segment {idx+1}/{len(SECTIONS)}: {sec['title']}")
        audio_aiff = str(DEMO_DIR / f"segment_{idx}.aiff")
        audio_wav = str(DEMO_DIR / f"segment_{idx}.wav")
        slide_png = str(DEMO_DIR / f"slide_{idx}.png")
        segment_mp4 = str(DEMO_DIR / f"segment_{idx}.mp4")
        
        generate_tts_audio(sec["text"], audio_aiff)
        subprocess.run(["ffmpeg", "-y", "-i", audio_aiff, "-ac", "2", "-ar", "44100", audio_wav], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", audio_wav
        ], capture_output=True, text=True)
        duration = float(probe.stdout.strip()) + 0.8
        
        render_slide(sec, slide_png)
        
        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", slide_png, "-i", audio_wav,
            "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k",
            "-pix_fmt", "yuv420p", "-t", str(duration), segment_mp4
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        temp_clips.append(segment_mp4)
        
    concat_list_file = DEMO_DIR / "concat_list.txt"
    with open(concat_list_file, "w") as f:
        for clip in temp_clips:
            f.write(f"file '{clip}'\n")
            
    print("[*] Stitching segments into final production video...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list_file),
        "-c", "copy", str(OUT_VIDEO)
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    probe_final = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(OUT_VIDEO)
    ], capture_output=True, text=True)
    total_dur = float(probe_final.stdout.strip())
    
    print(f"[✓] Final Video Rendered: {OUT_VIDEO} ({total_dur:.2f}s, 1080p HD)")


if __name__ == "__main__":
    main()
