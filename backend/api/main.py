from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Dict, Any
import sys
import os
import requests
from dotenv import load_dotenv

load_dotenv()

from datetime import datetime

# Add parent directory to path to allow importing backend modules when run directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.engine.math_engine import VedicMathEngine
from backend.engine.astrology import AstrologyEngine
from backend.engine.compiler import PredictionCompiler
from backend.engine.dasha import DashaCalculator
from backend.engine.matchmaker import MatchMaker
from backend.engine.transits import TransitEngine
from backend.rules.kp_evaluator import KPEvaluator
from backend.database import init_db, save_report, get_report

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Astro-Naught API",
    description="KP (Krishnamurti Paddhati) Astrology Engine",
    version="2.0.0"
)

@app.on_event("startup")
def startup_event():
    init_db()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://astro-naught.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines at startup to load ephemeris or constants once if needed
math_engine = VedicMathEngine()
astrology_engine = AstrologyEngine()

# Request Model
class BirthData(BaseModel):
    name: str = Field(..., description="Name of the person.")
    gender: str = Field(..., description="Gender (e.g., Male, Female, Other).")
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    utc_hour: float = Field(..., ge=0, le=24, description="Hour in UTC (24-hour format).")
    utc_minute: float = Field(..., ge=0, le=59, description="Minute in UTC.")
    latitude: float = Field(..., description="Latitude (e.g., 28.6139 for Delhi).")
    longitude: float = Field(..., description="Longitude (e.g., 77.2090 for Delhi).")
    ayanamsa_type: str = Field(default="kp", description="Ayanamsa calculation algorithm. Supports 'lahiri' or 'kp'. Defaults to 'kp'.")
    preferred_system: str = Field(default="kp", description="Preferred astrology system for AI oracle (e.g., 'kp' or 'vedic').")

class MatchRequest(BaseModel):
    person_a: BirthData
    person_b: BirthData

class TransitRequest(BaseModel):
    person: BirthData

class RulingPlanetRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    utc_hour: float = Field(..., ge=0, le=24)
    utc_minute: float = Field(..., ge=0, le=59)
    latitude: float = Field(...)
    longitude: float = Field(...)

class ShareRequest(BaseModel):
    type: str 
    input_payload: Dict[str, Any]
    result_payload: Dict[str, Any]
    source_report_code: str = None

class ExplainRequest(BaseModel):
    context: str
    topic: str

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Astro-Naught KP Engine", "version": "2.0.0"}

@app.post("/api/v1/chart")
def generate_chart(data: BirthData):
    """
    Returns the raw mathematical astrological chart data including planets, houses,
    KP cusps with sub-lords, KP significators, and KP numbers.
    """
    try:
        math_output = math_engine.calculate_positions(
            data.year, data.month, data.day, 
            data.utc_hour, data.utc_minute, 
            data.latitude, data.longitude,
            data.ayanamsa_type
        )
        chart_data = astrology_engine.generate_chart(math_output, data.ayanamsa_type.upper())
        
        # Attach personal data for the frontend to render the top-level chart context
        chart_data["personal_info"] = {
            "name": data.name,
            "gender": data.gender
        }
        
        return chart_data
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Chart Calculation Error: {str(e)}")

@app.post("/api/v1/predictions")
def generate_predictions(data: BirthData):
    """
    Analyzes the chart and returns a compiled deterministic profile with both
    classical Jyotish and KP analysis ready for an AI styling wrapper.
    """
    try:
        math_output = math_engine.calculate_positions(
            data.year, data.month, data.day, 
            data.utc_hour, data.utc_minute, 
            data.latitude, data.longitude,
            data.ayanamsa_type
        )
        chart_data = astrology_engine.generate_chart(math_output, data.ayanamsa_type.upper())
        
        compiler = PredictionCompiler(chart_data)
        profile = compiler.build_full_profile()
        return profile
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction Engine Error: {str(e)}")

@app.post("/api/v1/match")
def match_charts(data: MatchRequest):
    """
    Compares two charts for deterministic compatibility.
    """
    try:
        # Generate Chart A
        math_output_a = math_engine.calculate_positions(
            data.person_a.year, data.person_a.month, data.person_a.day, 
            data.person_a.utc_hour, data.person_a.utc_minute, 
            data.person_a.latitude, data.person_a.longitude,
            data.person_a.ayanamsa_type
        )
        chart_a = astrology_engine.generate_chart(math_output_a, data.person_a.ayanamsa_type.upper())

        # Generate Chart B
        math_output_b = math_engine.calculate_positions(
            data.person_b.year, data.person_b.month, data.person_b.day, 
            data.person_b.utc_hour, data.person_b.utc_minute, 
            data.person_b.latitude, data.person_b.longitude,
            data.person_b.ayanamsa_type
        )
        chart_b = astrology_engine.generate_chart(math_output_b, data.person_b.ayanamsa_type.upper())

        matcher = MatchMaker(chart_a, chart_b)
        result = matcher.run_match()

        return {
            "person_a_info": {"name": data.person_a.name, "ascendant": chart_a.get("ascendant", {}).get("sign")},
            "person_b_info": {"name": data.person_b.name, "ascendant": chart_b.get("ascendant", {}).get("sign")},
            "match_report": result
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ruling Planets Error: {str(e)}")

@app.post("/api/v1/explain")
def get_ai_explanation(data: ExplainRequest):
    """
    Acts as a 'Translator' for the deterministic engine.
    Uses a cheap, fast Gemini call to explain a specific astrological finding.
    """
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("GROQ_API_KEY"):
        raise HTTPException(status_code=503, detail="AI Translator is currently offline. Missing API Key.")
        
    prompt = f"""
You are an elite, empathetic Astrological Translator. 
Your job is to take raw, deterministic astrological outputs and explain them in plain English to the user.
Keep your answer to exactly 2-4 short sentences. Do not use overly mystical jargon, just explain *why* the engine said this.

Context from the engine about '{data.topic}':
{data.context}

Explanation:
"""
    try:
        groq_key = os.getenv("GROQ_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if groq_key:
            # Use Groq API (Llama 3) - Ultra fast fallback
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {groq_key}"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are an expert Vedic astrologer acting as an AI Translator. Your job is to explain the raw astrological data provided to the user in a short, encouraging way. You MUST explicitly name the specific planets, houses, or signs that are causing this effect (e.g., 'Because Jupiter is transiting your 7th house...') so the user learns the actual astrology behind the prediction."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                return {"explanation": f"Groq API Error ({response.status_code}): {response.text}"}
                
            data = response.json()
            try:
                text = data["choices"][0]["message"]["content"]
                return {"explanation": text.strip()}
            except (KeyError, IndexError):
                return {"explanation": "Groq could not generate a response for this specific calculation."}
                
        elif gemini_key:
            # Use Gemini API
            url = "https://generativelanguage.googleapis.com/v1beta/interactions"
            headers = {
                'Content-Type': 'application/json',
                'x-goog-api-key': gemini_key
            }
            payload = {
                "model": "gemini-3.5-flash",
                "input": prompt
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code != 200:
                return {"explanation": f"Gemini API Error ({response.status_code}): {response.text}"}
                
            data = response.json()
            
            # Extract response from new Interactions API format
            try:
                text = data.get("output_text") or data["outputs"][0]["text"]
                return {"explanation": text.strip()}
            except (KeyError, IndexError, TypeError):
                return {"explanation": "The AI Translator could not generate a response for this specific calculation."}
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate explanation: {str(e)}")

@app.post("/api/v1/share")
def create_share_link(data: ShareRequest):
    """Saves a generated report snapshot and returns a short link code."""
    try:
        short_code = save_report(
            report_type=data.type,
            input_payload=data.input_payload,
            result_payload=data.result_payload,
            source_report_code=data.source_report_code
        )
        return {"short_code": short_code}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create share link: {str(e)}")

@app.get("/api/v1/share/{short_code}")
def read_share_link(short_code: str):
    """Retrieves a shared report snapshot and increments the view count."""
    try:
        report = get_report(short_code)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found or link expired.")
        return report
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to retrieve report: {str(e)}")

@app.post("/api/v1/transits")
def get_daily_transits(data: TransitRequest):
    """
    Calculates the user's natal chart, then calculates where the planets are *today*,
    and generates deterministic daily/monthly/yearly insights.
    """
    from datetime import datetime
    try:
        # Generate Natal Chart
        math_output_natal = math_engine.calculate_positions(
            data.person.year, data.person.month, data.person.day, 
            data.person.utc_hour, data.person.utc_minute, 
            data.person.latitude, data.person.longitude,
            data.person.ayanamsa_type
        )
        natal_chart = astrology_engine.generate_chart(math_output_natal, data.person.ayanamsa_type.upper())

        # Generate Transit Chart (Today at 12:00 UTC)
        now = datetime.utcnow()
        math_output_transit = math_engine.calculate_positions(
            now.year, now.month, now.day,
            12.0, 0.0,
            data.person.latitude, data.person.longitude, # Location doesn't matter much for planet degrees, but we use the user's birth location for consistency
            data.person.ayanamsa_type
        )
        transit_chart = astrology_engine.generate_chart(math_output_transit, data.person.ayanamsa_type.upper())
        
        transit_engine = TransitEngine(natal_chart, transit_chart["planets"])
        insights = transit_engine.generate_daily_insights()

        return {
            "date": now.strftime("%Y-%m-%d"),
            "insights": insights
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Transit Engine Error: {str(e)}")

@app.post("/api/v1/ruling-planets")
def get_ruling_planets(data: RulingPlanetRequest):
    """
    Returns the 5 Ruling Planets for a given datetime and location.
    Used in KP horary astrology for precise timing of events.
    
    The 5 components: Day Lord, Moon Sign Lord, Moon Star Lord,
    Lagna Sign Lord, Lagna Star Lord.
    """
    try:
        math_output = math_engine.calculate_positions(
            data.year, data.month, data.day,
            data.utc_hour, data.utc_minute,
            data.latitude, data.longitude,
            "kp"
        )
        chart_data = astrology_engine.generate_chart(math_output, "KP")
        
        query_dt = datetime(data.year, data.month, data.day,
                           int(data.utc_hour), int(data.utc_minute))
        
        evaluator = KPEvaluator(chart_data)
        ruling = evaluator.get_ruling_planets(query_dt)
        
        return ruling
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ruling Planet Calculation Error: {str(e)}")

@app.post("/api/v1/ai-insights")
def generate_ai_insights(data: BirthData):
    """
    Wraps the deterministic KP prediction engine and sends the factual ground truth
    to a local Ollama LLM for a polished, human-readable reading.
    """
    import json
    import urllib.request
    import urllib.error
    
    try:
        # 1. Fetch deterministic truth
        math_output = math_engine.calculate_positions(
            data.year, data.month, data.day, 
            data.utc_hour, data.utc_minute, 
            data.latitude, data.longitude,
            data.ayanamsa_type
        )
        chart_data = astrology_engine.generate_chart(math_output, data.ayanamsa_type.upper())
        compiler = PredictionCompiler(chart_data)
        profile = compiler.build_full_profile()
        
        # 2. Build explicit prompt based on preferred system
        system_type = data.preferred_system.lower()
        if system_type == "vedic":
            prompt = f"""[SYSTEM ROLE: ELITE VEDIC ASTROLOGY ANALYST]
You are performing a deep-layer, soulful, and professional reading for {data.name}. 
Do NOT use generic fluff. Be authoritative, intuitive, and data-driven.

CRITICAL RULES:
- DO NOT mention raw 'scores', 'verdicts', 'percentages', or JSON key names (e.g., do not say "Vedic Score is 1" or "Confidence: 85%").
- USE the 'Narrative Context' and 'Yogas' as your deep research notes.
- Your goal is to sound like an INTUITIVE HUMAN EXPERT who has already processed the math and is now delivering the wisdom.

STRUCTURE:

# 🧭 1. Lagna & Core Personality
*   **Ascendant**: {profile.get("ascendant", {}).get("sign", "Unknown")} (Lord: {profile.get("ascendant", {}).get("lord", "Unknown")})
*   Deliver a powerful 3-4 sentence insight into their soul's purpose.

# 📊 2. Planetary Strength & Synergy (D1 vs D9)
*   Create a MARKDOWN TABLE [Planet, D1 Rashi, D9 Navamsa, Soul Strength]
*   Use 'Soul Strength' (e.g., Strong, Vargottama, Challenged) instead of 'Verdict'.

# 💼 3. The Path of Career & Success
*   Analysis Logic: {json.dumps(profile.get("event_synthesis", {}).get("career", {}).get("narrative_context", []), indent=2)}
*   Yogas: {json.dumps(profile.get("classical_yogas", []), indent=2)}
*   Weave these into a high-authority narrative about their professional destiny.

# ⏳ 4. Marriage & Relationship Destiny
*   Analysis Logic: {json.dumps(profile.get("event_synthesis", {}).get("marriage", {}).get("narrative_context", []), indent=2)}
*   Give a straight-talking, compassionate assessment of their partnership path.

# 📌 5. The Astrologer's Truth
*   Based on all data, give 3 specific, tactical, and non-generic advice points for {data.name}. 
*   Mention Path A/B if relevant, but as a 'choice' not a 'code'.

DATA CONTEXT:
{json.dumps(profile, indent=2)}
"""

        else:
            prompt = f"""[SYSTEM ROLE: ELITE KP ASTROLOGY ENGINEER]
You are performing a high-precision, tactical Sub-Lord analysis for {data.name}. 
Do NOT use generic fluff. Be technical yet accessible, precision-oriented, and clinical.

CRITICAL RULES:
- DO NOT mention raw 'scores', 'verdicts', 'percentages', or JSON key names.
- USE the 'Narrative Context' provided below as your internal logic notes.
- Your goal is to deliver a 'Tactical Briefing' that feels mathematically perfect but is delivered with human wisdom.

STRUCTURE:

# 🧿 1. KP Cusp & Sub-Lord Architecture
*   Explain the state of the 1st, 7th, and 10th cusps based on their Sub-Lords.
*   Do NOT say "KP Verdict is X." Say "The celestial geometry for your [House] is [Result]."

# 📊 2. The Power Players (Significators)
*   Identify the 2 strongest planets for Career vs Marriage from the significator list.
*   Create a simple summary or table.

# 💼 3. Professional & Financial Destiny
*   Analysis Logic: {json.dumps(profile.get("event_synthesis", {}).get("career", {}).get("narrative_context", []), indent=2)}
*   Deliver a sharp, tactical assessment of their professional rise.

# ⏳ 4. Relationship Dynamics
*   Analysis Logic: {json.dumps(profile.get("event_synthesis", {}).get("marriage", {}).get("narrative_context", []), indent=2)}
*   Explain the partnership promise using Sub-Lord theory (in human terms).

# 📌 5. The Engineer's Final Truth
*   Give 3 blunt, tactical advice points. Use the 'Path A/B' logic as life choices.
*   Tell {data.name} exactly what to focus on right now to trigger the positive results.

DATA CONTEXT:
{json.dumps(profile, indent=2)}
"""


        
        # 3. Call Local Ollama API
        ollama_url = "http://localhost:11434/api/generate"
        payload = {
            "model": "dolphin-3b-uncensored:latest",
            "prompt": prompt,
            "stream": False
        }
        
        req = urllib.request.Request(ollama_url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())
                return {"ai_reading": result.get("response", "No response generated.")}
        except urllib.error.URLError as e:
            raise HTTPException(status_code=502, detail=f"Failed to connect to Local Ollama instance. Is Ollama running? Error: {str(e)}")
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"AI Wrapper Error: {str(e)}")

# Example usage string if run directly
if __name__ == "__main__":
    import uvicorn
    print("Starting Astro-Naught KP Engine API on Port 8000...")
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
