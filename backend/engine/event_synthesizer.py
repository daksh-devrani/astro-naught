class EventSynthesizer:
    """
    The Prediction Intelligence Layer.
    Fuses Classical Vedic scoring, exact KP rules, and Dasha timing into
    human-readable, confidence-weighted life event predictions.
    """

    def __init__(self, chart_data: dict, evaluator_results: dict, dasha_results: dict, house_reports: dict = None):
        from backend.interpretations.text_db import (
            get_planet_in_house_reading, 
            get_lord_in_house_reading
        )
        self.get_planet_in_house_reading = get_planet_in_house_reading
        self.get_lord_in_house_reading = get_lord_in_house_reading
        
        self.chart = chart_data
        self.evaluator = evaluator_results
        self.dasha = dasha_results
        self.house_reports = house_reports or {}
        
        self.kp_houses = self.chart.get('kp_houses', {})
        self.vedic_houses = self.chart.get('houses', {})
        self.kp_significators = self.chart.get('kp_significators', {})
        self.planets = self.chart.get('planets', {})

    def synthesize_all(self):
        """Returns the intelligent synthesis of major life events"""
        return {
            "marriage": self.evaluate_marriage(),
            "career": self.evaluate_career(),
            "wealth": self.evaluate_wealth(),
            "d9_fruit": self.evaluate_d9_fruit()
        }

    def _get_planet_dignity_score(self, planet_name: str) -> int:
        """Returns a numeric score (-3 to +3) for a planet based on dignity."""
        if planet_name not in self.planets:
            return 0
            
        p = self.planets[planet_name]
        score = 0
        if p.get("is_exalted"): score += 2
        elif p.get("is_debilitated"): score -= 2
        
        if p.get("is_vargottama"): score += 1
        if p.get("is_combust"): score -= 2
        
        return score

    def _get_house_occupant_score(self, house_num: int, is_vedic=True) -> int:
        """Scores a house based on the natural benefics/malefics inside it."""
        benefics = ['Jupiter', 'Venus', 'Moon', 'Mercury']
        malefics = ['Saturn', 'Mars', 'Rahu', 'Ketu', 'Sun']
        
        houses = self.vedic_houses if is_vedic else self.kp_houses
        occupants = houses.get(house_num, [])
        
        if isinstance(occupants, dict):
             occupants = list(occupants.keys())
        elif not isinstance(occupants, list):
             occupants = []
             
        score = 0
        for occ in occupants:
            if occ in benefics: score += 1
            if occ in malefics: score -= 1
        return score
        
    def _is_dasha_active(self, target_houses: list) -> bool:
        """Checks if current MD or AD lords signify the target houses"""
        if not self.dasha:
            return False
            
        md_lord = self.dasha.get("current_mahadasha")
        ad_lord = self.dasha.get("current_antardasha")
        
        active = False
        for lord in [md_lord, ad_lord]:
            if not lord: continue
            sig_houses = []
            for h, levels in self.kp_significators.items():
                # Allow both int and str keys for significators
                h_key = h if h in self.kp_significators else str(h)
                if h_key != h: continue # Skip if we already checked it or it's not the right format
                
                levels = self.kp_significators.get(h_key, {})
                if lord in levels.get("L1", []) or lord in levels.get("L2", []) or lord in levels.get("L3", []) or lord in levels.get("L4", []):
                    try:
                        sig_houses.append(int(h))
                    except ValueError:
                        continue
                    
            if any(th in sig_houses for th in target_houses):
                active = True
                break
        return active

    def evaluate_marriage(self):
        """Synthesizes the promise and timing of marriage."""
        vedic_score = self._get_planet_dignity_score("Venus") + self._get_house_occupant_score(7)
        
        kp_promise = "NEUTRAL"
        kp_score = 0.0
        seventh_cusp = self.chart.get('kp_cusps', {}).get(7, {})
        sub_lord = seventh_cusp.get('sub_lord')
        
        if sub_lord:
            sig_houses = []
            for h, levels in self.kp_significators.items():
                if sub_lord in levels.get("L1", []) or sub_lord in levels.get("L2", []):
                    sig_houses.append(h)
            
            if any(h in [2, 7, 11] for h in sig_houses):
                kp_promise = "PROMISED"
                kp_score = 1.0
            elif any(h in [1, 6, 10] for h in sig_houses):
                kp_promise = "DELAYED/DENIED"
                kp_score = -1.0
                
        dasha_active = self._is_dasha_active([2, 7, 11])
        has_conflict = (vedic_score > 1 and kp_score < 0) or (vedic_score < -1 and kp_score > 0)
        
        confidence = 0.5
        if kp_promise == "PROMISED" and vedic_score >= 0: confidence = 0.85
        elif kp_promise == "DELAYED/DENIED" and vedic_score <= 0: confidence = 0.85
        elif has_conflict: confidence = 0.45

        # Narratives
        reasoning = []
        if vedic_score > 0: reasoning.append("Classical Vedic metrics show a favorable environment for partnership.")
        if kp_promise == "PROMISED": reasoning.append("KP Sub-Lord analysis confirms the promise of a long-term union.")
        if dasha_active: reasoning.append("Current time-cycle (Dasha) is actively triggering relationship-oriented houses.")

        narrative_context = []
        ven = self.planets.get("Venus", {})
        if ven:
            narrative_context.append(f"Venus in {ven.get('sign')}: {self.get_planet_in_house_reading('Venus', ven.get('house', 7))}")
        
        # D9 Refinement (Fruit of Promise)
        d9_lagna = self.chart.get("ascendant", {}).get("navamsa_sign_number", 1)
        ven_d9_sign = ven.get("d9_sign_number")
        if ven_d9_sign:
            ven_d9_house = ((ven_d9_sign - d9_lagna) % 12) + 1
            if ven_d9_house in [1, 4, 7, 10, 5, 9]:
                reasoning.append("The Navamsha (D9) shows favorable 'fruit' for partnership, indicating internal satisfaction.")
            elif ven_d9_house in [6, 8, 12]:
                reasoning.append("Navamsha (D9) suggests some friction or 'karmic debt' in the internal experience of partnership.")

        # Pull from enriched house reports if available, else skip
        seven_lord_data = self.house_reports.get("house_7", {}).get("lord_analysis", {})
        if seven_lord_data and isinstance(seven_lord_data, dict):
            narrative_context.append(f"7th Lord Rule: {seven_lord_data.get('reading', 'Stable')}")

        return {
            "topic": "Marriage & Partnership",
            "kp_verdict": kp_promise,
            "vedic_score": vedic_score,
            "dasha_active": dasha_active,
            "confidence_score": confidence,
            "has_conflict": has_conflict,
            "reasoning": reasoning,
            "narrative_context": narrative_context,
            "technical_details": f"Venus Dignity: {self._get_planet_dignity_score('Venus')}. 7H Score: {self._get_house_occupant_score(7)}.",
            "path_a": "Practicing patience and prioritizing emotional maturity will lead to a highly stabilizing long-term partnership.",
            "path_b": "If you push aggressively for a relationship without evaluating compatibility, conflicts may lead to early dissolution."
        }

    def evaluate_career(self):
        """Synthesizes career and professional success."""
        vedic_score = self._get_house_occupant_score(10) + self._get_planet_dignity_score("Sun") + self._get_planet_dignity_score("Saturn")
        
        tenth_cusp = self.chart.get('kp_cusps', {}).get(10, {})
        sub_lord = tenth_cusp.get('sub_lord')
        
        kp_promise = "NEUTRAL"
        if sub_lord:
            sig_houses = []
            for h, levels in self.kp_significators.items():
                if sub_lord in levels.get("L1", []) or sub_lord in levels.get("L2", []):
                    sig_houses.append(h)
            if any(h in [2, 6, 10, 11] for h in sig_houses): kp_promise = "SUCCESS_PROMISED"
            elif any(h in [5, 8, 12] for h in sig_houses): kp_promise = "OBSTACLES_LIKELY"
                
        dasha_active = self._is_dasha_active([2, 6, 10, 11])
        confidence = 0.90 if kp_promise == "SUCCESS_PROMISED" and vedic_score >= 0 else 0.5
        
        reasoning = []
        if vedic_score > 1: reasoning.append("Strong classical indicators for professional rise.")
        if kp_promise == "SUCCESS_PROMISED": reasoning.append("KP Sub-Lord connects to powerful success houses.")
        
        # D9 Career Fruit
        d9_lagna = self.chart.get("ascendant", {}).get("navamsa_sign_number", 1)
        sun = self.planets.get("Sun", {})
        if sun.get("d9_sign_number"):
            sun_d9_house = ((sun.get("d9_sign_number") - d9_lagna) % 12) + 1
            if sun_d9_house in [1, 10, 11]:
                reasoning.append("Navamsha (D9) confirms that professional efforts will bear significant fruit and public recognition.")

        narrative_context = []
        sun = self.planets.get("Sun", {})
        if sun: narrative_context.append(f"Sun in {sun.get('sign')}: {self.get_planet_in_house_reading('Sun', sun.get('house', 10))}")
        sat = self.planets.get("Saturn", {})
        if sat: narrative_context.append(f"Saturn in {sat.get('sign')}: {self.get_planet_in_house_reading('Saturn', sat.get('house', 10))}")

        return {
            "topic": "Career & Success",
            "kp_verdict": kp_promise,
            "vedic_score": vedic_score,
            "dasha_active": dasha_active,
            "confidence_score": confidence,
            "has_conflict": False,
            "reasoning": reasoning,
            "narrative_context": narrative_context,
            "technical_details": f"Sun/Saturn Score: {self._get_planet_dignity_score('Sun') + self._get_planet_dignity_score('Saturn')}.",
            "path_a": "Sticking to structured, disciplined work will yield steady growth.",
            "path_b": "Chasing quick gains will trigger disruptive energy."
        }

    def evaluate_wealth(self):
        vedic_score = self._get_house_occupant_score(2) + self._get_house_occupant_score(11)
        
        return {
            "topic": "Wealth & Assets",
            "kp_verdict": "MODERATE",
            "vedic_score": vedic_score,
            "dasha_active": self._is_dasha_active([2, 11]),
            "confidence_score": 0.6,
            "has_conflict": False,
            "reasoning": ["Steady accumulation suggested by house lords."],
            "narrative_context": [f"Wealth Potential: {self.get_lord_in_house_reading(2, 2)}"],
            "technical_details": f"Wealth Houses Score: {vedic_score}.",
            "path_a": "Conservative investments guarantee security.",
            "path_b": "Speculative risk may lead to erosion."
        }

    def evaluate_d9_fruit(self):
        """Specially analyzes the D9 (Navamsha) for internal strength and fruits."""
        d9_lagna = self.chart.get("ascendant", {}).get("navamsa_sign_number", 1)
        d9_lagna_sign = self.chart.get("ascendant", {}).get("navamsa_sign", "Unknown")
        
        vargottama_planets = [p for p, data in self.planets.items() if data.get("is_vargottama")]
        pushkara_planets = [p for p, data in self.planets.items() if data.get("is_pushkara")]
        
        reasoning = []
        if vargottama_planets:
            reasoning.append(f"Vargottama planets found: {', '.join(vargottama_planets)}. These planets are in harmony with your soul's purpose and give consistent results.")
        
        if pushkara_planets:
            reasoning.append(f"Pushkara Navamsha detected for: {', '.join(pushkara_planets)}. This brings a 'healing' or regenerative quality to their significations.")
            
        # Analyze D9 Lagna Lord fruit
        from backend.rules.constants import SIGN_LORDS
        d9_lagna_lord = SIGN_LORDS.get(d9_lagna)
        d9_lord_data = self.planets.get(d9_lagna_lord, {})
        
        d9_verdict = "STABLE"
        if d9_lagna_lord in vargottama_planets:
            d9_verdict = "EXCEPTIONAL"
            reasoning.append(f"D9 Lagna Lord ({d9_lagna_lord}) is Vargottama, indicating a very strong 'internal foundation' and resilience.")

        # Planet positions in D9
        benefics_in_d9_kendras = []
        for p in ['Jupiter', 'Venus', 'Mercury', 'Moon']:
            p_data = self.planets.get(p, {})
            d9_sign = p_data.get("d9_sign_number")
            if d9_sign:
                d9_house = ((d9_sign - d9_lagna) % 12) + 1
                if d9_house in [1, 4, 7, 10]:
                    benefics_in_d9_kendras.append(p)
        
        if benefics_in_d9_kendras:
            reasoning.append(f"Benefics in D9 Kendras: {', '.join(benefics_in_d9_kendras)}. This promises a life where internal peace and happiness are high.")

        return {
            "topic": "Navamsha & Core Strength",
            "kp_verdict": d9_verdict,
            "vedic_score": len(vargottama_planets) + len(pushkara_planets),
            "dasha_active": False, # Not directly linked to one dasha
            "confidence_score": 0.85,
            "has_conflict": False,
            "reasoning": reasoning,
            "narrative_context": [f"Navamsha Lagna: {d9_lagna_sign}"],
            "technical_details": f"Vargottama: {len(vargottama_planets)}, Pushkara: {len(pushkara_planets)}.",
            "path_a": "Focus on your internal intuition (D9) to guide your external actions (D1).",
            "path_b": "Ignoring the 'soul's' needs and focusing only on material gains may lead to internal burnout."
        }
