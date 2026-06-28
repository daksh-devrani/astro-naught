class MatchMaker:
    """
    Deterministic Compatibility Engine (Synastry).
    Compares two astrological charts to calculate relationship synergies,
    strengths, and potential challenges.
    """
    def __init__(self, chart_a: dict, chart_b: dict):
        self.chart_a = chart_a
        self.chart_b = chart_b

    def _get_angular_distance(self, deg1: float, deg2: float) -> float:
        """Returns the shortest angular distance between two degrees."""
        diff = abs(deg1 - deg2)
        return min(diff, 360 - diff)

    def _check_aspect(self, deg1: float, deg2: float, aspect: int, orb: float = 8.0) -> bool:
        """Checks if two degrees form a specific aspect within an orb."""
        dist = self._get_angular_distance(deg1, deg2)
        return abs(dist - aspect) <= orb

    def _calculate_element(self, sign_number: int) -> str:
        """Returns the element of a sign (1=Aries, etc.)."""
        # 1,5,9=Fire; 2,6,10=Earth; 3,7,11=Air; 4,8,12=Water
        if sign_number in [1, 5, 9]: return "Fire"
        if sign_number in [2, 6, 10]: return "Earth"
        if sign_number in [3, 7, 11]: return "Air"
        if sign_number in [4, 8, 12]: return "Water"
        return "Unknown"

    def _elements_compatible(self, el1: str, el2: str) -> bool:
        """Checks if two elements are naturally compatible."""
        if el1 == el2: return True
        if el1 in ["Fire", "Air"] and el2 in ["Fire", "Air"]: return True
        if el1 in ["Earth", "Water"] and el2 in ["Earth", "Water"]: return True
        return False

    def evaluate_emotional(self) -> dict:
        """Moon to Moon and Moon to Venus compatibility."""
        score = 50
        strengths = []
        challenges = []

        moon_a = self.chart_a.get("planets", {}).get("Moon", {})
        moon_b = self.chart_b.get("planets", {}).get("Moon", {})
        venus_b = self.chart_b.get("planets", {}).get("Venus", {})

        if moon_a and moon_b:
            el_a = self._calculate_element(moon_a.get("sign_number", 1))
            el_b = self._calculate_element(moon_b.get("sign_number", 1))

            if self._elements_compatible(el_a, el_b):
                score += 20
                strengths.append("Emotionally synced: Both share compatible elemental needs (Earth/Water or Fire/Air).")
            else:
                score -= 10
                challenges.append("Emotional mismatch: Core emotional needs may require conscious translation.")

            # Moon-Moon Trine/Conjunction
            if self._check_aspect(moon_a.get("absolute_degree", 0), moon_b.get("absolute_degree", 0), 120):
                score += 15
                strengths.append("Trine Moons: Deep, instinctive understanding of each other's feelings.")
            if self._check_aspect(moon_a.get("absolute_degree", 0), moon_b.get("absolute_degree", 0), 0):
                score += 15
                strengths.append("Conjunction Moons: Soulmate-level emotional resonance.")
            if self._check_aspect(moon_a.get("absolute_degree", 0), moon_b.get("absolute_degree", 0), 90):
                score -= 15
                challenges.append("Square Moons: Emotional friction; feelings can get easily hurt.")

        if moon_a and venus_b:
            if self._check_aspect(moon_a.get("absolute_degree", 0), venus_b.get("absolute_degree", 0), 120) or \
               self._check_aspect(moon_a.get("absolute_degree", 0), venus_b.get("absolute_degree", 0), 0):
                score += 15
                strengths.append("Moon-Venus Harmony: Natural affection and romantic tenderness.")

        return {"score": min(max(score, 0), 100), "strengths": strengths, "challenges": challenges}

    def evaluate_communication(self) -> dict:
        """Mercury to Mercury compatibility."""
        score = 50
        strengths = []
        challenges = []

        merc_a = self.chart_a.get("planets", {}).get("Mercury", {})
        merc_b = self.chart_b.get("planets", {}).get("Mercury", {})

        if merc_a and merc_b:
            el_a = self._calculate_element(merc_a.get("sign_number", 1))
            el_b = self._calculate_element(merc_b.get("sign_number", 1))

            if self._elements_compatible(el_a, el_b):
                score += 25
                strengths.append("Smooth Communication: You both process information and converse in similar ways.")
            else:
                score -= 10
                challenges.append("Communication Styles: One may be overly logical while the other is highly intuitive.")

            # Hard aspects
            if self._check_aspect(merc_a.get("absolute_degree", 0), merc_b.get("absolute_degree", 0), 90) or \
               self._check_aspect(merc_a.get("absolute_degree", 0), merc_b.get("absolute_degree", 0), 180):
                score -= 20
                challenges.append("Mercury Tension: Frequent misunderstandings or debates that escalate quickly.")
            
            # Soft aspects
            if self._check_aspect(merc_a.get("absolute_degree", 0), merc_b.get("absolute_degree", 0), 120) or \
               self._check_aspect(merc_a.get("absolute_degree", 0), merc_b.get("absolute_degree", 0), 60):
                score += 25
                strengths.append("Mental Synergy: Excellent brainstorming and effortless conversation.")

        return {"score": min(max(score, 0), 100), "strengths": strengths, "challenges": challenges}

    def evaluate_physical(self) -> dict:
        """Mars and Venus interplay."""
        score = 50
        strengths = []
        challenges = []

        mars_a = self.chart_a.get("planets", {}).get("Mars", {})
        venus_b = self.chart_b.get("planets", {}).get("Venus", {})
        venus_a = self.chart_a.get("planets", {}).get("Venus", {})
        mars_b = self.chart_b.get("planets", {}).get("Mars", {})

        if mars_a and venus_b:
            dist = self._get_angular_distance(mars_a.get("absolute_degree", 0), venus_b.get("absolute_degree", 0))
            if dist <= 8 or abs(dist - 120) <= 8 or abs(dist - 180) <= 8:
                score += 25
                strengths.append("High Magnetic Attraction (A's Mars to B's Venus).")

        if venus_a and mars_b:
            dist = self._get_angular_distance(venus_a.get("absolute_degree", 0), mars_b.get("absolute_degree", 0))
            if dist <= 8 or abs(dist - 120) <= 8 or abs(dist - 180) <= 8:
                score += 25
                strengths.append("High Magnetic Attraction (B's Mars to A's Venus).")

        # Manglik Check (Simple proxy)
        mars_a_house = mars_a.get("house", 0)
        mars_b_house = mars_b.get("house", 0)
        a_is_manglik = mars_a_house in [1, 4, 7, 8, 12]
        b_is_manglik = mars_b_house in [1, 4, 7, 8, 12]

        if a_is_manglik != b_is_manglik:
            score -= 15
            challenges.append("Manglik Mismatch: One partner has significantly higher aggressive/protective drive (Kuja Dosha).")
        elif a_is_manglik and b_is_manglik:
            score += 10
            strengths.append("Manglik Cancelled: Both possess high martial energy, canceling out potential friction.")

        return {"score": min(max(score, 0), 100), "strengths": strengths, "challenges": challenges}

    def evaluate_long_term(self) -> dict:
        """Saturn and 7th House synergies."""
        score = 50
        strengths = []
        challenges = []

        sat_a = self.chart_a.get("planets", {}).get("Saturn", {})
        moon_b = self.chart_b.get("planets", {}).get("Moon", {})
        venus_b = self.chart_b.get("planets", {}).get("Venus", {})

        sat_b = self.chart_b.get("planets", {}).get("Saturn", {})
        moon_a = self.chart_a.get("planets", {}).get("Moon", {})

        # Saturn stabilizing Moon/Venus
        if sat_a and moon_b:
            if self._check_aspect(sat_a.get("absolute_degree", 0), moon_b.get("absolute_degree", 0), 120) or \
               self._check_aspect(sat_a.get("absolute_degree", 0), moon_b.get("absolute_degree", 0), 60):
                score += 20
                strengths.append("Saturn-Moon Harmony: Deep sense of duty, loyalty, and long-term security.")
            if self._check_aspect(sat_a.get("absolute_degree", 0), moon_b.get("absolute_degree", 0), 90):
                score -= 15
                challenges.append("Saturn-Moon Friction: Emotional coldness or feeling restricted by the relationship.")

        if sat_b and moon_a:
            if self._check_aspect(sat_b.get("absolute_degree", 0), moon_a.get("absolute_degree", 0), 120):
                score += 20
                if "Saturn-Moon Harmony: Deep sense of duty, loyalty, and long-term security." not in strengths:
                    strengths.append("Saturn-Moon Harmony: Deep sense of duty, loyalty, and long-term security.")
                    
        # KP 7th Cusp Alignment (Checking if SubLords match or signify matching houses)
        h7_a = self.chart_a.get("kp_cusps", {}).get("7", {}).get("sub_lord")
        h7_b = self.chart_b.get("kp_cusps", {}).get("7", {}).get("sub_lord")
        if h7_a and h7_b and h7_a == h7_b:
            score += 20
            strengths.append(f"KP Partnership Alignment: Both share {h7_a} as the 7th Cusp Sub-Lord, indicating shared relationship destiny.")

        return {"score": min(max(score, 0), 100), "strengths": strengths, "challenges": challenges}
        
    def evaluate_family_harmony(self) -> dict:
        """Jupiter and 2nd/4th House synergies."""
        score = 60
        strengths = []
        challenges = []

        jup_a = self.chart_a.get("planets", {}).get("Jupiter", {})
        jup_b = self.chart_b.get("planets", {}).get("Jupiter", {})

        if jup_a and jup_b:
            el_a = self._calculate_element(jup_a.get("sign_number", 1))
            el_b = self._calculate_element(jup_b.get("sign_number", 1))

            if self._elements_compatible(el_a, el_b):
                score += 20
                strengths.append("Shared Values: Highly compatible views on family, ethics, and growth.")
            
            if self._check_aspect(jup_a.get("absolute_degree", 0), jup_b.get("absolute_degree", 0), 90) or \
               self._check_aspect(jup_a.get("absolute_degree", 0), jup_b.get("absolute_degree", 0), 180):
                score -= 20
                challenges.append("Value Clash: Disagreements over family expansion, religion, or core beliefs.")

        return {"score": min(max(score, 0), 100), "strengths": strengths, "challenges": challenges}

    def run_match(self) -> dict:
        """Compiles the full matching profile."""
        emotional = self.evaluate_emotional()
        communication = self.evaluate_communication()
        physical = self.evaluate_physical()
        long_term = self.evaluate_long_term()
        family = self.evaluate_family_harmony()

        overall_score = (
            emotional["score"] * 0.30 +
            communication["score"] * 0.20 +
            long_term["score"] * 0.25 +
            physical["score"] * 0.15 +
            family["score"] * 0.10
        )

        all_strengths = emotional["strengths"] + communication["strengths"] + physical["strengths"] + long_term["strengths"] + family["strengths"]
        all_challenges = emotional["challenges"] + communication["challenges"] + physical["challenges"] + long_term["challenges"] + family["challenges"]

        # Sort based on length/importance or just take top 4
        all_strengths = list(set(all_strengths))
        all_challenges = list(set(all_challenges))

        return {
            "overall_score": round(overall_score),
            "categories": {
                "emotional": emotional["score"],
                "communication": communication["score"],
                "physical": physical["score"],
                "long_term": long_term["score"],
                "family": family["score"]
            },
            "top_strengths": all_strengths[:5],
            "potential_challenges": all_challenges[:5]
        }
