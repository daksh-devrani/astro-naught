import math

class AstrologyEngine:
    def __init__(self):
        # 12 Zodiac Signs, each 30 degrees long
        self.ZODIAC_SIGNS = [
            "Aries", "Taurus", "Gemini", "Cancer",
            "Leo", "Virgo", "Libra", "Scorpio",
            "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        
        # 27 Nakshatras, each 13 degrees 20 minutes (13.3333... degrees) long
        self.NAKSHATRAS = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
            "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]

    def degree_to_zodiac(self, degree: float):
        """
        Converts a 0-360 degree to its Zodiac Sign and the degree within that sign.
        """
        from backend.rules.constants import SIGN_LORDS
        # Ensure degree is strictly within 0 - 359.999
        normalized_deg = degree % 360
        
        # Each sign is 30 degrees. 
        # Example: 45 degrees // 30 = 1 -> Taurus.
        sign_index = int(normalized_deg // 30)
        sign_number = sign_index + 1
        sign_name = self.ZODIAC_SIGNS[sign_index]
        
        degree_in_sign = normalized_deg % 30
        
        return {
            "sign": sign_name,
            "sign_number": sign_number,  # 1-indexed (Aries=1, Pisces=12)
            "degree": degree_in_sign,
            "lord": SIGN_LORDS[sign_number]
        }

    def degree_to_nakshatra(self, degree: float):
        """
        Converts a 0-360 degree to its Nakshatra and Pada (quarter).
        """
        normalized_deg = degree % 360
        
        # Each Nakshatra is exactly 13.333333 degrees (13 degrees 20 minutes = 13 + 1/3 degrees)
        # 360 / 27 = 13.333333
        nakshatra_length = 360.0 / 27.0
        
        nakshatra_index = int(normalized_deg // nakshatra_length)
        nakshatra_name = self.NAKSHATRAS[nakshatra_index]
        
        degree_in_nakshatra = normalized_deg % nakshatra_length
        
        # Each Nakshatra has 4 Padas. Length of one pada = nakshatra_length / 4 = 3.33333 degrees
        pada_length = nakshatra_length / 4.0
        pada_number = int(degree_in_nakshatra // pada_length) + 1  # 1 to 4
        
        return {
            "nakshatra": nakshatra_name,
            "nakshatra_index": nakshatra_index,
            "pada": pada_number
        }

    def calculate_navamsa(self, degree: float, d1_sign_name: str = None):
        """
        Calculates the D9 (Navamsa) longitudinal position.
        The continuous formula is (Absolute_Degree * 9) % 360.
        """
        d9_degree = (degree * 9.0) % 360.0
        navamsa_info = self.degree_to_zodiac(d9_degree)
        
        # Determine the Navamsa Number (1-9) within the D1 sign
        degree_in_sign = degree % 30.0
        navamsa_number = int(degree_in_sign // (30.0 / 9.0)) + 1
        
        # Evaluate Advanced features
        is_vargottama = (navamsa_info["sign"] == d1_sign_name) if d1_sign_name else False
        is_pushkara = False
        
        if d1_sign_name:
            from backend.rules.constants import PUSHKARA_NAVAMSA_INDICES, SIGN_ELEMENTS
            element = SIGN_ELEMENTS.get(d1_sign_name)
            if element and navamsa_number in PUSHKARA_NAVAMSA_INDICES.get(element, []):
                is_pushkara = True
                
        navamsa_info["navamsa_number"] = navamsa_number
        navamsa_info["is_vargottama"] = is_vargottama
        navamsa_info["is_pushkara"] = is_pushkara
        
        return navamsa_info

    def calculate_varga(self, degree: float, division: int) -> dict:
        """
        Calculates the sign-level information for any divisional chart (Varga).
        Standard divisions like D12, D60 use a cyclic projection: (Degree * N) % 360.
        Special divisions like D2 (Hora) use sign-parity based logic.
        """
        normalized_deg = degree % 360.0
        sign_number = int(normalized_deg // 30) + 1
        degree_in_sign = normalized_deg % 30.0
        
        if division == 1:
            return self.degree_to_zodiac(degree)
            
        if division == 2: # Parashari Hora
            # Odd signs: 0-15 Sun (Leo), 15-30 Moon (Cancer)
            # Even signs: 0-15 Moon (Cancer), 15-30 Sun (Leo)
            is_odd = sign_number % 2 != 0
            if degree_in_sign < 15.0:
                v_sign_num = 5 if is_odd else 4
            else:
                v_sign_num = 4 if is_odd else 5
            
            # Hora degree doesn't have a standard physical meaning in signs like D9, 
            # so we just return the sign-level info.
            from backend.rules.constants import SIGN_NAMES
            return {
                "sign": SIGN_NAMES[v_sign_num],
                "sign_number": v_sign_num,
                "degree": degree_in_sign * 2 # Normalized to 30 for consistency
            }

        # General cyclic formula for D9, D12, D60 etc.
        # This matches the method of multiplying absolute longitude and stripping full circles.
        v_degree = (degree * float(division)) % 360.0
        return self.degree_to_zodiac(v_degree)
        
    def calculate_kp_number(self, degree: float) -> int:
        """
        Maps any degree (0-360) to its KP Number (1-249).
        The zodiac is divided into 249 sub-divisions (27 nakshatras × ~9.222 subs each).
        Each sub has a unique number based on cumulative Vimshottari proportional division.
        """
        from backend.rules.constants import VIMSHOTTARI_YEARS, VIMSHOTTARI_SEQUENCE
        
        normalized_deg = degree % 360.0
        nakshatra_length = 360.0 / 27.0  # 13.3333 degrees
        nakshatra_index = int(normalized_deg // nakshatra_length)
        
        # Star lord from Vimshottari sequence
        lord_index = nakshatra_index % 9
        
        # Degree into this nakshatra
        nak_start = nakshatra_index * nakshatra_length
        deg_into_nak = normalized_deg - nak_start
        minutes_into_nak = deg_into_nak * 60.0
        total_nak_minutes = nakshatra_length * 60.0
        
        # Find which sub we're in
        start_idx = lord_index
        current_boundary = 0.0
        sub_index_in_nak = 0
        
        for i in range(9):
            idx = (start_idx + i) % 9
            planet = VIMSHOTTARI_SEQUENCE[idx]
            years = VIMSHOTTARI_YEARS[planet]
            span = (years / 120.0) * total_nak_minutes
            
            if current_boundary <= minutes_into_nak < (current_boundary + span - 1e-9):
                sub_index_in_nak = i
                break
            current_boundary += span
            sub_index_in_nak = i  # fallback to last
        
        # KP number = (nakshatra_index * 9) + sub_index_in_nak + 1
        # But the actual count of subs per nakshatra is always 9 (one for each Vimshottari planet)
        kp_number = (nakshatra_index * 9) + sub_index_in_nak + 1
        
        # Clamp to 1-249 range (27 * 9 = 243, but last few map to 249 due to rounding)
        return min(kp_number, 249)

    def calculate_sublords(self, degree: float) -> dict:
        """
        Calculates the KP Star Lord, Sub Lord, and Sub-Sub Lord for a given absolute degree (0-360).
        Each Nakshatra spans 13°20' (800 minutes). The span is divided proportionally
        according to the Vimshottari Mahadasha sequence (total 120 years).
        """
        from backend.rules.constants import VIMSHOTTARI_YEARS, VIMSHOTTARI_SEQUENCE
        
        # In Vedic astrology, the 27 Nakshatras are ruled by the 9 planets in the exact Vimshottari sequence repeated 3 times.
        # 1st group: Ashwini (Ketu) to Aslesha (Mercury)
        # 2nd group: Magha (Ketu) to Jyeshtha (Mercury)
        # 3rd group: Mula (Ketu) to Revati (Mercury)
        
        # Calculate exactly which of the 27 nakshatras this degree falls into (0-26 index)
        nakshatra_index_absolute = int(degree // (360.0 / 27.0))
        
        # The lord is simply the Vimshottari sequence index (0-8)
        lord_index = nakshatra_index_absolute % 9
        star_lord = VIMSHOTTARI_SEQUENCE[lord_index]

        # Exact minutes into this specific Nakshatra
        # Nakshatra starts at: nakshatra_index * (800/60) degrees
        import math
        
        # Calculate the start degree of the current nakshatra
        # Each nakshatra is 360/27 degrees long
        nakshatra_length_deg = 360.0 / 27.0
        nakshatra_start_degree = nakshatra_index_absolute * nakshatra_length_deg
        
        degrees_into_nakshatra = degree - nakshatra_start_degree
        if degrees_into_nakshatra < 0: # Handle wrap around for 0-360 range
            degrees_into_nakshatra += 360
        
        # If the degree is exactly on the boundary of a nakshatra, it might be 0 or very close to 0
        # Ensure it's within the current nakshatra's span
        if degrees_into_nakshatra >= nakshatra_length_deg:
            degrees_into_nakshatra -= nakshatra_length_deg # Should not happen with % 360 and correct start_degree

        minutes_into_nakshatra = degrees_into_nakshatra * 60.0
        
        # 2. Find Sub Lord
        # The sequence starts with the Star Lord itself
        start_idx = VIMSHOTTARI_SEQUENCE.index(star_lord)
        
        current_minute_boundary = 0.0
        sub_lord = None
        sub_lord_idx = start_idx
        
        # Total span of a nakshatra in minutes (13 degrees 20 minutes = 800 minutes)
        total_nakshatra_span_minutes = nakshatra_length_deg * 60.0
        
        for i in range(9):
            idx = (start_idx + i) % 9
            planet = VIMSHOTTARI_SEQUENCE[idx]
            years = VIMSHOTTARI_YEARS[planet]
            
            # Sub-lord span = (Years / 120) * total_nakshatra_span_minutes
            span_minutes = (years / 120.0) * total_nakshatra_span_minutes
            
            # Use a small epsilon for floating point comparison to avoid issues at boundaries
            epsilon = 1e-9
            if current_minute_boundary <= minutes_into_nakshatra < (current_minute_boundary + span_minutes - epsilon):
                sub_lord = planet
                sub_lord_idx = idx
                # How many minutes into THIS Sub-lord's span are we?
                minutes_into_sub = minutes_into_nakshatra - current_minute_boundary
                break
            
            current_minute_boundary += span_minutes
        
        # Fallback for the last segment if floating point precision causes it to miss
        if sub_lord is None:
            sub_lord = VIMSHOTTARI_SEQUENCE[(start_idx + 8) % 9]
            sub_lord_idx = (start_idx + 8) % 9
            minutes_into_sub = minutes_into_nakshatra - (current_minute_boundary - span_minutes) # Recalculate for last segment

        # 3. Find Sub-Sub Lord
        # The sequence starts with the Sub Lord itself
        current_sub_boundary = 0.0
        sub_sub_lord = None
        
        sub_lord_years = VIMSHOTTARI_YEARS[sub_lord]
        sub_span_minutes_total = (sub_lord_years / 120.0) * total_nakshatra_span_minutes
        
        for i in range(9):
            idx = (sub_lord_idx + i) % 9
            planet = VIMSHOTTARI_SEQUENCE[idx]
            years = VIMSHOTTARI_YEARS[planet]
            
            # Sub-Sub-lord span = (Years / 120) * Sub-lord Span
            sub_sub_span_minutes = (years / 120.0) * sub_span_minutes_total
            
            epsilon = 1e-9
            if current_sub_boundary <= minutes_into_sub < (current_sub_boundary + sub_sub_span_minutes - epsilon):
                sub_sub_lord = planet
                break
                
            current_sub_boundary += sub_sub_span_minutes
            
        # Fallback for the last segment if floating point precision causes it to miss
        if sub_sub_lord is None:
            sub_sub_lord = VIMSHOTTARI_SEQUENCE[(sub_lord_idx + 8) % 9]
            
        return {
            "star_lord": star_lord,
            "sub_lord": sub_lord,
            "sub_sub_lord": sub_sub_lord
        }

    def generate_chart(self, calculation_results: dict, ayanamsa_type: str = "LAHIRI"):
        """
        Takes the output from the MathEngine and maps everything to signs, houses, and nakshatras.
        """
        ascendant_deg = calculation_results["Ascendant"]
        planets_deg = calculation_results["Planets"]
        
        # 1. Map Ascendant (D1)
        asc_info = self.degree_to_zodiac(ascendant_deg)
        asc_sign_number = asc_info["sign_number"]
        
        # Ascendant (D9)
        asc_navamsa = self.calculate_navamsa(ascendant_deg, asc_info["sign"])
        
        # Compute Moon's attributes (Gana, Varna, Yoni, Nadi)
        from backend.rules.constants import NAKSHATRA_GANA, SIGN_VARNA, NAKSHATRA_YONI, NAKSHATRA_NADI
        
        moon_deg = planets_deg.get("Moon", 0)
        moon_nak_info = self.degree_to_nakshatra(moon_deg)
        moon_nak_idx = moon_nak_info["nakshatra_index"]
        
        moon_sign_info = self.degree_to_zodiac(moon_deg)
        moon_sign_name = moon_sign_info["sign"]

        # Ascendant details
        asc_sign = self.degree_to_zodiac(ascendant_deg)
        asc_nak = self.degree_to_nakshatra(ascendant_deg)
        asc_d9 = self.calculate_navamsa(ascendant_deg, d1_sign_name=asc_sign["sign"])
        asc_sub = self.calculate_sublords(ascendant_deg)
        
        chart_data = {
            "ascendant": {
                "degree": ascendant_deg,
                "sign": asc_info["sign"],
                "sign_number": asc_sign_number,
                "degree_in_sign": asc_info["degree"],
                "nakshatra": asc_nak["nakshatra"],
                "pada": asc_nak["pada"],
                "navamsa_sign": asc_navamsa["sign"],
                "navamsa_sign_number": asc_navamsa["sign_number"],
                "navamsa_number": asc_navamsa["navamsa_number"],
                "is_vargottama": asc_navamsa["is_vargottama"],
                "is_pushkara": asc_navamsa["is_pushkara"],
                "d2_sign_number": self.calculate_varga(ascendant_deg, 2)["sign_number"],
                "d9_sign_number": asc_navamsa["sign_number"],
                "d12_sign_number": self.calculate_varga(ascendant_deg, 12)["sign_number"],
                "d60_sign_number": self.calculate_varga(ascendant_deg, 60)["sign_number"],
                "kp_star_lord": asc_sub["star_lord"],
                "kp_sub_lord": asc_sub["sub_lord"],
                "kp_sub_sub_lord": asc_sub["sub_sub_lord"]
            },
            "moon_attributes": {
                "nakshatra": moon_nak_info["nakshatra"],
                "pada": moon_nak_info["pada"],
                "gana": NAKSHATRA_GANA[moon_nak_idx],
                "varna": SIGN_VARNA.get(moon_sign_name, ""),
                "yoni": NAKSHATRA_YONI[moon_nak_idx],
                "nadi": NAKSHATRA_NADI[moon_nak_idx]
            },
            "varga_charts": {
                "D1": {i: [] for i in range(1, 13)},
                "D2": {i: [] for i in range(1, 13)},
                "D9": {i: [] for i in range(1, 13)},
                "D12": {i: [] for i in range(1, 13)},
                "D60": {i: [] for i in range(1, 13)}
            },
            "planets": {},
            "kp_cusps": {}, # KP exact cusps with sub-lords
            "houses": {i: [] for i in range(1, 13)}, # Occupants of Vedic houses (for classical rules)
            "kp_houses": {i: [] for i in range(1, 13)} # Occupants of KP houses (Placidus)
        }
        
        # 1.5 Process 12 KP House Cusps
        house_cusps_sidereal = calculation_results.get("HouseCusps", [])
        for i, cusp_deg in enumerate(house_cusps_sidereal):
            cusp_num = i + 1
            z_info = self.degree_to_zodiac(cusp_deg)
            n_info = self.degree_to_nakshatra(cusp_deg)
            sub_info = self.calculate_sublords(cusp_deg)
            
            chart_data["kp_cusps"][cusp_num] = {
                "degree": cusp_deg,
                "sign": z_info["sign"],
                "sign_number": z_info["sign_number"],
                "nakshatra": n_info["nakshatra"],
                "star_lord": sub_info["star_lord"],
                "sub_lord": sub_info["sub_lord"],
                "sub_sub_lord": sub_info["sub_sub_lord"],
                "sign_lord": z_info["lord"],
                "kp_number": self.calculate_kp_number(cusp_deg)
            }
        
        from backend.rules.constants import EXALTED_SIGNS, DEBILITATED_SIGNS, COMBUSTION_ORBS
        
        sun_deg = planets_deg.get("Sun", 0)
        
        # 2. Map Planets
        for planet, degree in planets_deg.items():
            zodiac_info = self.degree_to_zodiac(degree)
            nakshatra_info = self.degree_to_nakshatra(degree)
            navamsa_info = self.calculate_navamsa(degree, zodiac_info["sign"])
            kp_sublords = self.calculate_sublords(degree) # Calculate sublords for planet
            
            # Calculate Vedic House (Whole Sign calculation)
            # Ascendant sign is house 1. The formula works because signs are 1-12.
            planet_sign_number = zodiac_info["sign_number"]
            house_vedic = ((planet_sign_number - asc_sign_number) % 12) + 1

            # Determine KP House (Placidus Cusps)
            # In KP, a planet is in House X if its degree >= Cusp X and < Cusp X+1
            # Note: Houses can span across multiple signs.
            house_kp = 12
            for h_num in range(1, 12):
                c1 = house_cusps_sidereal[h_num - 1]
                c2 = house_cusps_sidereal[h_num]
                
                # Handle 360/0 boundary
                if c1 < c2:
                    if c1 <= degree < c2:
                        house_kp = h_num
                        break
                else: # Boundary case (e.g. Cusp 12 in Pisces, Cusp 1 in Aries)
                    if degree >= c1 or degree < c2:
                        house_kp = h_num
                        break
            
            # Calculate Combustion (Asta)
            is_combust = False
            if planet in COMBUSTION_ORBS:
                distance_to_sun = abs(sun_deg - degree)
                if distance_to_sun > 180:
                    distance_to_sun = 360 - distance_to_sun
                if distance_to_sun <= COMBUSTION_ORBS[planet]:
                    is_combust = True
            
            planet_data = {
                "absolute_degree": degree,
                "sign": zodiac_info["sign"],
                "sign_number": planet_sign_number,
                "degree_in_sign": zodiac_info["degree"],
                "is_exalted": EXALTED_SIGNS.get(planet) == planet_sign_number,
                "is_debilitated": DEBILITATED_SIGNS.get(planet) == planet_sign_number,
                "is_combust": is_combust,
                "house": house_vedic, # For backward compatibility with classical evaluator
                "house_vedic": house_vedic,
                "house_kp": house_kp,
                "nakshatra": nakshatra_info["nakshatra"],
                "pada": nakshatra_info["pada"],
                "navamsa_sign": navamsa_info["sign"],
                "navamsa_sign_number": navamsa_info["sign_number"],
                "navamsa_number": navamsa_info["navamsa_number"],
                "is_vargottama": navamsa_info["is_vargottama"],
                "is_pushkara": navamsa_info["is_pushkara"],
                
                # New Vargas
                "d2_sign": self.calculate_varga(degree, 2)["sign"],
                "d2_sign_number": self.calculate_varga(degree, 2)["sign_number"],
                "d9_sign": navamsa_info["sign"],
                "d9_sign_number": navamsa_info["sign_number"],
                "d12_sign": self.calculate_varga(degree, 12)["sign"],
                "d12_sign_number": self.calculate_varga(degree, 12)["sign_number"],
                "d60_sign": self.calculate_varga(degree, 60)["sign"],
                "d60_sign_number": self.calculate_varga(degree, 60)["sign_number"],

                "kp_star_lord": kp_sublords["star_lord"],
                "kp_sub_lord": kp_sublords["sub_lord"],
                "kp_sub_sub_lord": kp_sublords["sub_sub_lord"],
                "kp_number": self.calculate_kp_number(degree),
                "is_navamsa_exalted": EXALTED_SIGNS.get(planet) == navamsa_info["sign_number"],
                "is_navamsa_debilitated": DEBILITATED_SIGNS.get(planet) == navamsa_info["sign_number"]
            }
            
            chart_data["planets"][planet] = planet_data
            
            # Map to Varga House structures (by Sign)
            chart_data["varga_charts"]["D1"][planet_sign_number].append(planet)
            chart_data["varga_charts"]["D2"][self.calculate_varga(degree, 2)["sign_number"]].append(planet)
            chart_data["varga_charts"]["D9"][navamsa_info["sign_number"]].append(planet)
            chart_data["varga_charts"]["D12"][self.calculate_varga(degree, 12)["sign_number"]].append(planet)
            chart_data["varga_charts"]["D60"][self.calculate_varga(degree, 60)["sign_number"]].append(planet)

            # Add to the House dictionary for easy searching later
            chart_data["houses"][house_vedic].append(planet)
            chart_data["kp_houses"][house_kp].append(planet)
            
        # 3. Calculate KP Significators
        chart_data["kp_significators"] = self.calculate_kp_significators(chart_data)
            
        return chart_data

    def calculate_kp_significators(self, chart_data: dict) -> dict:
        """
        Calculates KP Significators for all 12 houses.
        Levels:
        1: Star Lord of a house occupant.
        2: House Occupant.
        3: Star Lord of house owner.
        4: House Owner.
        """
        significators = {i: {"L1": [], "L2": [], "L3": [], "L4": []} for i in range(1, 13)}
        
        # Helper to get Star Lord of a planet
        def get_star_lord(p_name):
            return chart_data["planets"].get(p_name, {}).get("kp_star_lord")

        # Process each house
        for h_num in range(1, 13):
            cusp = chart_data["kp_cusps"][h_num]
            owner = cusp["sign_lord"]
            occupants = chart_data["kp_houses"][h_num]
            
            # Level 4: House Owner
            significators[h_num]["L4"].append(owner)
            
            # Level 2: House Occupants
            for occ in occupants:
                significators[h_num]["L2"].append(occ)
                # Level 1: Star Lord of Occupant
                sl = get_star_lord(occ)
                if sl and sl not in significators[h_num]["L1"]:
                    significators[h_num]["L1"].append(sl)
            
            # Level 3: Star Lord of House Owner
            owner_sl = get_star_lord(owner)
            if owner_sl and owner_sl not in significators[h_num]["L3"]:
                significators[h_num]["L3"].append(owner_sl)
                
        return significators

# Quick Test
if __name__ == "__main__":
    # Simulate output from our math engine for the test case
    mock_math_output = {
        'Ascendant': 305.01,
        'Planets': {
            'Sun': 59.06, 
            'Moon': 287.74, 
            'Mars': 50.90, 
            'Mercury': 63.89, 
            'Jupiter': 332.36, 
            'Venus': 23.92, 
            'Saturn': 6.57, 
            'Rahu': 131.10, 
            'Ketu': 311.10
        },
        'HouseCusps': [305.01 + (i*30) for i in range(12)] # Simple Equal House mock for testing
    }
    
    astro = AstrologyEngine()
    chart = astro.generate_chart(mock_math_output, ayanamsa_type="KP")
    
    print(f"Ascendant: {chart['ascendant']['sign']} (KP Star: {chart['ascendant']['kp_star_lord']})")
    
    print("\nHouses Overview:")
    for house, planets in chart["houses"].items():
        occupants = ", ".join(planets) if planets else "Empty"
        print(f"House {house}: {occupants}")

    print("\nKP Significators (House 1):")
    print(chart["kp_significators"][1])
