import json
from backend.rules.evaluator import RuleEvaluator
from backend.rules.kp_evaluator import KPEvaluator
from backend.engine.event_synthesizer import EventSynthesizer
from backend.interpretations.text_db import (
    get_planet_in_house_reading, get_lord_in_house_reading,
    get_house_description, get_gana_description, get_varna_description, get_yoni_description,
    get_yoga_description, get_dosha_description
)
from backend.interpretations.kp_text_db import (
    get_cusp_sublord_reading, get_cusp_description,
    get_life_query_info, get_planet_significator_reading
)

class PredictionCompiler:
    def __init__(self, chart_data: dict):
        self.chart = chart_data
        self.evaluator = RuleEvaluator(self.chart)
        self.kp_evaluator = KPEvaluator(self.chart)
        
    def compile_house_report(self, house_number: int) -> dict:
        """
        Gathers all deterministically true facts and interpretations for a specific house.
        """
        house_desc = get_house_description(house_number)
        
        report = {
            "house": house_number,
            "house_name": house_desc["name"],
            "house_domain": house_desc["domain"],
            "house_description": house_desc["description"],
            "occupants": [],
            "lord_analysis": {},
            "aspects": [],
            "conjunctions": []
        }
        
        # 1. Occupants (Planets sitting in the house)
        occupants = self.evaluator.get_planets_in_house(house_number)
        for planet in occupants:
            reading = get_planet_in_house_reading(planet, house_number)
            report["occupants"].append({
                "planet": planet,
                "reading": reading
            })
            
        # 2. Lord Analysis
        lord_info = self.evaluator.get_lord_placement(house_number)
        lord_reading = get_lord_in_house_reading(house_number, lord_info.get("placement_house"))
        report["lord_analysis"] = {
            "lord": lord_info["lord"],
            "placement_house": lord_info.get("placement_house"),
            "placement_sign": lord_info.get("placement_sign"),
            "reading": lord_reading
        }
        
        # 3. Aspects
        aspects = self.evaluator.get_aspects_on_house(house_number)
        report["aspects"] = aspects
        
        return report

    def build_kp_profile(self, current_dasha: dict = None) -> dict:
        """
        Builds a pure KP profile — the primary output for KP mode.
        Includes: chart data, promise analysis, significator table,
        ruling planets, and dasha analysis.
        """
        # 1. KP Chart Data (cusps with sub-lords, planets with star/sub-lords)
        kp_cusps = {}
        for h_num in range(1, 13):
            h_key = h_num if h_num in self.chart.get("kp_cusps", {}) else str(h_num)
            cusp_data = self.chart.get("kp_cusps", {}).get(h_key, {})
            kp_cusps[h_num] = {
                **cusp_data,
                "kp_description": get_cusp_description(h_num)
            }

        # 2. Promise Analysis for key life areas
        promise_analysis = self.kp_evaluator.analyze_all_promises()
        
        # Enrich with KP text descriptions
        enriched_promises = {}
        for h_num, analysis in promise_analysis.items():
            for query_name, query_data in analysis.get("analyses", {}).items():
                is_promised = query_data.get("is_promised", False)
                query_info = get_life_query_info(query_name)
                enriched_promises[query_name] = {
                    **query_data,
                    "title": query_info.get("title", query_name),
                    "detailed_explanation": query_info.get("explanation", ""),
                    "timing_guidance": query_info.get("timing", ""),
                    "cusp_reading": get_cusp_sublord_reading(h_num, is_promised)
                }

        # 3. Significator Table
        significator_table = {}
        for h in range(1, 13):
            sig = self.kp_evaluator.get_significators(h)
            # Add planet-as-significator descriptions
            for planet in sig.get("ordered", [])[:3]:
                if planet:
                    sig.setdefault("planet_descriptions", {})[planet] = \
                        get_planet_significator_reading(planet)
            significator_table[h] = sig

        # 4. Ruling Planets
        ruling_planets = self.kp_evaluator.get_ruling_planets()

        # 5. Dasha Connections (if provided)
        dasha_connections = {}
        if current_dasha:
            for h in range(1, 13):
                dasha_connections[h] = self.kp_evaluator.analyze_dasha_timing(h, current_dasha)

        return {
            "cusps": kp_cusps,
            "promise_analysis": enriched_promises,
            "significators": significator_table,
            "ruling_planets": ruling_planets,
            "dasha_connections": dasha_connections if dasha_connections else None
        }

    def build_full_profile(self):
        """
        Compiles ALL 12 houses to generate a comprehensive life profile.
        Includes both classical (Parashari) AND KP analysis.
        """
        # Build all 12 house reports
        house_reports = {}
        for h in range(1, 13):
            house_reports[f"house_{h}"] = self.compile_house_report(h)
        
        # Moon attributes with personality descriptions
        moon_attrs = self.chart.get("moon_attributes", {})
        gana = moon_attrs.get("gana", "")
        varna = moon_attrs.get("varna", "")
        yoni = moon_attrs.get("yoni", "")
        nadi = moon_attrs.get("nadi", "")
        
        profile = {
            "ascendant": self.chart.get("ascendant", {}),
            "varga_charts": self.chart.get("varga_charts", {}),
            **house_reports,
            "moon_profile": {
                "nakshatra": moon_attrs.get("nakshatra", ""),
                "pada": moon_attrs.get("pada", ""),
                "gana": gana,
                "gana_description": get_gana_description(gana),
                "varna": varna,
                "varna_description": get_varna_description(varna),
                "yoni": yoni,
                "yoni_description": get_yoni_description(yoni),
                "nadi": nadi
            },
            "classical_yogas": self.evaluator.evaluate_yogas()
        }
        
        # Inject Combustion status directly into the occupants list for easier AI reading
        for house_key, data in profile.items():
            if house_key in ["classical_yogas", "moon_profile", "advanced_analysis", "kp_analysis"]:
                continue
            for occ in data.get("occupants", []):
                planet_name = occ["planet"]
                planet_math = self.chart["planets"].get(planet_name, {})
                if planet_math.get("is_combust"):
                    occ["is_combust"] = True
                    occ["combustion_note"] = f"{planet_name} is Combust (Asta) by the Sun. Its natural significations may feel suppressed, frustrated, or internalized."
        
        # ==== ADVANCED JYOTISH ANALYSIS ====
        advanced = self.evaluator.evaluate_all_advanced()

        # Enrich yoga/dosha results with detailed descriptions from text_db
        for category in ["panch_mahapurusha", "dhana_yogas", "raja_yogas",
                         "viparita_raja_yogas", "neecha_bhanga", "sun_yogas",
                         "moon_yogas", "amala_yoga"]:
            for yoga in advanced.get(category, []):
                yoga["detailed_description"] = get_yoga_description(yoga.get("name", ""))

        # Enrich doshas
        for dosha_key in ["manglik_dosha", "kaal_sarp_dosha", "sade_sati"]:
            dosha = advanced.get(dosha_key, {})
            dosha["detailed_description"] = get_dosha_description(dosha.get("name", ""))

        profile["advanced_analysis"] = advanced
        
        # 5. KP Astrology Profile — Full KP analysis
        profile["kp_analysis"] = self.build_kp_profile()
        
        # 6. Event Synthesizer — Fusion of Vedic, KP, and Dasha
        dasha_results = None
        try:
            from backend.engine.dasha import DashaCalculator
            from datetime import datetime
            moon_degree = self.chart.get('planets', {}).get('Moon', {}).get('absolute_degree', 0)
            asc_deg = self.chart.get('ascendant', {}).get('degree', 0)
            # Find nakshatra info for dasha
            from backend.engine.astrology import AstrologyEngine
            astro = AstrologyEngine()
            moon_nak = astro.degree_to_nakshatra(moon_degree)
            
            dob_info = self.chart.get("personal_info", {})
            dob = datetime(
                dob_info.get("year", 2000), 
                dob_info.get("month", 1), 
                dob_info.get("day", 1),
                dob_info.get("hour", 12),
                dob_info.get("minute", 0)
            )
            d_calc = DashaCalculator(moon_nak["nakshatra_index"], moon_degree % (360/27.0), dob)
            dasha_results = d_calc.calculate_dashas()
            profile["dasha_timeline"] = d_calc.get_full_timeline()
        except Exception:
            dasha_results = None

        synthesizer = EventSynthesizer(self.chart, advanced, dasha_results, house_reports)
        profile["event_synthesis"] = synthesizer.synthesize_all()
        
        return profile

# Quick Test
if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from backend.engine.math_engine import VedicMathEngine
    from backend.engine.astrology import AstrologyEngine
    import json
    
    math_res = VedicMathEngine().calculate_positions(1998, 6, 14, 5, 0, 28.6139, 77.2090, "kp")
    chart = AstrologyEngine().generate_chart(math_res, "KP")
    compiler = PredictionCompiler(chart)
    
    full_profile = compiler.build_full_profile()
    
    print("\n[Compiled Deterministic AI Prompt Payload]")
    print(json.dumps(full_profile, indent=2))
