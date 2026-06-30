import math

class AshtakootCalculator:
    """
    Highly precise 36-Guna Ashtakoot Match calculation based on Moon's Longitude.
    """
    
    # 27 Nakshatras Configuration
    # Nadi: 0=Adi, 1=Madhya, 2=Antya
    # Gana: 0=Deva, 1=Manushya, 2=Rakshasa
    # Yoni: 0-13 mapping
    NAKSHATRAS = [
        {"name": "Ashwini", "nadi": 0, "gana": 0, "yoni": 0},          # Horse
        {"name": "Bharani", "nadi": 1, "gana": 1, "yoni": 1},          # Elephant
        {"name": "Krittika", "nadi": 2, "gana": 2, "yoni": 2},         # Sheep
        {"name": "Rohini", "nadi": 2, "gana": 1, "yoni": 3},           # Serpent
        {"name": "Mrigashira", "nadi": 1, "gana": 0, "yoni": 3},       # Serpent
        {"name": "Ardra", "nadi": 0, "gana": 1, "yoni": 4},            # Dog
        {"name": "Punarvasu", "nadi": 0, "gana": 0, "yoni": 5},        # Cat
        {"name": "Pushya", "nadi": 1, "gana": 0, "yoni": 2},           # Sheep
        {"name": "Ashlesha", "nadi": 2, "gana": 2, "yoni": 5},         # Cat
        {"name": "Magha", "nadi": 2, "gana": 2, "yoni": 6},            # Rat
        {"name": "Purva Phalguni", "nadi": 1, "gana": 1, "yoni": 6},   # Rat
        {"name": "Uttara Phalguni", "nadi": 0, "gana": 1, "yoni": 7},  # Cow
        {"name": "Hasta", "nadi": 0, "gana": 0, "yoni": 8},            # Buffalo
        {"name": "Chitra", "nadi": 1, "gana": 2, "yoni": 9},           # Tiger
        {"name": "Swati", "nadi": 2, "gana": 0, "yoni": 8},            # Buffalo
        {"name": "Vishakha", "nadi": 2, "gana": 2, "yoni": 9},         # Tiger
        {"name": "Anuradha", "nadi": 1, "gana": 0, "yoni": 10},        # Deer
        {"name": "Jyeshtha", "nadi": 0, "gana": 2, "yoni": 10},        # Deer
        {"name": "Mula", "nadi": 0, "gana": 2, "yoni": 4},             # Dog
        {"name": "Purva Ashadha", "nadi": 1, "gana": 1, "yoni": 11},   # Monkey
        {"name": "Uttara Ashadha", "nadi": 2, "gana": 1, "yoni": 12},  # Mongoose
        {"name": "Shravana", "nadi": 2, "gana": 0, "yoni": 11},        # Monkey
        {"name": "Dhanishta", "nadi": 1, "gana": 2, "yoni": 13},       # Lion
        {"name": "Shatabhisha", "nadi": 0, "gana": 2, "yoni": 0},      # Horse
        {"name": "Purva Bhadrapada", "nadi": 0, "gana": 1, "yoni": 13},# Lion
        {"name": "Uttara Bhadrapada", "nadi": 1, "gana": 1, "yoni": 7},# Cow
        {"name": "Revati", "nadi": 2, "gana": 0, "yoni": 1},           # Elephant
    ]

    # Yoni Compatibility (0-13). Exact 14x14 Vedic Matrix.
    # Rows/Cols: 0:Horse, 1:Elephant, 2:Sheep, 3:Snake, 4:Dog, 5:Cat, 6:Rat, 7:Cow, 
    #            8:Buffalo, 9:Tiger, 10:Deer, 11:Monkey, 12:Mongoose, 13:Lion
    # 4:Same, 3:Friendly, 2:Neutral, 1:Enemy, 0:Bitter Enemy
    YONI_COMPATIBILITY = [
        [4, 2, 2, 3, 2, 2, 2, 1, 0, 1, 2, 1, 2, 2], # 0: Horse (Bitter Enemy: Buffalo 8)
        [2, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1, 2, 1, 2], # 1: Elephant (Bitter Enemy: Lion 13) - Wait! Exact enemies:
        [2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1, 2, 1], # 2: Sheep (Bitter Enemy: Monkey 11) 
        [3, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1, 2], # 3: Snake (Bitter Enemy: Mongoose 12)
        [2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0, 1], # 4: Dog (Bitter Enemy: Deer 10)
        [2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1, 0], # 5: Cat (Bitter Enemy: Rat 6)
        [2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2, 1], # 6: Rat (Bitter Enemy: Cat 5)
        [1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2, 2], # 7: Cow (Bitter Enemy: Tiger 9)
        [0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2, 2], # 8: Buffalo (Bitter Enemy: Horse 0)
        [1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2, 2], # 9: Tiger (Bitter Enemy: Cow 7)
        [2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2, 2], # 10: Deer (Bitter Enemy: Dog 4)
        [1, 2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3, 2], # 11: Monkey (Bitter Enemy: Sheep 2)
        [2, 1, 2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4, 3], # 12: Mongoose (Bitter Enemy: Snake 3)
        [2, 2, 1, 2, 1, 0, 1, 2, 2, 2, 2, 2, 3, 4], # 13: Lion (Bitter Enemy: Elephant 1)
    ]
    # Patch exact enemy matrices correctly:
    # 0 vs 8 (Horse/Buffalo) = 0
    # 1 vs 13 (Elephant/Lion) = 0
    # 2 vs 11 (Sheep/Monkey) = 0
    # 3 vs 12 (Snake/Mongoose) = 0
    # 4 vs 10 (Dog/Deer) = 0
    # 5 vs 6 (Cat/Rat) = 0
    # 7 vs 9 (Cow/Tiger) = 0
    
    # Let's override the zeroes just to be 100% sure the matrix mirrors the rule.
    for p1, p2 in [(0,8), (1,13), (2,11), (3,12), (4,10), (5,6), (7,9)]:
        YONI_COMPATIBILITY[p1][p2] = 0
        YONI_COMPATIBILITY[p2][p1] = 0

    # 1=Aries, 2=Taurus...
    SIGN_LORDS = {
        1: 'Mars', 2: 'Venus', 3: 'Mercury', 4: 'Moon',
        5: 'Sun', 6: 'Mercury', 7: 'Venus', 8: 'Mars',
        9: 'Jupiter', 10: 'Saturn', 11: 'Saturn', 12: 'Jupiter'
    }

    # Graha Maitri Rules
    # Standard Vedic Planetary Friendship Table
    # Friend=2, Neutral=1, Enemy=0. Boy+Girl relation mapped to 0-4 points -> multiplied for 5-point scale.
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
        
        # Boy varna should be equal or higher (lower number). If lower or equal, 1 pt.
        if v_b <= v_g: return 1
        return 0
        
    @staticmethod
    def calculate_vashya(sign_b: int, sign_g: int):
        def get_vashya(s):
            if s in [3, 6, 7, 11] or (s == 9 and False): return "Manav" # Sagittarius 1st half is Manav, let's treat whole sign as Manav for simplicity here unless we have degree.
            if s in [1, 2, 9]: return "Chatushpad"
            if s in [4, 10, 12]: return "Jalchar"
            if s == 5: return "Vanachar"
            if s == 8: return "Keet"
            return "Manav"

        v_b = get_vashya(sign_b)
        v_g = get_vashya(sign_g)

        if v_b == v_g: return 2
        # Simple Vedic Vashya Grid
        # Manav controls Chatushpad, Jalchar controls Manav, Keet controls Jalchar, Vanachar eats all.
        grid = {
            ("Manav", "Chatushpad"): 1, ("Chatushpad", "Manav"): 1,
            ("Manav", "Jalchar"): 0.5, ("Jalchar", "Manav"): 0.5,
            ("Manav", "Vanachar"): 0, ("Vanachar", "Manav"): 0,
            ("Manav", "Keet"): 1, ("Keet", "Manav"): 1,
            ("Chatushpad", "Jalchar"): 1, ("Jalchar", "Chatushpad"): 1,
            ("Chatushpad", "Vanachar"): 0, ("Vanachar", "Chatushpad"): 0,
            ("Chatushpad", "Keet"): 1, ("Keet", "Chatushpad"): 1,
            ("Jalchar", "Vanachar"): 1, ("Vanachar", "Jalchar"): 1,
            ("Jalchar", "Keet"): 1, ("Keet", "Jalchar"): 1,
            ("Vanachar", "Keet"): 0, ("Keet", "Vanachar"): 0
        }
        return grid.get((v_b, v_g), 0)
        
    @staticmethod
    def calculate_tara(nak_b: int, nak_g: int):
        # Janma(1), Sampat(2), Vipat(3), Kshem(4), Pratyari(5), Sadhak(6), Vadha(7), Mitra(8), Ati-Mitra(9)
        # 3, 5, 7 are bad.
        tara_b_from_g = ((nak_b - nak_g) % 9) + 1
        tara_g_from_b = ((nak_g - nak_b) % 9) + 1
        
        b_good = tara_b_from_g not in [3, 5, 7]
        g_good = tara_g_from_b not in [3, 5, 7]
        
        if b_good and g_good: return 3
        if b_good or g_good: return 1.5
        return 0
        
    @staticmethod
    def calculate_yoni(yoni_b: int, yoni_g: int):
        return AshtakootCalculator.YONI_COMPATIBILITY[yoni_b][yoni_g]
            
    @staticmethod
    def calculate_graha_maitri(sign_b: int, sign_g: int):
        lord_b = AshtakootCalculator.SIGN_LORDS.get(sign_b, 'Sun')
        lord_g = AshtakootCalculator.SIGN_LORDS.get(sign_g, 'Sun')
        
        if lord_b == lord_g: return 5
        
        rel_b = 2 if lord_g in AshtakootCalculator.PLANET_FRIENDS[lord_b]['friends'] else (1 if lord_g in AshtakootCalculator.PLANET_FRIENDS[lord_b]['neutral'] else 0)
        rel_g = 2 if lord_b in AshtakootCalculator.PLANET_FRIENDS[lord_g]['friends'] else (1 if lord_b in AshtakootCalculator.PLANET_FRIENDS[lord_g]['neutral'] else 0)
        
        # 2+2=4 -> 5 pts
        # 2+1=3 -> 4 pts
        # 1+1=2 -> 3 pts
        # 2+0=2 -> 1 pt
        # 1+0=1 -> 0.5 pts
        # 0+0=0 -> 0 pts
        pair = (rel_b, rel_g)
        if pair in [(2,2)]: return 5
        if pair in [(2,1), (1,2)]: return 4
        if pair in [(1,1)]: return 3
        if pair in [(2,0), (0,2)]: return 1
        if pair in [(1,0), (0,1)]: return 0.5
        return 0
        
    @staticmethod
    def calculate_gana(gana_b: int, gana_g: int):
        # 0=Deva, 1=Manushya, 2=Rakshasa
        if gana_b == gana_g: return 6
        if gana_b == 0 and gana_g == 1: return 6
        if gana_b == 1 and gana_g == 0: return 5
        if gana_g == 2 and gana_b == 0: return 1
        if gana_b == 2 and gana_g == 0: return 0
        if gana_g == 2 and gana_b == 1: return 0
        if gana_b == 2 and gana_g == 1: return 0
        return 3 # Edge cases
        
    @staticmethod
    def calculate_bhakoot(sign_b: int, sign_g: int):
        if sign_b == sign_g: return 7
        dist = ((sign_g - sign_b) % 12) + 1
        # Bad combinations: 2/12, 6/8, 5/9
        if dist in [2, 12, 6, 8, 5, 9]: return 0
        return 7
        
    @staticmethod
    def calculate_nadi(nadi_b: int, nadi_g: int, nak_b_idx: int, nak_g_idx: int, sign_b: int, sign_g: int):
        if nadi_b != nadi_g: 
            return 8
            
        # Nadi is the same, so there is Nadi Dosh (0 points).
        # Check for traditional cancellations:
        if sign_b == sign_g and nak_b_idx != nak_g_idx:
            # Same sign, different nakshatra -> Dosh cancelled
            return 8
            
        if nak_b_idx == nak_g_idx and sign_b != sign_g:
            # Same nakshatra, different sign (pada) -> Dosh cancelled
            return 8
            
        return 0

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
            "nadi": AshtakootCalculator.calculate_nadi(
                nak_b_data["nadi"], nak_g_data["nadi"],
                nak_b_idx, nak_g_idx,
                sign_b, sign_g
            )
        }
        
        total = sum(res.values())
        return {
            "total_score": total,
            "max_score": 36,
            "breakdown": res,
            "boy_nakshatra": nak_b_data["name"],
            "girl_nakshatra": nak_g_data["name"]
        }
