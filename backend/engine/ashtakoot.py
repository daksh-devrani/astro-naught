import math

class AshtakootCalculator:
    """
    Calculates the traditional 36-Guna Ashtakoot Match based on Moon's Longitude.
    """
    
    # 27 Nakshatras
    # Nadi mapping: 0=Adi, 1=Madhya, 2=Antya
    # Gana mapping: 0=Deva, 1=Manushya, 2=Rakshasa
    # Yoni mapping (animal number 0-13)
    NAKSHATRAS = [
        {"name": "Ashwini", "nadi": 0, "gana": 0, "yoni": 0},
        {"name": "Bharani", "nadi": 1, "gana": 1, "yoni": 1},
        {"name": "Krittika", "nadi": 2, "gana": 2, "yoni": 2},
        {"name": "Rohini", "nadi": 2, "gana": 1, "yoni": 3},
        {"name": "Mrigashira", "nadi": 1, "gana": 0, "yoni": 3},
        {"name": "Ardra", "nadi": 0, "gana": 1, "yoni": 4},
        {"name": "Punarvasu", "nadi": 0, "gana": 0, "yoni": 5},
        {"name": "Pushya", "nadi": 1, "gana": 0, "yoni": 2},
        {"name": "Ashlesha", "nadi": 2, "gana": 2, "yoni": 5},
        {"name": "Magha", "nadi": 2, "gana": 2, "yoni": 6},
        {"name": "Purva Phalguni", "nadi": 1, "gana": 1, "yoni": 6},
        {"name": "Uttara Phalguni", "nadi": 0, "gana": 1, "yoni": 7},
        {"name": "Hasta", "nadi": 0, "gana": 0, "yoni": 8},
        {"name": "Chitra", "nadi": 1, "gana": 2, "yoni": 9},
        {"name": "Swati", "nadi": 2, "gana": 0, "yoni": 8},
        {"name": "Vishakha", "nadi": 2, "gana": 2, "yoni": 9},
        {"name": "Anuradha", "nadi": 1, "gana": 0, "yoni": 10},
        {"name": "Jyeshtha", "nadi": 0, "gana": 2, "yoni": 10},
        {"name": "Mula", "nadi": 0, "gana": 2, "yoni": 4},
        {"name": "Purva Ashadha", "nadi": 1, "gana": 1, "yoni": 11},
        {"name": "Uttara Ashadha", "nadi": 2, "gana": 1, "yoni": 12},
        {"name": "Shravana", "nadi": 2, "gana": 0, "yoni": 11},
        {"name": "Dhanishta", "nadi": 1, "gana": 2, "yoni": 13},
        {"name": "Shatabhisha", "nadi": 0, "gana": 2, "yoni": 0},
        {"name": "Purva Bhadrapada", "nadi": 0, "gana": 1, "yoni": 13},
        {"name": "Uttara Bhadrapada", "nadi": 1, "gana": 1, "yoni": 7},
        {"name": "Revati", "nadi": 2, "gana": 0, "yoni": 1},
    ]
    
    YONI_COMPATIBILITY = [
        # simplified matrix
        [4, 2, 2, 3, 2, 2, 2, 1, 0, 1, 2, 1, 2, 2], # 0
        [2, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1, 2, 1, 2], # 1
        [2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1, 2, 1], # 2
        [3, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1, 2], # 3
        [2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1], # 4
        [2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0], # 5
        [2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1], # 6
        [1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2], # 7
        [0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2], # 8
        [1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2], # 9
        [2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2], # 10
        [1, 2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2], # 11
        [2, 1, 2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3], # 12
        [2, 2, 1, 2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4], # 13
    ]
    
    # 1=Aries, 2=Taurus...
    SIGN_LORDS = {
        1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
        5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
        9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
    }
    
    PLANET_FRIENDS = {
        'Sun': {'friends': ['Moon', 'Mars', 'Jupiter'], 'neutral': ['Mercury'], 'enemies': ['Venus', 'Saturn']},
        'Moon': {'friends': ['Sun', 'Mercury'], 'neutral': ['Mars', 'Jupiter', 'Venus', 'Saturn'], 'enemies': []},
        'Mars': {'friends': ['Sun', 'Moon', 'Jupiter'], 'neutral': ['Venus', 'Saturn'], 'enemies': ['Mercury']},
        'Mercury': {'friends': ['Sun', 'Venus'], 'neutral': ['Mars', 'Jupiter', 'Saturn'], 'enemies': ['Moon']},
        'Jupiter': {'friends': ['Sun', 'Moon', 'Mars'], 'neutral': ['Saturn'], 'enemies': ['Mercury', 'Venus']},
        'Venus': {'friends': ['Mercury', 'Saturn'], 'neutral': ['Mars', 'Jupiter'], 'enemies': ['Sun', 'Moon']},
        'Saturn': {'friends': ['Mercury', 'Venus'], 'neutral': ['Jupiter'], 'enemies': ['Sun', 'Moon', 'Mars']},
    }
    
    @staticmethod
    def get_nakshatra(longitude: float):
        nak_idx = int(math.floor(longitude / (13 + 1/3))) % 27
        return AshtakootCalculator.NAKSHATRAS[nak_idx], nak_idx
        
    @staticmethod
    def calculate_varna(sign_b: int, sign_g: int):
        # 1=Brahmin(Water 4,8,12), 2=Kshatriya(Fire 1,5,9), 3=Vaishya(Earth 2,6,10), 4=Shudra(Air 3,7,11)
        def get_varna(s):
            if s in [4, 8, 12]: return 1
            if s in [1, 5, 9]: return 2
            if s in [2, 6, 10]: return 3
            if s in [3, 7, 11]: return 4
            return 4
        
        v_b = get_varna(sign_b)
        v_g = get_varna(sign_g)
        
        if v_b <= v_g: return 1
        return 0
        
    @staticmethod
    def calculate_vashya(sign_b: int, sign_g: int):
        return 2 if sign_b == sign_g else 1
        
    @staticmethod
    def calculate_tara(nak_b: int, nak_g: int):
        tara_bg = ((nak_g - nak_b) % 9) + 1
        tara_gb = ((nak_b - nak_g) % 9) + 1
        
        bg_good = tara_bg not in [3, 5, 7]
        gb_good = tara_gb not in [3, 5, 7]
        
        if bg_good and gb_good: return 3
        if bg_good or gb_good: return 1.5
        return 0
        
    @staticmethod
    def calculate_yoni(yoni_b: int, yoni_g: int):
        try:
            return AshtakootCalculator.YONI_COMPATIBILITY[yoni_b][yoni_g]
        except:
            return 2
            
    @staticmethod
    def calculate_graha_maitri(sign_b: int, sign_g: int):
        lord_b = AshtakootCalculator.SIGN_LORDS.get(sign_b, 'Sun')
        lord_g = AshtakootCalculator.SIGN_LORDS.get(sign_g, 'Sun')
        
        if lord_b == lord_g: return 5
        
        rel_b = 1 if lord_g in AshtakootCalculator.PLANET_FRIENDS[lord_b]['friends'] else (0.5 if lord_g in AshtakootCalculator.PLANET_FRIENDS[lord_b]['neutral'] else 0)
        rel_g = 1 if lord_b in AshtakootCalculator.PLANET_FRIENDS[lord_g]['friends'] else (0.5 if lord_b in AshtakootCalculator.PLANET_FRIENDS[lord_g]['neutral'] else 0)
        
        score_map = {
            2: 5, 1.5: 4, 1: 3, 0.5: 1, 0: 0
        }
        return score_map.get(rel_b + rel_g, 0)
        
    @staticmethod
    def calculate_gana(gana_b: int, gana_g: int):
        if gana_b == gana_g: return 6
        if gana_b == 0 and gana_g == 1: return 6
        if gana_b == 1 and gana_g == 0: return 5
        if gana_g == 2 and gana_b == 0: return 1
        if gana_b == 2 and gana_g == 0: return 0
        if gana_g == 2 and gana_b == 1: return 0
        if gana_b == 2 and gana_g == 1: return 0
        return 3
        
    @staticmethod
    def calculate_bhakoot(sign_b: int, sign_g: int):
        if sign_b == sign_g: return 7
        dist = ((sign_g - sign_b) % 12) + 1
        # Bad combinations: 2/12, 6/8, 5/9
        if dist in [2, 12, 6, 8, 5, 9]: return 0
        return 7
        
    @staticmethod
    def calculate_nadi(nadi_b: int, nadi_g: int):
        if nadi_b == nadi_g: return 0
        return 8

    @staticmethod
    def calculate(moon_b_deg: float, moon_g_deg: float, sign_b: int, sign_g: int):
        nak_b_data, nak_b_idx = AshtakootCalculator.get_nakshatra(moon_b_deg)
        nak_g_data, nak_g_idx = AshtakootCalculator.get_nakshatra(moon_g_deg)
        
        res = {
            "varna": AshtakootCalculator.calculate_varna(sign_b, sign_g),
            "vashya": AshtakootCalculator.calculate_vashya(sign_b, sign_g),
            "tara": AshtakootCalculator.calculate_tara(nak_b_idx, nak_g_idx),
            "yoni": AshtakootCalculator.calculate_yoni(nak_b_data["yoni"], nak_g_data["yoni"]),
            "graha_maitri": AshtakootCalculator.calculate_graha_maitri(sign_b, sign_g),
            "gana": AshtakootCalculator.calculate_gana(nak_b_data["gana"], nak_g_data["gana"]),
            "bhakoot": AshtakootCalculator.calculate_bhakoot(sign_b, sign_g),
            "nadi": AshtakootCalculator.calculate_nadi(nak_b_data["nadi"], nak_g_data["nadi"])
        }
        
        total = sum(res.values())
        return {
            "total_score": total,
            "max_score": 36,
            "breakdown": res,
            "boy_nakshatra": nak_b_data["name"],
            "girl_nakshatra": nak_g_data["name"]
        }
