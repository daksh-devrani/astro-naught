"""
KP (Krishnamurti Paddhati) Evaluator — Pure KP Analysis Engine.

Replaces the Parashari evaluator.py for KP-mode analysis.
Core axiom: "The Sub-Lord of the cusp decides the result of a house."
"""
from datetime import datetime
import math

from backend.rules.constants import (
    SIGN_LORDS, VIMSHOTTARI_YEARS, VIMSHOTTARI_SEQUENCE,
    KP_HOUSE_GROUPS, RULING_PLANET_DAY_LORDS, SIGN_NAMES,
    NAKSHATRA_LORDS, SPECIAL_ASPECTS
)


class KPEvaluator:
    def __init__(self, chart_data: dict):
        self.chart = chart_data
        self.ascendant_sign_num = self.chart["ascendant"]["sign_number"]

    # ============================================================
    # 1. SIGNIFICATOR SYSTEM (4-Fold)
    # ============================================================

    def get_significators(self, house: int) -> dict:
        """
        Returns the 4-fold significators for a house with strength ordering.
        L1 (strongest): Star Lord of house occupant  — planet connects via star
        L2: House Occupant — planet physically sits there
        L3: Star Lord of house owner — owner connects via star
        L4 (weakest): House Owner — owns the sign on the cusp
        """
        if "kp_significators" in self.chart:
            sig = self.chart["kp_significators"].get(house, self.chart["kp_significators"].get(str(house), {}))
            # Flatten into ordered list (L1 first)
            ordered = []
            for level in ["L1", "L2", "L3", "L4"]:
                for planet in sig.get(level, []):
                    if planet not in ordered:
                        ordered.append(planet)
            return {
                "house": house,
                **sig, # This puts L1, L2, L3, L4 at the top level
                "ordered": ordered,
                "strongest": ordered[0] if ordered else None
            }
        return {"house": house, "levels": {}, "ordered": [], "strongest": None}

    def get_all_significators_for_planet(self, planet: str) -> list:
        """
        Returns list of houses that this planet is a significator of (any level).
        Critical for determining what a dasha lord will activate.
        """
        houses = []
        sigs = self.chart.get("kp_significators", {})
        for h_num in range(1, 13):
            h_key = h_num if h_num in sigs else str(h_num)
            if h_key not in sigs:
                continue
            for level in ["L1", "L2", "L3", "L4"]:
                if planet in sigs[h_key].get(level, []):
                    houses.append(h_num)
                    break
        return houses

    # ============================================================
    # 2. CUSP PROMISE ANALYSIS (Core KP Prediction)
    # ============================================================

    def analyze_cusp_promise(self, house: int) -> dict:
        """
        The fundamental KP prediction method.
        "Is the event promised?" = Is the sub-lord of the cusp a significator
        of the favorable houses for that life matter?

        Example: For marriage (house 7), check if the sub-lord of the 7th cusp
        is a significator of houses 2, 7, 11.
        """
        cusp_data = self.chart.get("kp_cusps", {}).get(house, self.chart.get("kp_cusps", {}).get(str(house), {}))
        if not cusp_data:
            return {"house": house, "promised": False, "reason": "No cusp data available."}

        sub_lord = cusp_data.get("sub_lord")
        if not sub_lord:
            return {"house": house, "promised": False, "reason": "No sub-lord found."}

        # Get which houses this sub-lord signifies
        sub_lord_houses = self.get_all_significators_for_planet(sub_lord)

        result = {
            "house": house,
            "cusp_sub_lord": sub_lord,
            "sub_lord_signifies_houses": sub_lord_houses,
            "analyses": {}
        }

        # Check against each life query that involves this house
        for query, group in KP_HOUSE_GROUPS.items():
            # Determine the primary cusp for this query
            primary_cusp_map = {
                "marriage": 7, "profession": 10, "wealth": 2, "children": 5,
                "education": 9, "foreign_travel": 12, "foreign_settlement": 12,
                "health": 1, "longevity": 8, "property": 4, "litigation": 6,
                "vehicle": 4, "spiritual_progress": 9, "business_partnership": 7,
                "government_job": 10
            }
            primary_cusp = primary_cusp_map.get(query)
            if primary_cusp != house:
                continue

            favorable = group["favorable"]
            unfavorable = group["unfavorable"]

            favorable_count = len([h for h in sub_lord_houses if h in favorable])
            unfavorable_count = len([h for h in sub_lord_houses if h in unfavorable])

            is_promised = favorable_count > unfavorable_count
            strength = "strong" if favorable_count >= 2 else "moderate" if favorable_count == 1 else "weak"

            result["analyses"][query] = {
                "query": query,
                "is_promised": is_promised,
                "strength": strength if is_promised else "denied",
                "favorable_connections": [h for h in sub_lord_houses if h in favorable],
                "unfavorable_connections": [h for h in sub_lord_houses if h in unfavorable],
                "description": group["description"],
                "verdict": f"{query.replace('_', ' ').title()} is {'PROMISED' if is_promised else 'NOT PROMISED'}. "
                          f"Sub-lord {sub_lord} signifies favorable houses {[h for h in sub_lord_houses if h in favorable]} "
                          f"and unfavorable houses {[h for h in sub_lord_houses if h in unfavorable]}."
            }

        return result

    def analyze_all_promises(self) -> dict:
        """Analyze cusp promise for all 12 houses."""
        promises = {}
        for h in range(1, 13):
            analysis = self.analyze_cusp_promise(h)
            if analysis.get("analyses"):
                promises[h] = analysis
        return promises

    # ============================================================
    # 3. RULING PLANETS
    # ============================================================

    def get_ruling_planets(self, query_datetime: datetime = None,
                           lat: float = 0.0, lon: float = 0.0) -> dict:
        """
        Calculates the 5 Ruling Planets at the moment of judgment.
        KP uses these to filter significators for timing precision.

        The 5 components:
        1. Day Lord — planet ruling the day of the week
        2. Moon Sign Lord — planet ruling the sign Moon is in at query time
        3. Moon Star Lord — planet ruling the nakshatra Moon is in at query time
        4. Lagna Sign Lord — planet ruling the ascendant sign at query time
        5. Lagna Star Lord — planet ruling the ascendant nakshatra at query time

        For natal chart analysis, we use the birth chart's Moon and Lagna.
        """
        if query_datetime is None:
            query_datetime = datetime.now()

        # 1. Day Lord
        day_of_week = query_datetime.weekday()  # Monday=0, Sunday=6
        day_lord = RULING_PLANET_DAY_LORDS[day_of_week]

        # 2-3. Moon Sign Lord and Moon Star Lord (from natal chart)
        moon_data = self.chart["planets"].get("Moon", {})
        moon_sign_num = moon_data.get("sign_number", 1)
        moon_sign_lord = SIGN_LORDS.get(moon_sign_num, "Unknown")
        moon_star_lord = moon_data.get("kp_star_lord", "Unknown")

        # 4-5. Lagna Sign Lord and Lagna Star Lord (from natal chart)
        asc_data = self.chart.get("ascendant", {})
        lagna_sign_num = asc_data.get("sign_number", 1)
        lagna_sign_lord = SIGN_LORDS.get(lagna_sign_num, "Unknown")
        lagna_star_lord = asc_data.get("kp_star_lord", "Unknown")

        ruling_planets = [day_lord, moon_sign_lord, moon_star_lord,
                         lagna_sign_lord, lagna_star_lord]

        # Unique planets that appear as ruling planets
        unique_rps = list(dict.fromkeys(ruling_planets))  # preserves order, removes dupes

        return {
            "day_lord": day_lord,
            "moon_sign_lord": moon_sign_lord,
            "moon_star_lord": moon_star_lord,
            "lagna_sign_lord": lagna_sign_lord,
            "lagna_star_lord": lagna_star_lord,
            "all_ruling_planets": ruling_planets,
            "unique_ruling_planets": unique_rps,
            "query_datetime": query_datetime.isoformat()
        }

    # ============================================================
    # 4. SIGNIFICATOR FILTERING BY RULING PLANETS
    # ============================================================

    def filter_significators_by_ruling_planets(self, house: int,
                                               query_datetime: datetime = None) -> dict:
        """
        Cross-references significators of a house with ruling planets.
        Planets that are BOTH significators AND ruling planets are the ones
        most likely to deliver results in their dasha/bhukti.
        """
        sigs = self.get_significators(house)
        rps = self.get_ruling_planets(query_datetime)

        filtered = [p for p in sigs["ordered"] if p in rps["unique_ruling_planets"]]

        return {
            "house": house,
            "all_significators": sigs["ordered"],
            "ruling_planets": rps["unique_ruling_planets"],
            "filtered_significators": filtered,
            "timing_planets": filtered,  # These planets' dasha periods will activate the house
            "description": f"House {house}: Significators filtered by ruling planets → {filtered or 'None found'}. "
                          f"These planets' dasha periods are most likely to trigger events related to House {house}."
        }

    # ============================================================
    # 5. DASHA TIMING ANALYSIS
    # ============================================================

    def analyze_dasha_timing(self, house: int, current_dasha: dict = None) -> dict:
        """
        Checks if the current Dasha/Bhukti lords are significators
        of the given house. If yes, the house matters are likely active.
        """
        sigs = self.get_significators(house)
        sig_planets = sigs["ordered"]

        result = {
            "house": house,
            "significators": sig_planets,
            "dasha_analysis": None
        }

        if current_dasha:
            md_lord = current_dasha.get("current_mahadasha")
            ad_lord = current_dasha.get("current_antardasha")

            md_is_sig = md_lord in sig_planets if md_lord else False
            ad_is_sig = ad_lord in sig_planets if ad_lord else False

            activation_level = "none"
            if md_is_sig and ad_is_sig:
                activation_level = "strong"
            elif md_is_sig or ad_is_sig:
                activation_level = "moderate"

            result["dasha_analysis"] = {
                "mahadasha_lord": md_lord,
                "antardasha_lord": ad_lord,
                "md_is_significator": md_is_sig,
                "ad_is_significator": ad_is_sig,
                "activation_level": activation_level,
                "description": f"House {house} activation: {activation_level}. "
                              f"MD lord {md_lord} {'IS' if md_is_sig else 'is NOT'} a significator. "
                              f"AD lord {ad_lord} {'IS' if ad_is_sig else 'is NOT'} a significator."
            }

        return result

    # ============================================================
    # 6. PLANET FRUITFULNESS
    # ============================================================

    def is_planet_fruitful(self, planet: str, house: int) -> dict:
        """
        Determines if a planet will give positive or negative results
        for a specific house, based on its sub-lord's significations.

        In KP: A planet gives the result of its STAR LORD,
        modified by its SUB LORD. If the sub-lord signifies
        favorable houses → positive. Unfavorable → negative.
        """
        p_data = self.chart["planets"].get(planet, {})
        sub_lord = p_data.get("kp_sub_lord")

        if not sub_lord:
            return {"planet": planet, "house": house, "fruitful": None, "reason": "No sub-lord data."}

        sub_lord_houses = self.get_all_significators_for_planet(sub_lord)

        # Check fruitfulness against ALL relevant life queries for this house
        is_fruitful = None
        reasons = []

        for query, group in KP_HOUSE_GROUPS.items():
            primary_map = {
                "marriage": 7, "profession": 10, "wealth": 2, "children": 5,
                "education": 9, "foreign_travel": 12, "foreign_settlement": 12,
                "health": 1, "longevity": 8, "property": 4, "litigation": 6,
                "vehicle": 4, "spiritual_progress": 9, "business_partnership": 7,
                "government_job": 10
            }
            if primary_map.get(query) != house:
                continue

            fav = [h for h in sub_lord_houses if h in group["favorable"]]
            unfav = [h for h in sub_lord_houses if h in group["unfavorable"]]

            if len(fav) > len(unfav):
                is_fruitful = True
                reasons.append(f"{planet}'s sub-lord {sub_lord} favors {query}: connects to houses {fav}.")
            elif len(unfav) > len(fav):
                is_fruitful = False
                reasons.append(f"{planet}'s sub-lord {sub_lord} denies {query}: connects to houses {unfav}.")

        if is_fruitful is None:
            # Generic check — is sub-lord a significator of the house itself?
            is_fruitful = house in sub_lord_houses
            if is_fruitful:
                reasons.append(f"{planet}'s sub-lord {sub_lord} directly signifies house {house}.")
            else:
                reasons.append(f"{planet}'s sub-lord {sub_lord} does not directly signify house {house}.")

        return {
            "planet": planet,
            "house": house,
            "sub_lord": sub_lord,
            "sub_lord_signifies": sub_lord_houses,
            "fruitful": is_fruitful,
            "reasons": reasons
        }

    # ============================================================
    # 7. COMPREHENSIVE HOUSE PROMISE
    # ============================================================

    def get_house_promise(self, house: int) -> dict:
        """
        Comprehensive "will this matter manifest?" analysis combining:
        1. Cusp sub-lord promise
        2. Significator strength
        3. Planet fruitfulness for key significators
        """
        promise = self.analyze_cusp_promise(house)
        sigs = self.get_significators(house)

        # Check fruitfulness of each significator
        fruitfulness_results = []
        for planet in sigs["ordered"][:5]:  # Top 5 significators
            fr = self.is_planet_fruitful(planet, house)
            fruitfulness_results.append(fr)

        fruitful_count = sum(1 for fr in fruitfulness_results if fr.get("fruitful"))
        denied_count = sum(1 for fr in fruitfulness_results if fr.get("fruitful") is False)

        overall_promise = "strong" if fruitful_count >= 3 else \
                         "moderate" if fruitful_count >= 1 else "weak"

        return {
            "house": house,
            "cusp_analysis": promise,
            "significators": sigs,
            "fruitfulness": fruitfulness_results,
            "fruitful_count": fruitful_count,
            "denied_count": denied_count,
            "overall_promise": overall_promise,
            "summary": f"House {house} overall promise: {overall_promise}. "
                      f"{fruitful_count} fruitful significators, {denied_count} denied."
        }

    # ============================================================
    # 8. FULL KP PROFILE
    # ============================================================

    def build_full_kp_analysis(self, current_dasha: dict = None) -> dict:
        """
        Generates the complete KP analysis profile.
        """
        # Promise analysis for all major life areas
        all_promises = self.analyze_all_promises()

        # Significator table for all 12 houses
        significator_table = {}
        for h in range(1, 13):
            significator_table[h] = self.get_significators(h)

        # Ruling planets at current moment
        ruling = self.get_ruling_planets()

        # Dasha-significator connections if dasha data available
        dasha_analysis = {}
        if current_dasha:
            for h in range(1, 13):
                dasha_analysis[h] = self.analyze_dasha_timing(h, current_dasha)

        # Timing filter for key houses
        timing_analysis = {}
        for h in [1, 2, 5, 7, 10, 11]:
            timing_analysis[h] = self.filter_significators_by_ruling_planets(h)

        return {
            "promise_analysis": all_promises,
            "significator_table": significator_table,
            "ruling_planets": ruling,
            "dasha_connections": dasha_analysis if dasha_analysis else None,
            "timing_analysis": timing_analysis
        }


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
    evaluator = KPEvaluator(chart)

    print("=== KP SIGNIFICATORS (House 7 — Marriage) ===")
    print(json.dumps(evaluator.get_significators(7), indent=2))

    print("\n=== CUSP PROMISE (House 7) ===")
    print(json.dumps(evaluator.analyze_cusp_promise(7), indent=2))

    print("\n=== RULING PLANETS ===")
    print(json.dumps(evaluator.get_ruling_planets(), indent=2))

    print("\n=== HOUSE PROMISE (House 10 — Career) ===")
    print(json.dumps(evaluator.get_house_promise(10), indent=2))
