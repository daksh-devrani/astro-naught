from backend.rules.constants import (
    SIGN_LORDS, HOUSE_TYPES, SPECIAL_ASPECTS,
    EXALTED_SIGNS, DEBILITATED_SIGNS, MOOLATRIKONA_SIGNS, OWN_SIGNS,
    DIG_BALA, NATURAL_BENEFICS, NATURAL_MALEFICS, KARAKA_PLANETS,
    MANGLIK_HOUSES, KENDRA_HOUSES, TRIKONA_HOUSES, DUSTHANA_HOUSES,
    PANCH_MAHAPURUSHA, PLANETARY_RELATIONSHIPS
)

class RuleEvaluator:
    def __init__(self, chart_data: dict):
        self.chart = chart_data
        self.ascendant_sign_num = self.chart["ascendant"]["sign_number"]
    
    def get_house_lord(self, house_number: int):
        """
        Returns the planet that rules a specific house.
        """
        # Determine which sign falls in the requested house.
        # e.g. Asc (1) is 11 (Aquarius). 2nd house is 12 (Pisces).
        # Formula: (Ascendant_Sign + House_Number - 2) % 12 + 1
        sign_in_house = (self.ascendant_sign_num + house_number - 2) % 12 + 1
        lord = SIGN_LORDS[sign_in_house]
        return {
            "house": house_number,
            "sign": sign_in_house,
            "lord": lord
        }
        
    def get_lord_placement(self, house_number: int):
        """
        Finds where the lord of a given house is currently placed in the chart.
        """
        lord_info = self.get_house_lord(house_number)
        lord = lord_info["lord"]
        
        # Where is this planet sitting?
        for planet, data in self.chart["planets"].items():
            if planet == lord:
                lord_info["placement_house"] = data["house"]
                lord_info["placement_sign"] = data["sign"]
                
                # Useful rule description:
                lord_info["rule_string"] = f"Lord of House {house_number} ({lord}) is placed in House {data['house']}."
                return lord_info
                
        return lord_info

    def get_planets_in_house(self, house_number: int):
        """
        Returns all planets physically sitting in a house.
        """
        return self.chart["houses"].get(house_number, [])
        
    def evaluate_conjunctions(self):
        """
        Finds all houses with 2 or more planets.
        """
        conjunctions = []
        for house, occupants in self.chart["houses"].items():
            if len(occupants) > 1:
                conjunctions.append({
                    "house": house,
                    "planets": occupants,
                    "rule_string": f"Conjunction of {', '.join(occupants)} in House {house}."
                })
        return conjunctions

    def evaluate_yogas(self):
        """
        Scans the chart for specific classical combinations (Yogas).
        """
        yogas = []
        for house, occupants in self.chart["houses"].items():
            occupants_set = set(occupants)
            
            # Budhaditya Yoga
            if "Sun" in occupants_set and "Mercury" in occupants_set:
                yogas.append({
                    "name": "Budhaditya Yoga",
                    "house": house,
                    "planets": ["Sun", "Mercury"],
                    "description": f"Sun and Mercury conjunct in House {house}. Promotes high intelligence, analytical skills, and business acumen."
                })
            
            # Grahan Yoga (Eclipses)
            if "Sun" in occupants_set and ("Rahu" in occupants_set or "Ketu" in occupants_set):
                yogas.append({
                    "name": "Surya Grahan Yoga",
                    "house": house,
                    "planets": [p for p in occupants if p in ["Sun", "Rahu", "Ketu"]],
                    "description": f"Sun conjunct Nodes in House {house}. Can indicate issues with confidence, authority, or ego expression."
                })
            
            if "Moon" in occupants_set and ("Rahu" in occupants_set or "Ketu" in occupants_set):
                yogas.append({
                    "name": "Chandra Grahan Yoga",
                    "house": house,
                    "planets": [p for p in occupants if p in ["Moon", "Rahu", "Ketu"]],
                    "description": f"Moon conjunct Nodes in House {house}. Can indicate emotional volatility, mental stress, or intuitive overload."
                })
                
            # Gajakesari Yoga (Conjunct)
            if "Jupiter" in occupants_set and "Moon" in occupants_set:
                yogas.append({
                    "name": "Gajakesari Yoga",
                    "house": house,
                    "planets": ["Jupiter", "Moon"],
                    "description": f"Jupiter and Moon conjunct in House {house}. Indicates widespread respect, wisdom, and sustained prosperity."
                })
                
        # Gajakesari Yoga (Mutual Kendras: 1, 4, 7, 10 distance from each other)
        moon_house = self.chart["planets"].get("Moon", {}).get("house")
        jupiter_house = self.chart["planets"].get("Jupiter", {}).get("house")
        if moon_house and jupiter_house:
            dist = (moon_house - jupiter_house) % 12
            # 0=conjunct, 3=4th away, 6=7th away, 9=10th away
            if dist in [3, 6, 9]:
                yogas.append({
                    "name": "Gajakesari Yoga (Mutual Kendra)",
                    "houses": [moon_house, jupiter_house],
                    "planets": ["Jupiter", "Moon"],
                    "description": f"Jupiter and Moon are in mutual Kendras. Indicates strong reputation, wisdom, and noble pursuits."
                })

        return yogas

    def get_aspects_on_house(self, target_house: int):
        """
        Determines which planets are aspecting (looking at) a specific house.
        """
        aspecting_planets = []
        
        for planet, p_data in self.chart["planets"].items():
            p_house = p_data["house"]
            aspects = SPECIAL_ASPECTS.get(planet, [7])
            
            for asp in aspects:
                # If a planet is in house 2 and aspects 7th from itself:
                # 2 + 7 - 1 = 8th house.
                aspected_house = (p_house + asp - 2) % 12 + 1
                if aspected_house == target_house:
                    aspecting_planets.append(planet)
                    
        return aspecting_planets

    # ============================================================
    # ADVANCED JYOTISH RULES
    # ============================================================

    # --- Planet Dignity System ---
    def get_planet_dignity(self, planet: str) -> dict:
        """
        Returns the full dignity status of a planet:
        Exalted > Moolatrikona > Own Sign > Friend's Sign > Neutral > Enemy's Sign > Debilitated
        """
        p_data = self.chart["planets"].get(planet, {})
        sign_num = p_data.get("sign_number")
        if not sign_num:
            return {"planet": planet, "dignity": "Unknown"}

        dignity = "Neutral"
        dignity_score = 0  # Higher is better

        if EXALTED_SIGNS.get(planet) == sign_num:
            dignity = "Exalted"
            dignity_score = 6
        elif DEBILITATED_SIGNS.get(planet) == sign_num:
            dignity = "Debilitated"
            dignity_score = -6
        elif MOOLATRIKONA_SIGNS.get(planet) == sign_num:
            dignity = "Moolatrikona"
            dignity_score = 5
        elif sign_num in OWN_SIGNS.get(planet, []):
            dignity = "Own Sign"
            dignity_score = 4
        else:
            # Check friendship via PLANETARY_RELATIONSHIPS
            sign_lord = SIGN_LORDS.get(sign_num)
            if sign_lord and sign_lord != planet:
                rel = PLANETARY_RELATIONSHIPS.get(planet, {})
                if sign_lord in rel.get("Friends", []):
                    dignity = "Friend's Sign"
                    dignity_score = 2
                elif sign_lord in rel.get("Enemies", []):
                    dignity = "Enemy's Sign"
                    dignity_score = -2
                else:
                    dignity = "Neutral Sign"
                    dignity_score = 0

        return {
            "planet": planet,
            "sign_number": sign_num,
            "dignity": dignity,
            "dignity_score": dignity_score,
            "has_dig_bala": DIG_BALA.get(planet) == p_data.get("house"),
            "is_combust": p_data.get("is_combust", False),
            "rule_string": f"{planet} is {dignity} in sign {sign_num}."
        }

    def evaluate_all_dignities(self) -> list:
        """Returns dignity analysis for all planets."""
        return [self.get_planet_dignity(p) for p in self.chart["planets"]]

    # --- Panch Mahapurusha Yoga ---
    def evaluate_panch_mahapurusha(self) -> list:
        """
        Panch Mahapurusha Yoga forms when Mars, Mercury, Jupiter, Venus, or Saturn
        is in its Own Sign or Exalted AND placed in a Kendra house (1, 4, 7, 10).
        """
        yogas = []
        for planet, yoga_name in PANCH_MAHAPURUSHA.items():
            p_data = self.chart["planets"].get(planet, {})
            house = p_data.get("house")
            sign_num = p_data.get("sign_number")

            if house not in KENDRA_HOUSES:
                continue

            is_own = sign_num in OWN_SIGNS.get(planet, [])
            is_exalted = EXALTED_SIGNS.get(planet) == sign_num

            if is_own or is_exalted:
                dignity = "Exalted" if is_exalted else "Own Sign"
                yogas.append({
                    "name": yoga_name,
                    "planet": planet,
                    "house": house,
                    "dignity": dignity,
                    "description": f"{yoga_name}: {planet} is {dignity} in Kendra House {house}."
                })
        return yogas

    # --- Dhana Yoga (Wealth Combinations) ---
    def evaluate_dhana_yogas(self) -> list:
        """
        Dhana Yoga forms when lords of houses 1, 2, 5, 9, 11 are
        conjunct (in the same house) with each other.
        """
        yogas = []
        dhana_houses = [1, 2, 5, 9, 11]
        lords = {}
        for h in dhana_houses:
            info = self.get_house_lord(h)
            lord = info["lord"]
            p_data = self.chart["planets"].get(lord, {})
            placement = p_data.get("house")
            if placement:
                lords[h] = {"lord": lord, "placement": placement}

        # Check for conjunctions between Dhana house lords
        checked = set()
        for h1 in dhana_houses:
            for h2 in dhana_houses:
                if h1 >= h2:
                    continue
                pair = (h1, h2)
                if pair in checked:
                    continue
                checked.add(pair)

                l1 = lords.get(h1)
                l2 = lords.get(h2)
                if not l1 or not l2:
                    continue
                if l1["lord"] == l2["lord"]:
                    continue  # Same planet lords both houses — inherent connection, not conjunction

                if l1["placement"] == l2["placement"]:
                    yogas.append({
                        "name": "Dhana Yoga",
                        "lords": [f"H{h1}: {l1['lord']}", f"H{h2}: {l2['lord']}"],
                        "house": l1["placement"],
                        "description": f"Dhana Yoga: Lords of houses {h1} ({l1['lord']}) and {h2} ({l2['lord']}) conjunct in House {l1['placement']}. Indicates wealth potential."
                    })
        return yogas

    # --- Raja Yoga (Power Combinations) ---
    def evaluate_raja_yogas(self) -> list:
        """
        Raja Yoga forms when a Kendra lord (1,4,7,10) and a Trikona lord (1,5,9)
        conjunct in the same house, or exchange signs (Parivartana).
        """
        yogas = []
        kendra = [4, 7, 10]  # Exclude 1 to avoid duplicates
        trikona = [5, 9]     # Exclude 1

        kendra_lords = {}
        trikona_lords = {}

        for h in kendra:
            info = self.get_house_lord(h)
            p_data = self.chart["planets"].get(info["lord"], {})
            kendra_lords[h] = {"lord": info["lord"], "placement": p_data.get("house"), "sign": info["sign"]}

        for h in trikona:
            info = self.get_house_lord(h)
            p_data = self.chart["planets"].get(info["lord"], {})
            trikona_lords[h] = {"lord": info["lord"], "placement": p_data.get("house"), "sign": info["sign"]}

        for kh, kdata in kendra_lords.items():
            for th, tdata in trikona_lords.items():
                if kdata["lord"] == tdata["lord"]:
                    # Same planet lords both a Kendra and Trikona — Yoga Karaka
                    yogas.append({
                        "name": "Yoga Karaka",
                        "planet": kdata["lord"],
                        "houses": [kh, th],
                        "description": f"Yoga Karaka: {kdata['lord']} lords both Kendra {kh} and Trikona {th}. Extremely powerful for success."
                    })
                    continue

                # Conjunction check
                if kdata["placement"] and kdata["placement"] == tdata["placement"]:
                    yogas.append({
                        "name": "Raja Yoga (Conjunction)",
                        "planets": [kdata["lord"], tdata["lord"]],
                        "houses": [kh, th],
                        "conjunction_house": kdata["placement"],
                        "description": f"Raja Yoga: Kendra lord {kdata['lord']} (H{kh}) and Trikona lord {tdata['lord']} (H{th}) conjunct in House {kdata['placement']}."
                    })

                # Parivartana (sign exchange) check
                if kdata["placement"] and tdata["placement"]:
                    k_in_t_sign = (kdata["placement"] == th)
                    t_in_k_sign = (tdata["placement"] == kh)
                    if k_in_t_sign and t_in_k_sign:
                        yogas.append({
                            "name": "Raja Yoga (Parivartana)",
                            "planets": [kdata["lord"], tdata["lord"]],
                            "houses": [kh, th],
                            "description": f"Raja Yoga via Parivartana: Lords of H{kh} and H{th} have exchanged houses."
                        })
        return yogas

    # --- Viparita Raja Yoga ---
    def evaluate_viparita_raja_yogas(self) -> list:
        """
        Viparita Raja Yoga forms when the lord of a Dusthana house (6, 8, 12)
        is placed in another Dusthana house.
        """
        yogas = []
        dusthana_lords = {}

        for h in DUSTHANA_HOUSES:
            info = self.get_house_lord(h)
            p_data = self.chart["planets"].get(info["lord"], {})
            dusthana_lords[h] = {"lord": info["lord"], "placement": p_data.get("house")}

        yoga_names = {6: "Harsha", 8: "Sarala", 12: "Vimala"}

        for h, data in dusthana_lords.items():
            if data["placement"] in DUSTHANA_HOUSES and data["placement"] != h:
                yogas.append({
                    "name": f"{yoga_names[h]} Viparita Raja Yoga",
                    "lord_of": h,
                    "placed_in": data["placement"],
                    "planet": data["lord"],
                    "description": f"{yoga_names[h]} Viparita Raja Yoga: Lord of H{h} ({data['lord']}) placed in H{data['placement']}. Turns adversity into advantage."
                })
        return yogas

    # --- Neecha Bhanga Raja Yoga (Cancelled Debilitation) ---
    def evaluate_neecha_bhanga(self) -> list:
        """
        Neecha Bhanga Raja Yoga — debilitation of a planet gets cancelled under
        specific classical conditions, turning it into a source of great strength.
        
        Conditions checked:
        1. Lord of the sign where the planet is debilitated is in a Kendra from Lagna or Moon.
        2. Lord of the sign where the planet gets exalted is in a Kendra from Lagna or Moon.
        3. The planet is aspected by or conjunct with the lord of the debilitation sign.
        """
        yogas = []
        moon_house = self.chart["planets"].get("Moon", {}).get("house")

        for planet, p_data in self.chart["planets"].items():
            if not p_data.get("is_debilitated"):
                continue

            deb_sign = p_data["sign_number"]
            deb_sign_lord = SIGN_LORDS.get(deb_sign)
            cancellation_reasons = []

            # Condition 1: Lord of debilitation sign in Kendra from Lagna
            if deb_sign_lord:
                dsl_data = self.chart["planets"].get(deb_sign_lord, {})
                dsl_house = dsl_data.get("house")
                if dsl_house in KENDRA_HOUSES:
                    cancellation_reasons.append(
                        f"{deb_sign_lord} (lord of debilitation sign) is in Kendra House {dsl_house}."
                    )

            # Condition 2: Lord of the sign where planet gets exalted is in Kendra
            exalt_sign = EXALTED_SIGNS.get(planet)
            if exalt_sign:
                exalt_sign_lord = SIGN_LORDS.get(exalt_sign)
                if exalt_sign_lord:
                    esl_data = self.chart["planets"].get(exalt_sign_lord, {})
                    esl_house = esl_data.get("house")
                    if esl_house in KENDRA_HOUSES:
                        cancellation_reasons.append(
                            f"{exalt_sign_lord} (lord of exaltation sign) is in Kendra House {esl_house}."
                        )

            # Condition 3: Debilitated planet conjunct with lord of its debilitation sign
            if deb_sign_lord:
                dsl_data = self.chart["planets"].get(deb_sign_lord, {})
                if dsl_data.get("house") == p_data.get("house"):
                    cancellation_reasons.append(
                        f"{planet} is conjunct {deb_sign_lord} (lord of debilitation sign)."
                    )

            if cancellation_reasons:
                yogas.append({
                    "name": "Neecha Bhanga Raja Yoga",
                    "planet": planet,
                    "reasons": cancellation_reasons,
                    "description": f"Neecha Bhanga Raja Yoga for {planet}: Debilitation is cancelled. {' '.join(cancellation_reasons)} This turns weakness into extraordinary strength."
                })
        return yogas

    # --- Sun-Adjacent Yogas ---
    def evaluate_sun_yogas(self) -> list:
        """
        Veshi Yoga: A planet (not Moon/Rahu/Ketu) in 2nd from Sun.
        Vashi Yoga: A planet (not Moon/Rahu/Ketu) in 12th from Sun.
        Ubhayachari Yoga: Planets on both 2nd and 12th from Sun.
        """
        yogas = []
        sun_house = self.chart["planets"].get("Sun", {}).get("house")
        if not sun_house:
            return yogas

        excluded = {"Sun", "Moon", "Rahu", "Ketu"}
        house_2nd = (sun_house % 12) + 1       # 2nd from Sun
        house_12th = ((sun_house - 2) % 12) + 1  # 12th from Sun

        planets_2nd = [p for p in self.chart["houses"].get(house_2nd, []) if p not in excluded]
        planets_12th = [p for p in self.chart["houses"].get(house_12th, []) if p not in excluded]

        if planets_2nd:
            yogas.append({
                "name": "Veshi Yoga",
                "planets": planets_2nd,
                "house": house_2nd,
                "description": f"Veshi Yoga: {', '.join(planets_2nd)} in 2nd from Sun (H{house_2nd}). Enhances reputation and initiative."
            })

        if planets_12th:
            yogas.append({
                "name": "Vashi Yoga",
                "planets": planets_12th,
                "house": house_12th,
                "description": f"Vashi Yoga: {', '.join(planets_12th)} in 12th from Sun (H{house_12th}). Enhances influence and charisma."
            })

        if planets_2nd and planets_12th:
            yogas.append({
                "name": "Ubhayachari Yoga",
                "planets": planets_2nd + planets_12th,
                "description": f"Ubhayachari Yoga: Planets on both sides of the Sun. Indicates a highly protected and successful personality."
            })

        return yogas

    # --- Moon Yogas ---
    def evaluate_kemadurma_yoga(self) -> dict | None:
        """
        Kemadurma Yoga: No planets in 2nd or 12th house from Moon.
        Indicates potential for periods of loneliness, poverty, or emotional struggle.
        """
        moon_house = self.chart["planets"].get("Moon", {}).get("house")
        if not moon_house:
            return None

        house_2nd = (moon_house % 12) + 1
        house_12th = ((moon_house - 2) % 12) + 1

        planets_2nd = [p for p in self.chart["houses"].get(house_2nd, []) if p != "Moon"]
        planets_12th = [p for p in self.chart["houses"].get(house_12th, []) if p != "Moon"]

        if not planets_2nd and not planets_12th:
            return {
                "name": "Kemadurma Yoga",
                "moon_house": moon_house,
                "description": "Kemadurma Yoga: No planets flank the Moon (2nd and 12th from it are empty). May indicate periods of emotional isolation or financial difficulty. Cancelled if Moon is in Kendra or aspected by Jupiter."
            }
        return None

    def evaluate_chandra_mangal_yoga(self) -> dict | None:
        """
        Chandra-Mangal Yoga: Moon and Mars conjunct in the same house.
        Indicates wealth through courage, real estate, or bold action.
        """
        moon_house = self.chart["planets"].get("Moon", {}).get("house")
        mars_house = self.chart["planets"].get("Mars", {}).get("house")

        if moon_house and mars_house and moon_house == mars_house:
            return {
                "name": "Chandra-Mangal Yoga",
                "house": moon_house,
                "description": f"Chandra-Mangal Yoga: Moon and Mars conjunct in House {moon_house}. Indicates earning through courage, land, or bold enterprise."
            }
        return None

    def evaluate_amala_yoga(self) -> list:
        """
        Amala Yoga: A natural benefic in the 10th house from Lagna or Moon.
        Indicates a person of spotless character and noble reputation.
        """
        yogas = []
        # 10th from Lagna
        house_10_lagna = 10
        occupants_10 = self.chart["houses"].get(house_10_lagna, [])
        benefics_10_lagna = [p for p in occupants_10 if p in NATURAL_BENEFICS]

        if benefics_10_lagna:
            yogas.append({
                "name": "Amala Yoga (from Lagna)",
                "planets": benefics_10_lagna,
                "description": f"Amala Yoga: {', '.join(benefics_10_lagna)} in 10th from Lagna. Indicates spotless character and noble reputation."
            })

        # 10th from Moon
        moon_house = self.chart["planets"].get("Moon", {}).get("house")
        if moon_house:
            house_10_moon = ((moon_house + 8) % 12) + 1
            occupants_10_moon = self.chart["houses"].get(house_10_moon, [])
            benefics_10_moon = [p for p in occupants_10_moon if p in NATURAL_BENEFICS]

            if benefics_10_moon:
                yogas.append({
                    "name": "Amala Yoga (from Moon)",
                    "planets": benefics_10_moon,
                    "house": house_10_moon,
                    "description": f"Amala Yoga: {', '.join(benefics_10_moon)} in 10th from Moon (H{house_10_moon}). Noble conduct and public respect."
                })
        return yogas

    # --- Doshas (Defects) ---
    def evaluate_manglik_dosha(self) -> dict:
        """
        Manglik (Kuja) Dosha: Mars in houses 1, 2, 4, 7, 8, or 12 from Lagna or Moon.
        Significant for marriage compatibility analysis.
        """
        mars_house = self.chart["planets"].get("Mars", {}).get("house")
        moon_house = self.chart["planets"].get("Moon", {}).get("house")
        
        from_lagna = mars_house in MANGLIK_HOUSES if mars_house else False
        
        from_moon = False
        if mars_house and moon_house:
            mars_from_moon = ((mars_house - moon_house) % 12) + 1
            from_moon = mars_from_moon in MANGLIK_HOUSES

        is_manglik = from_lagna or from_moon
        severity = "None"
        if from_lagna and from_moon:
            severity = "High (from both Lagna and Moon)"
        elif from_lagna:
            severity = "Moderate (from Lagna)"
        elif from_moon:
            severity = "Moderate (from Moon)"

        # Check for cancellation conditions
        cancellations = []
        if is_manglik and mars_house:
            mars_sign = self.chart["planets"]["Mars"].get("sign_number")
            # Mars in own sign or exalted cancels dosha
            if mars_sign in OWN_SIGNS.get("Mars", []):
                cancellations.append("Mars is in its own sign.")
            if EXALTED_SIGNS.get("Mars") == mars_sign:
                cancellations.append("Mars is exalted.")
            # Jupiter aspecting Mars cancels
            aspects_on_mars_house = self.get_aspects_on_house(mars_house)
            if "Jupiter" in aspects_on_mars_house:
                cancellations.append("Jupiter aspects Mars.")

        return {
            "name": "Manglik (Kuja) Dosha",
            "is_manglik": is_manglik,
            "mars_house": mars_house,
            "from_lagna": from_lagna,
            "from_moon": from_moon,
            "severity": severity,
            "cancellations": cancellations,
            "is_cancelled": len(cancellations) > 0,
            "description": f"Mars is in House {mars_house}. Manglik: {severity}." + (
                f" However, dosha may be mitigated: {' '.join(cancellations)}" if cancellations else ""
            )
        }

    def evaluate_kaal_sarp_dosha(self) -> dict:
        """
        Kaal Sarp Dosha: All 7 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn)
        are hemmed between the Rahu-Ketu axis (all on one side).
        """
        rahu_house = self.chart["planets"].get("Rahu", {}).get("house")
        ketu_house = self.chart["planets"].get("Ketu", {}).get("house")

        if not rahu_house or not ketu_house:
            return {"name": "Kaal Sarp Dosha", "is_present": False}

        main_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

        # Check if all planets are on one side of Rahu-Ketu axis
        # "Between Rahu and Ketu" means going from Rahu to Ketu clockwise
        def is_between(planet_house, start, end):
            """Check if planet_house is between start and end going clockwise."""
            if start < end:
                return start < planet_house < end
            else:  # Wraps around
                return planet_house > start or planet_house < end

        all_rahu_to_ketu = True
        all_ketu_to_rahu = True

        for planet in main_planets:
            p_house = self.chart["planets"].get(planet, {}).get("house")
            if not p_house:
                return {"name": "Kaal Sarp Dosha", "is_present": False}

            if p_house == rahu_house or p_house == ketu_house:
                # Planet on the axis — partial Kaal Sarp
                continue

            if not is_between(p_house, rahu_house, ketu_house):
                all_rahu_to_ketu = False
            if not is_between(p_house, ketu_house, rahu_house):
                all_ketu_to_rahu = False

        is_present = all_rahu_to_ketu or all_ketu_to_rahu
        direction = ""
        if all_rahu_to_ketu:
            direction = "Kaal Sarp (Rahu-leading)"
        elif all_ketu_to_rahu:
            direction = "Kaal Amrit (Ketu-leading)"

        return {
            "name": "Kaal Sarp Dosha",
            "is_present": is_present,
            "rahu_house": rahu_house,
            "ketu_house": ketu_house,
            "type": direction,
            "description": f"{direction}: All planets hemmed between Rahu (H{rahu_house}) and Ketu (H{ketu_house}). Can indicate karmic struggles, delays, and intense spiritual transformation." if is_present else "No Kaal Sarp Dosha present."
        }

    def evaluate_sade_sati(self, current_saturn_sign: int = None) -> dict:
        """
        Sade Sati: Saturn transiting the 12th, 1st, or 2nd sign from the Moon sign.
        This is a 7.5-year period of testing and transformation.
        Uses natal Saturn position if no transit Saturn sign is provided.
        """
        moon_sign = self.chart["planets"].get("Moon", {}).get("sign_number")
        saturn_sign = current_saturn_sign or self.chart["planets"].get("Saturn", {}).get("sign_number")

        if not moon_sign or not saturn_sign:
            return {"name": "Sade Sati", "is_active": False}

        # Relative position of Saturn from Moon's sign
        relative = ((saturn_sign - moon_sign) % 12)
        # 0 = same sign (peak), 11 = 12th from Moon (rising), 1 = 2nd from Moon (setting)

        phase = None
        if relative == 11:
            phase = "Rising (12th from Moon)"
        elif relative == 0:
            phase = "Peak (over Moon)"
        elif relative == 1:
            phase = "Setting (2nd from Moon)"

        is_active = phase is not None

        return {
            "name": "Sade Sati",
            "is_active": is_active,
            "phase": phase,
            "moon_sign": moon_sign,
            "saturn_sign": saturn_sign,
            "description": f"Sade Sati is {phase}. Saturn ({saturn_sign}) is transiting near Moon's sign ({moon_sign}). A period of deep karmic testing and growth." if is_active else "Sade Sati is not currently active in the natal chart."
        }

    # --- Composite Strength Analysis ---
    def evaluate_planet_strengths(self) -> list:
        """
        Generates a composite strength summary for each planet considering:
        dignity, combustion, dig bala, and overall disposition.
        """
        strengths = []
        for planet in self.chart["planets"]:
            dignity = self.get_planet_dignity(planet)
            p_data = self.chart["planets"][planet]

            factors = []
            score = dignity["dignity_score"]

            # Dig Bala bonus
            if dignity["has_dig_bala"]:
                factors.append("Has Dig Bala (directional strength)")
                score += 2

            # Combustion penalty
            if p_data.get("is_combust"):
                factors.append("Combust by Sun (weakened)")
                score -= 3

            # Exaltation in Navamsa bonus
            if p_data.get("is_navamsa_exalted"):
                factors.append("Exalted in Navamsa (D9 strength)")
                score += 2

            # Debilitation in Navamsa penalty
            if p_data.get("is_navamsa_debilitated"):
                factors.append("Debilitated in Navamsa (D9 weakness)")
                score -= 2

            # Classify overall strength
            if score >= 6:
                disposition = "Very Strong"
            elif score >= 3:
                disposition = "Strong"
            elif score >= 0:
                disposition = "Average"
            elif score >= -3:
                disposition = "Weak"
            else:
                disposition = "Very Weak"

            strengths.append({
                "planet": planet,
                "dignity": dignity["dignity"],
                "house": p_data.get("house"),
                "score": score,
                "disposition": disposition,
                "factors": factors,
                "description": f"{planet}: {disposition} (score {score}). {dignity['dignity']} in H{p_data.get('house')}. {'; '.join(factors) if factors else 'No special modifiers.'}"
            })
        return strengths

    # --- Master Evaluator: All Advanced Rules ---
    def evaluate_all_advanced(self) -> dict:
        """
        Runs all advanced Jyotish evaluations and returns a comprehensive result.
        """
        kemadurma = self.evaluate_kemadurma_yoga()
        chandra_mangal = self.evaluate_chandra_mangal_yoga()

        moon_yogas = []
        if kemadurma:
            moon_yogas.append(kemadurma)
        if chandra_mangal:
            moon_yogas.append(chandra_mangal)

        return {
            "planet_dignities": self.evaluate_all_dignities(),
            "panch_mahapurusha": self.evaluate_panch_mahapurusha(),
            "dhana_yogas": self.evaluate_dhana_yogas(),
            "raja_yogas": self.evaluate_raja_yogas(),
            "viparita_raja_yogas": self.evaluate_viparita_raja_yogas(),
            "neecha_bhanga": self.evaluate_neecha_bhanga(),
            "sun_yogas": self.evaluate_sun_yogas(),
            "moon_yogas": moon_yogas,
            "amala_yoga": self.evaluate_amala_yoga(),
            "manglik_dosha": self.evaluate_manglik_dosha(),
            "kaal_sarp_dosha": self.evaluate_kaal_sarp_dosha(),
            "sade_sati": self.evaluate_sade_sati(),
            "planet_strengths": self.evaluate_planet_strengths()
        }

# Quick Test
if __name__ == "__main__":
    # We will need to run the engine to get a mock chart
    import sys
    import os
    # Add project root to path so we can import engine
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    
    from backend.engine.math_engine import VedicMathEngine
    from backend.engine.astrology import AstrologyEngine
    
    math_res = VedicMathEngine().calculate_positions(1998, 6, 14, 5, 0, 28.6139, 77.2090)
    chart = AstrologyEngine().generate_chart(math_res)
    
    evaluator = RuleEvaluator(chart)
    
    print("\n--- 7th House Analysis (Marriage/Partnership) ---")
    house = 7
    print(f"Occupants: {evaluator.get_planets_in_house(house)}")
    lord = evaluator.get_lord_placement(house)
    print(lord["rule_string"])
    print(f"Aspects on 7th House: {evaluator.get_aspects_on_house(house)}")
    
    print("\n--- Conjunctions ---")
    for conj in evaluator.evaluate_conjunctions():
        print(conj["rule_string"])
