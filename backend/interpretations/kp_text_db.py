"""
KP (Krishnamurti Paddhati) Text Database — KP-specific interpretations.

Replaces text_db.py for KP-mode predictions. Focused on:
1. Cusp Sub-Lord result descriptions
2. House Group Significations for life queries
3. Planet as Significator descriptions
"""

# ============================================================
# 1. CUSP SUB-LORD RESULTS
# ============================================================

# What happens when the sub-lord of a cusp signifies certain houses
CUSP_SUBLORD_RESULTS = {
    1: {  # Ascendant
        "favorable": "The sub-lord of the 1st cusp signifying houses 1, 5, 11 indicates good health, vitality, and overall well-being. The native has a strong constitution and recovers quickly from illness.",
        "unfavorable": "The sub-lord of the 1st cusp signifying houses 6, 8, 12 indicates health challenges, a tendency toward chronic ailments, and periods of physical weakness.",
        "description": "The 1st cusp sub-lord determines overall health, longevity, and the native's general approach to life."
    },
    2: {  # Wealth
        "favorable": "The sub-lord of the 2nd cusp signifying houses 2, 6, 10, 11 indicates steady income, wealth accumulation, and financial security through profession and service.",
        "unfavorable": "The sub-lord of the 2nd cusp signifying houses 5, 8, 12 indicates financial losses through speculation, unexpected events, or excessive spending.",
        "description": "The 2nd cusp sub-lord determines wealth, family harmony, and quality of speech."
    },
    3: {  # Courage & Siblings
        "favorable": "The sub-lord of the 3rd cusp signifying houses 3, 9, 11 indicates courage, successful short journeys, good relations with siblings, and communication skills.",
        "unfavorable": "The sub-lord of the 3rd cusp signifying houses 8, 12 indicates lack of initiative, strained relationships with siblings, and obstacles in communication.",
        "description": "The 3rd cusp sub-lord determines courage, siblings, short travels, and self-expression."
    },
    4: {  # Home & Property
        "favorable": "The sub-lord of the 4th cusp signifying houses 4, 11, 12 indicates acquisition of property, vehicles, domestic harmony, and academic success.",
        "unfavorable": "The sub-lord of the 4th cusp signifying houses 3, 5, 10 indicates difficulty in acquiring property, domestic disturbances, and frequent relocations.",
        "description": "The 4th cusp sub-lord determines home, mother, vehicles, and emotional peace."
    },
    5: {  # Children & Intelligence
        "favorable": "The sub-lord of the 5th cusp signifying houses 2, 5, 11 indicates children are promised, creative intelligence, gains through speculation, and romantic fulfillment.",
        "unfavorable": "The sub-lord of the 5th cusp signifying houses 1, 4, 10 indicates delays or denial of children, losses in speculation, and disappointment in romance.",
        "description": "The 5th cusp sub-lord determines children, intelligence, romance, and speculative gains."
    },
    6: {  # Health Issues & Service
        "favorable": "The sub-lord of the 6th cusp signifying houses 6, 11 indicates victory over enemies, success in competitive exams, and ability to overcome debt and disease.",
        "unfavorable": "The sub-lord of the 6th cusp signifying houses 1, 12 indicates vulnerability to enemies, prolonged illness, and difficulty in clearing debts.",
        "description": "The 6th cusp sub-lord determines enemies, disease, debts, and service."
    },
    7: {  # Marriage
        "favorable": "The sub-lord of the 7th cusp signifying houses 2, 7, 11 indicates marriage is PROMISED. The native will find a suitable partner, and the marriage will bring gains and fulfillment.",
        "unfavorable": "The sub-lord of the 7th cusp signifying houses 1, 6, 10, 12 indicates delays, denial, or difficulties in marriage. Separation tendencies may exist.",
        "description": "The 7th cusp sub-lord determines marriage, partnerships, and all one-to-one relationships."
    },
    8: {  # Longevity
        "favorable": "The sub-lord of the 8th cusp signifying houses 1, 3, 8 indicates long life, inheritance, and the ability to handle sudden transformations with resilience.",
        "unfavorable": "The sub-lord of the 8th cusp signifying houses 2, 7, 12 indicates potential for health crises, financial losses through partners, and karmic challenges.",
        "description": "The 8th cusp sub-lord determines longevity, sudden events, inheritance, and transformation."
    },
    9: {  # Fortune & Higher Learning
        "favorable": "The sub-lord of the 9th cusp signifying houses 4, 9, 11 indicates higher education success, long-distance travel, spiritual growth, and exceptional fortune.",
        "unfavorable": "The sub-lord of the 9th cusp signifying houses 3, 8, 12 indicates obstacles in higher education, difficulties in travel, and strained relations with father/guru.",
        "description": "The 9th cusp sub-lord determines fortune, father, higher learning, and spiritual progress."
    },
    10: {  # Career
        "favorable": "The sub-lord of the 10th cusp signifying houses 2, 6, 10 indicates professional success, steady career growth, recognition, and good standing in society.",
        "unfavorable": "The sub-lord of the 10th cusp signifying houses 1, 5, 9, 12 indicates career instability, frequent job changes, lack of recognition, or involuntary retirement.",
        "description": "The 10th cusp sub-lord determines profession, public reputation, and career achievements."
    },
    11: {  # Gains & Aspirations
        "favorable": "The sub-lord of the 11th cusp signifying houses 2, 6, 10, 11 indicates fulfillment of desires, steady income, large social network, and successful investments.",
        "unfavorable": "The sub-lord of the 11th cusp signifying houses 5, 8, 12 indicates unfulfilled ambitions, disappointing gains, and unreliable social connections.",
        "description": "The 11th cusp sub-lord determines gains, income fulfillment, and realization of aspirations."
    },
    12: {  # Foreign & Spiritual
        "favorable": "The sub-lord of the 12th cusp signifying houses 3, 9, 12 indicates foreign travel and settlement, spiritual liberation, and meaningful solitude.",
        "unfavorable": "The sub-lord of the 12th cusp signifying houses 2, 4, 11 indicates wasteful expenditure, inability to settle abroad, and loss of domestic peace.",
        "description": "The 12th cusp sub-lord determines foreign lands, expenses, losses, and spiritual liberation."
    }
}

# ============================================================
# 2. HOUSE GROUP SIGNIFICATIONS
# ============================================================

LIFE_QUERY_DESCRIPTIONS = {
    "marriage": {
        "title": "Marriage & Partnership",
        "primary_cusp": 7,
        "favorable_houses": [2, 7, 11],
        "unfavorable_houses": [1, 6, 10, 12],
        "explanation": "For marriage to be promised, the sub-lord of the 7th cusp must be a significator of houses 2 (family addition), 7 (partnership), and 11 (fulfillment). If the sub-lord connects to 1 (self over partner), 6 (enmity/separation), or 12 (loss), marriage faces obstacles.",
        "timing": "Marriage timing: Look for Dasha/Bhukti lords who are significators of 2, 7, 11 and also appear as Ruling Planets."
    },
    "profession": {
        "title": "Career & Profession",
        "primary_cusp": 10,
        "favorable_houses": [2, 6, 10],
        "unfavorable_houses": [1, 5, 9, 12],
        "explanation": "For career success, the sub-lord of the 10th cusp must signify houses 2 (income), 6 (service/daily work), and 10 (profession/status). Houses 5, 9 point to leaving service (5, 9 are 12th from 6, 10).",
        "timing": "Career changes occur during Dasha/Bhukti of significators of 2, 6, 10 filtered by Ruling Planets."
    },
    "wealth": {
        "title": "Wealth & Finance",
        "primary_cusp": 2,
        "favorable_houses": [1, 2, 3, 6, 10, 11],
        "unfavorable_houses": [5, 8, 12],
        "explanation": "Wealth accumulates when the sub-lord of the 2nd cusp connects to income houses (2, 6, 10, 11). Houses 5 (speculation loss), 8 (sudden loss), 12 (expenditure) work against wealth.",
        "timing": "Wealth comes during Dasha/Bhukti of significators of 2, 11 filtered by Ruling Planets."
    },
    "children": {
        "title": "Children & Progeny",
        "primary_cusp": 5,
        "favorable_houses": [2, 5, 11],
        "unfavorable_houses": [1, 4, 10],
        "explanation": "Children are promised when the sub-lord of the 5th cusp signifies 2 (family growth), 5 (children), and 11 (fulfillment of desire). Houses 4, 10 (being 12th from 5, 11) negate.",
        "timing": "Childbirth occurs during Dasha/Bhukti of significators of 2, 5, 11."
    },
    "education": {
        "title": "Higher Education",
        "primary_cusp": 9,
        "favorable_houses": [4, 9, 11],
        "unfavorable_houses": [3, 8, 12],
        "explanation": "Education success requires the sub-lord of the 9th cusp to signify 4 (basic education), 9 (higher learning), and 11 (success). Houses 3, 8, 12 denote failure or discontinuation.",
        "timing": "Education success periods: Dasha/Bhukti of significators of 4, 9, 11."
    },
    "foreign_travel": {
        "title": "Foreign Travel",
        "primary_cusp": 12,
        "favorable_houses": [3, 9, 12],
        "unfavorable_houses": [4, 8, 11],
        "explanation": "Foreign travel is indicated when the sub-lord of the 12th cusp connects to 3 (short journeys), 9 (long journeys), and 12 (foreign lands).",
        "timing": "Foreign trips happen during Dasha/Bhukti of significators of 3, 9, 12."
    },
    "health": {
        "title": "Health & Vitality",
        "primary_cusp": 1,
        "favorable_houses": [1, 5, 11],
        "unfavorable_houses": [6, 8, 12],
        "explanation": "Good health requires the sub-lord of the 1st cusp to signify 1 (vitality), 5 (recovery), and 11 (gain of health). Houses 6, 8, 12 indicate disease, surgery, or hospitalization.",
        "timing": "Health crises occur during Dasha/Bhukti of significators of 6, 8, 12."
    },
    "property": {
        "title": "Property & Real Estate",
        "primary_cusp": 4,
        "favorable_houses": [4, 11, 12],
        "unfavorable_houses": [3, 5, 10],
        "explanation": "Property acquisition requires the sub-lord of the 4th cusp to signify 4 (immovable property), 11 (fulfillment), and 12 (investment/expenditure for purchase).",
        "timing": "Property purchase occurs during Dasha/Bhukti of significators of 4, 11, 12."
    }
}

# ============================================================
# 3. PLANET AS SIGNIFICATOR DESCRIPTIONS
# ============================================================

PLANET_SIGNIFICATOR_DESCRIPTIONS = {
    "Sun": {
        "as_significator": "When Sun is the significator, results manifest through authority figures, government, father, and positions of power. The Sun activates matters with confidence and public visibility.",
        "strong": "A strong Sun as significator brings recognition, promotion, government favor, and vitality to the house affairs.",
        "weak": "A weak Sun as significator brings ego conflicts, problems with authority, issues with father, and loss of reputation."
    },
    "Moon": {
        "as_significator": "When Moon is the significator, results manifest through emotional connections, mother, public, and change. The Moon activates matters with sensitivity and fluctuation.",
        "strong": "A strong Moon as significator brings popularity, emotional fulfillment, travel opportunities, and public support.",
        "weak": "A weak Moon as significator brings mental anxiety, instability, issues with mother, and public criticism."
    },
    "Mars": {
        "as_significator": "When Mars is the significator, results manifest through action, courage, property, and siblings. Mars activates matters with energy and decisiveness.",
        "strong": "A strong Mars as significator brings bold achievement, property gains, physical vitality, and victory over competition.",
        "weak": "A weak Mars as significator brings conflicts, accidents, property disputes, and strained relations with siblings."
    },
    "Mercury": {
        "as_significator": "When Mercury is the significator, results manifest through intelligence, communication, business, and education. Mercury activates matters with analytical precision.",
        "strong": "A strong Mercury as significator brings academic success, business profits, strong communication, and intellectual recognition.",
        "weak": "A weak Mercury as significator brings confusion, business losses, miscommunication, and educational setbacks."
    },
    "Jupiter": {
        "as_significator": "When Jupiter is the significator, results manifest through wisdom, expansion, children, and dharma. Jupiter activates matters with grace and abundance.",
        "strong": "A strong Jupiter as significator brings prosperity, spiritual growth, children, and guidance from mentors.",
        "weak": "A weak Jupiter as significator brings overconfidence, financial overextension, and unfulfilled hopes."
    },
    "Venus": {
        "as_significator": "When Venus is the significator, results manifest through relationships, beauty, luxury, and art. Venus activates matters with harmony and pleasure.",
        "strong": "A strong Venus as significator brings marital happiness, artistic success, financial gains, and comfortable living.",
        "weak": "A weak Venus as significator brings relationship issues, overindulgence, financial waste, and romantic disappointment."
    },
    "Saturn": {
        "as_significator": "When Saturn is the significator, results manifest through discipline, delay, karma, and hard work. Saturn activates matters slowly but permanently.",
        "strong": "A strong Saturn as significator brings lasting success through persistence, organizational power, and karmic rewards.",
        "weak": "A weak Saturn as significator brings delays, chronic problems, obstacles, and feelings of restriction."
    },
    "Rahu": {
        "as_significator": "When Rahu is the significator, results manifest through unconventional means, foreign connections, technology, and sudden events. Rahu activates matters with intensity and surprise.",
        "strong": "A strong Rahu as significator brings sudden gains, foreign opportunities, technological success, and breaking of barriers.",
        "weak": "A weak Rahu as significator brings deception, confusion, addictions, and entanglement in worldly illusions."
    },
    "Ketu": {
        "as_significator": "When Ketu is the significator, results manifest through spirituality, detachment, and sudden endings. Ketu activates matters by dissolving attachments.",
        "strong": "A strong Ketu as significator brings spiritual insight, liberation from problems, and psychic abilities.",
        "weak": "A weak Ketu as significator brings aimlessness, losses without reason, health issues, and karmic confusion."
    }
}

# ============================================================
# ACCESSOR FUNCTIONS
# ============================================================

def get_cusp_sublord_reading(house: int, is_favorable: bool) -> str:
    """Returns the cusp sub-lord interpretation for a house."""
    key = "favorable" if is_favorable else "unfavorable"
    return CUSP_SUBLORD_RESULTS.get(house, {}).get(key, f"House {house} sub-lord analysis pending.")

def get_cusp_description(house: int) -> str:
    """Returns the cusp description for KP analysis."""
    return CUSP_SUBLORD_RESULTS.get(house, {}).get("description", f"House {house} in KP system.")

def get_life_query_info(query: str) -> dict:
    """Returns full interpretation data for a life query."""
    return LIFE_QUERY_DESCRIPTIONS.get(query, {
        "title": query.replace("_", " ").title(),
        "explanation": f"Analysis for {query} based on KP house significations."
    })

def get_planet_significator_reading(planet: str, strength: str = "as_significator") -> str:
    """Returns what a planet signifies when it's a significator at any level."""
    return PLANET_SIGNIFICATOR_DESCRIPTIONS.get(planet, {}).get(
        strength, f"{planet} as a significator influences house affairs."
    )
