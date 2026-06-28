# Astrological Constants and Mappings

# Rule 1: Sign Lords
# Maps the Zodiac Sign (1-12) to its ruling planet.
SIGN_LORDS = {
    1: "Mars",       # Aries
    2: "Venus",      # Taurus
    3: "Mercury",    # Gemini
    4: "Moon",       # Cancer
    5: "Sun",        # Leo
    6: "Mercury",    # Virgo
    7: "Venus",      # Libra
    8: "Mars",       # Scorpio
    9: "Jupiter",    # Sagittarius
    10: "Saturn",    # Capricorn
    11: "Saturn",    # Aquarius
    12: "Jupiter"    # Pisces
}

# Exaltation and Debilitation Signs (mapped by Sign Number 1-12)
EXALTED_SIGNS = {
    "Sun": 1,       # Aries
    "Moon": 2,      # Taurus
    "Mars": 10,     # Capricorn
    "Mercury": 6,   # Virgo
    "Jupiter": 4,   # Cancer
    "Venus": 12,    # Pisces
    "Saturn": 7,    # Libra
    "Rahu": 2,      # Taurus (Commonly accepted)
    "Ketu": 8       # Scorpio (Commonly accepted)
}

DEBILITATED_SIGNS = {
    "Sun": 7,       # Libra
    "Moon": 8,      # Scorpio
    "Mars": 4,      # Cancer
    "Mercury": 12,  # Pisces
    "Jupiter": 10,  # Capricorn
    "Venus": 6,     # Virgo
    "Saturn": 1,    # Aries
    "Rahu": 8,      # Scorpio
    "Ketu": 2       # Taurus
}

# Combustion (Asta) Orbs: Degrees from Sun at which a planet becomes Combust
COMBUSTION_ORBS = {
    "Moon": 12,
    "Mars": 17,
    "Mercury": 14,
    "Jupiter": 11,
    "Venus": 10,
    "Saturn": 15
}

# Nakshatra Attributes (Indexed 0-26, matching Ashwini to Revati)
# Used for Kundali matching (Ashtakoot) and personality profiling.

# Gana: Deva (Divine), Manushya (Human), Rakshasa (Demon)
NAKSHATRA_GANA = [
    "Deva", "Manushya", "Rakshasa",   # Ashwini, Bharani, Krittika
    "Manushya", "Deva", "Manushya",   # Rohini, Mrigashira, Ardra
    "Deva", "Deva", "Rakshasa",       # Punarvasu, Pushya, Ashlesha
    "Rakshasa", "Manushya", "Manushya",# Magha, Purva Phalguni, Uttara Phalguni
    "Deva", "Rakshasa", "Deva",       # Hasta, Chitra, Swati
    "Rakshasa", "Deva", "Rakshasa",   # Vishakha, Anuradha, Jyeshtha
    "Rakshasa", "Manushya", "Manushya",# Mula, Purva Ashadha, Uttara Ashadha
    "Deva", "Rakshasa", "Rakshasa",   # Shravana, Dhanishta, Shatabhisha
    "Manushya", "Manushya", "Deva"    # Purva Bhadrapada, Uttara Bhadrapada, Revati
]

# Varna: Brahmin, Kshatriya, Vaishya, Shudra (By Nakshatra - mainly used for match-making)
NAKSHATRA_VARNA = [
    "Vaishya", "Shudra", "Brahmin",    # Ashwini, Bharani, Krittika
    "Shudra", "Vaishya", "Shudra",     # Rohini, Mrigashira, Ardra
    "Brahmin", "Kshatriya", "Shudra",  # Punarvasu, Pushya, Ashlesha
    "Shudra", "Brahmin", "Kshatriya",  # Magha, Purva Phalguni, Uttara Phalguni
    "Vaishya", "Shudra", "Brahmin",    # Hasta, Chitra, Swati
    "Shudra", "Brahmin", "Brahmin",    # Vishakha, Anuradha, Jyeshtha
    "Shudra", "Brahmin", "Kshatriya",  # Mula, Purva Ashadha, Uttara Ashadha
    "Shudra", "Vaishya", "Shudra",     # Shravana, Dhanishta, Shatabhisha
    "Brahmin", "Kshatriya", "Vaishya"  # Purva Bhadrapada, Uttara Bhadrapada, Revati
]

# Varna based on Zodiac Sign (Rashi) - used for general personality profiling
SIGN_VARNA = {
    "Cancer": "Brahmin", "Scorpio": "Brahmin", "Pisces": "Brahmin",
    "Aries": "Kshatriya", "Leo": "Kshatriya", "Sagittarius": "Kshatriya",
    "Taurus": "Vaishya", "Virgo": "Vaishya", "Capricorn": "Vaishya",
    "Gemini": "Shudra", "Libra": "Shudra", "Aquarius": "Shudra"
}

# --- ASTROLOGICAL CONSTANTS ---

# Directions
DIRECTIONS = {
    "North": ["Aries", "Cancer", "Libra", "Capricorn"],
    "South": ["Taurus", "Leo", "Scorpio", "Aquarius"],
    "East": ["Gemini", "Virgo", "Sagittarius", "Pisces"],
    "West": [] # (Can be filled if needed theoretically)
}

# Vimshottari Mahadasha out of 120 years (Used for KP Sub-lords)
VIMSHOTTARI_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10,
    "Mars": 7, "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17
}

# Vimshottari Sequence mapping
VIMSHOTTARI_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", 
    "Rahu", "Jupiter", "Saturn", "Mercury"
]

# Yoni: Animal symbol representing sexual and instinctual compatibility
NAKSHATRA_YONI = [
    "Horse", "Elephant", "Goat",        # Ashwini, Bharani, Krittika
    "Serpent", "Serpent", "Dog",         # Rohini, Mrigashira, Ardra
    "Cat", "Goat", "Cat",               # Punarvasu, Pushya, Ashlesha
    "Rat", "Rat", "Cow",                # Magha, Purva Phalguni, Uttara Phalguni
    "Buffalo", "Tiger", "Buffalo",      # Hasta, Chitra, Swati
    "Tiger", "Deer", "Deer",            # Vishakha, Anuradha, Jyeshtha
    "Dog", "Monkey", "Mongoose",        # Mula, Purva Ashadha, Uttara Ashadha
    "Monkey", "Lion", "Horse",          # Shravana, Dhanishta, Shatabhisha
    "Lion", "Cow", "Elephant"           # Purva Bhadrapada, Uttara Bhadrapada, Revati
]

# Nadi: Aadi (Vata), Madhya (Pitta), Antya (Kapha) — Ayurvedic constitution
NAKSHATRA_NADI = [
    "Aadi", "Madhya", "Antya",   # Ashwini, Bharani, Krittika
    "Antya", "Madhya", "Aadi",   # Rohini, Mrigashira, Ardra
    "Aadi", "Madhya", "Antya",   # Punarvasu, Pushya, Ashlesha
    "Antya", "Madhya", "Aadi",   # Magha, Purva Phalguni, Uttara Phalguni
    "Aadi", "Madhya", "Antya",   # Hasta, Chitra, Swati
    "Antya", "Madhya", "Aadi",   # Vishakha, Anuradha, Jyeshtha
    "Aadi", "Madhya", "Antya",   # Mula, Purva Ashadha, Uttara Ashadha
    "Antya", "Madhya", "Aadi",   # Shravana, Dhanishta, Shatabhisha
    "Aadi", "Madhya", "Antya"    # Purva Bhadrapada, Uttara Bhadrapada, Revati
]

# Rule 2: Basic Planet Friendships (Nausargika Karakas / Natural Relationships)
# This is a simplified version for demonstration.
PLANETARY_RELATIONSHIPS = {
    "Sun": {"Friends": ["Moon", "Mars", "Jupiter"], "Enemies": ["Venus", "Saturn", "Rahu", "Ketu"], "Neutral": ["Mercury"]},
    "Moon": {"Friends": ["Sun", "Mercury"], "Enemies": ["Rahu", "Ketu"], "Neutral": ["Mars", "Jupiter", "Venus", "Saturn"]},
    "Mars": {"Friends": ["Sun", "Moon", "Jupiter"], "Enemies": ["Mercury", "Rahu"], "Neutral": ["Venus", "Saturn", "Ketu"]},
    "Mercury": {"Friends": ["Sun", "Venus"], "Enemies": ["Moon"], "Neutral": ["Mars", "Jupiter", "Saturn", "Rahu", "Ketu"]},
    "Jupiter": {"Friends": ["Sun", "Moon", "Mars"], "Enemies": ["Mercury", "Venus"], "Neutral": ["Saturn", "Rahu", "Ketu"]},
    "Venus": {"Friends": ["Mercury", "Saturn"], "Enemies": ["Sun", "Moon"], "Neutral": ["Mars", "Jupiter", "Rahu", "Ketu"]},
    "Saturn": {"Friends": ["Mercury", "Venus", "Rahu"], "Enemies": ["Sun", "Moon", "Mars"], "Neutral": ["Jupiter", "Ketu"]},
    "Rahu": {"Friends": ["Jupiter", "Venus", "Saturn"], "Enemies": ["Sun", "Moon", "Mars"], "Neutral": ["Mercury", "Ketu"]},
    "Ketu": {"Friends": ["Mars", "Venus", "Saturn"], "Enemies": ["Sun", "Moon"], "Neutral": ["Mercury", "Jupiter", "Rahu"]}
}

# House Classifications
HOUSE_TYPES = {
    "Kendra": [1, 4, 7, 10],   # Quadrants (Action/Pillars)
    "Trikona": [1, 5, 9],      # Trines (Luck/Dharma)
    "Dusthana": [6, 8, 12],    # Difficult Houses (Obstacles/Hidden)
    "Upachaya": [3, 6, 10, 11] # Houses of Growth
}

# Aspects (Drishti)
# Every planet aspects the 7th house from itself. Some have special aspects.
SPECIAL_ASPECTS = {
    "Mars": [4, 7, 8],
    "Jupiter": [5, 7, 9],
    "Saturn": [3, 7, 10],
    "Rahu": [5, 7, 9],
    "Ketu": [5, 7, 9],
    "Sun": [7],
    "Moon": [7],
    "Mercury": [7],
    "Venus": [7]
}

# ============================================================
# ADVANCED JYOTISH CONSTANTS
# ============================================================

# Moolatrikona Signs — a dignity between Exaltation and Own Sign
# Format: planet -> (sign_number, degree_start, degree_end) in the sign
MOOLATRIKONA_SIGNS = {
    "Sun": 5,        # Leo (0-20°)
    "Moon": 2,       # Taurus (4-20°)
    "Mars": 1,       # Aries (0-12°)
    "Mercury": 6,    # Virgo (16-20°)
    "Jupiter": 9,    # Sagittarius (0-10°)
    "Venus": 7,      # Libra (0-15°)
    "Saturn": 11     # Aquarius (0-20°)
}

# Own Signs — signs a planet rules (each planet owns 1 or 2 signs)
OWN_SIGNS = {
    "Sun": [5],              # Leo
    "Moon": [4],             # Cancer
    "Mars": [1, 8],          # Aries, Scorpio
    "Mercury": [3, 6],       # Gemini, Virgo
    "Jupiter": [9, 12],      # Sagittarius, Pisces
    "Venus": [2, 7],         # Taurus, Libra
    "Saturn": [10, 11],      # Capricorn, Aquarius
    "Rahu": [11],            # Aquarius (co-lord, commonly accepted)
    "Ketu": [8]              # Scorpio (co-lord, commonly accepted)
}

# Dig Bala (Directional Strength) — the house where a planet gains maximum strength
DIG_BALA = {
    "Sun": 10,       # 10th House (Midheaven)
    "Mars": 10,      # 10th House
    "Jupiter": 1,    # 1st House (Ascendant)
    "Mercury": 1,    # 1st House
    "Moon": 4,       # 4th House (IC / Nadir)
    "Venus": 4,      # 4th House
    "Saturn": 7,     # 7th House (Descendant)
    "Rahu": 10,      # 10th House (commonly accepted)
    "Ketu": 4        # 4th House (commonly accepted)
}

# Natural Benefics and Malefics
NATURAL_BENEFICS = ["Jupiter", "Venus", "Mercury", "Moon"]
NATURAL_MALEFICS = ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]

# Naisargika Karaka (Natural Significators)
# Each planet is the permanent significator for certain life themes.
KARAKA_PLANETS = {
    "Sun": {"karaka": "Atma Karaka", "signifies": "Soul, Father, Authority, Government, Vitality"},
    "Moon": {"karaka": "Manas Karaka", "signifies": "Mind, Mother, Emotions, Public, Nourishment"},
    "Mars": {"karaka": "Bhatri Karaka", "signifies": "Siblings, Courage, Land, Energy, Conflict"},
    "Mercury": {"karaka": "Vidya Karaka", "signifies": "Intelligence, Speech, Commerce, Learning, Communication"},
    "Jupiter": {"karaka": "Putra/Dhana Karaka", "signifies": "Children, Wisdom, Wealth, Dharma, Expansion"},
    "Venus": {"karaka": "Kalatra Karaka", "signifies": "Spouse, Love, Beauty, Luxury, Art, Vehicles"},
    "Saturn": {"karaka": "Ayush Karaka", "signifies": "Longevity, Discipline, Karma, Suffering, Service"},
    "Rahu": {"karaka": "Paternal Grandfather", "signifies": "Obsession, Foreign, Illusion, Unconventional, Technology"},
    "Ketu": {"karaka": "Maternal Grandfather", "signifies": "Moksha, Detachment, Mysticism, Past Life, Spirituality"}
}

# Manglik (Kuja) Dosha — Mars in these houses from Lagna or Moon causes the defect
MANGLIK_HOUSES = [1, 2, 4, 7, 8, 12]

# Convenience lists derived from HOUSE_TYPES
KENDRA_HOUSES = [1, 4, 7, 10]
TRIKONA_HOUSES = [1, 5, 9]
DUSTHANA_HOUSES = [6, 8, 12]
UPACHAYA_HOUSES = [3, 6, 10, 11]

# Panch Mahapurusha — which planet forms which yoga
PANCH_MAHAPURUSHA = {
    "Mars": "Ruchaka Yoga",
    "Mercury": "Bhadra Yoga",
    "Jupiter": "Hamsa Yoga",
    "Venus": "Malavya Yoga",
    "Saturn": "Shasha Yoga"
}

# Elements of Zodiac Signs
SIGN_ELEMENTS = {
    "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
    "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
    "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
    "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
}

# Pushkara Navamsa (Auspicious D9 portions)
# Format: Element -> List of auspicious Navamsa indices (1-9) within the sign
PUSHKARA_NAVAMSA_INDICES = {
    "Fire": [7, 9],    # 7th (Libra) & 9th (Sagittarius) Navamsa
    "Earth": [3, 5],   # 3rd (Pisces) & 5th (Taurus) Navamsa
    "Air": [6, 8],     # 6th (Taurus) & 8th (Pisces) Navamsa
    "Water": [1, 3]    # 1st (Cancer) & 3rd (Virgo) Navamsa
}

# ============================================================
# KP (KRISHNAMURTI PADDHATI) CONSTANTS
# ============================================================

# KP House Groups — for each life query, which houses are favorable/unfavorable
# Based on KP Readers and standard KP house signification rules
KP_HOUSE_GROUPS = {
    "marriage": {
        "favorable": [2, 7, 11],
        "unfavorable": [1, 6, 10, 12],
        "description": "Marriage is promised if the sub-lord of the 7th cusp signifies houses 2, 7, and 11."
    },
    "profession": {
        "favorable": [2, 6, 10],
        "unfavorable": [1, 5, 9, 12],
        "description": "Professional success if the sub-lord of the 10th cusp signifies houses 2, 6, and 10."
    },
    "wealth": {
        "favorable": [1, 2, 3, 6, 10, 11],
        "unfavorable": [5, 8, 12],
        "description": "Wealth accumulation if the sub-lord of the 2nd cusp signifies houses 2, 6, 10, 11."
    },
    "children": {
        "favorable": [2, 5, 11],
        "unfavorable": [1, 4, 10],
        "description": "Children are promised if the sub-lord of the 5th cusp signifies houses 2, 5, and 11."
    },
    "education": {
        "favorable": [4, 9, 11],
        "unfavorable": [3, 8, 12],
        "description": "Higher education success if the sub-lord of the 9th cusp signifies houses 4, 9, and 11."
    },
    "foreign_travel": {
        "favorable": [3, 9, 12],
        "unfavorable": [4, 8, 11],
        "description": "Foreign travel if the sub-lord of the 12th cusp signifies houses 3, 9, and 12."
    },
    "foreign_settlement": {
        "favorable": [9, 12],
        "unfavorable": [2, 4, 11],
        "description": "Foreign settlement if the sub-lord of the 12th cusp connects houses 9 and 12."
    },
    "health": {
        "favorable": [1, 5, 11],
        "unfavorable": [6, 8, 12],
        "description": "Good health if the sub-lord of the 1st cusp signifies houses 1, 5, 11."
    },
    "longevity": {
        "favorable": [1, 3, 8],
        "unfavorable": [2, 7, 12],
        "description": "Longevity depends on the sub-lord of the 8th cusp and its significations."
    },
    "property": {
        "favorable": [4, 11, 12],
        "unfavorable": [3, 5, 10],
        "description": "Property acquisition if the sub-lord of the 4th cusp signifies houses 4, 11, 12."
    },
    "litigation": {
        "favorable": [6, 11],
        "unfavorable": [1, 12],
        "description": "Success in litigation if the sub-lord of the 6th cusp signifies houses 6 and 11."
    },
    "vehicle": {
        "favorable": [4, 11],
        "unfavorable": [3, 5, 12],
        "description": "Vehicle acquisition if the sub-lord of the 4th cusp signifies houses 4 and 11."
    },
    "spiritual_progress": {
        "favorable": [5, 9, 12],
        "unfavorable": [1, 6, 10],
        "description": "Spiritual progress if the sub-lord of the 9th cusp signifies houses 5, 9, and 12."
    },
    "business_partnership": {
        "favorable": [3, 7, 10, 11],
        "unfavorable": [5, 6, 12],
        "description": "Business success if the sub-lord of the 7th cusp signifies houses 7, 10, and 11."
    },
    "government_job": {
        "favorable": [2, 6, 10, 11],
        "unfavorable": [1, 5, 9],
        "description": "Government job if the sub-lord of the 10th cusp signifies houses 6, 10, and 11."
    }
}

# Ruling Planet Day Lords — which planet rules each day of the week
# Used in the 5-fold Ruling Planet system
RULING_PLANET_DAY_LORDS = {
    0: "Moon",      # Monday
    1: "Mars",      # Tuesday
    2: "Mercury",   # Wednesday
    3: "Jupiter",   # Thursday
    4: "Venus",     # Friday
    5: "Saturn",    # Saturday
    6: "Sun"        # Sunday
}

# Sign Number to Sign Name (reverse lookup)
SIGN_NAMES = {
    1: "Aries", 2: "Taurus", 3: "Gemini", 4: "Cancer",
    5: "Leo", 6: "Virgo", 7: "Libra", 8: "Scorpio",
    9: "Sagittarius", 10: "Capricorn", 11: "Aquarius", 12: "Pisces"
}

# Nakshatra lords in order (repeating Vimshottari sequence 3 times for 27 nakshatras)
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",  # Ashwini-Ashlesha
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",  # Magha-Jyeshtha
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"   # Mula-Revati
]
