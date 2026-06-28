# A foundational mapping of Astrological Placements to their classical meanings.
# This serves as the ground truth before passing to an AI model for styling.

INTERPRETATIONS_DB = {
    # General Placements of Planets in Houses
    "planet_in_house": {
        "Sun": {
            1: "Strong willpower, commanding personality, prone to ego.",
            4: "Success through real estate or mother's influence, but inner restlessness.",
            7: "May seek a dominant partner, potential for ego clashes in marriage.",
            10: "Excellent for career, natural leadership, authority."
        },
        "Moon": {
            1: "Emotional, intuitive, deeply influenced by surroundings.",
            4: "Deep attachment to home and mother, emotional security is paramount.",
            7: "Seeks emotional fulfillment through partnership, empathetic spouse.",
            12: "Vivid imagination, requires spiritual or solitary retreats to recharge."
        },
        "Mars": {
            1: "High energy, aggressive, athletic, prone to head injuries.",
            4: "Manglik defect from 4th house. Drive to acquire property, possible domestic friction.",
            7: "Manglik defect. Passionate but potentially combative partnerships.",
            10: "Highly ambitious, 'go-getter' attitude. Excellent for engineering, police, or military careers."
        },
        "Jupiter": {
            1: "Optimistic, philosophical, physically healthy, protective aura.",
            2: "Expansion of wealth and family. Truthful and philosophical speech.",
            7: "Blessed partnerships, philosophical or religious spouse.",
            10: "Respect in society, career related to teaching, law, or advising."
        },
        "Venus": {
            1: "Charming, attractive, loves luxury and harmony.",
            2: "Loves comfortable living, earns through artistic or diplomatic means.",
            7: "Beautiful and charming spouse, strong desire for harmony in marriage.",
            12: "Enjoys foreign travels, loves private luxuries and romance."
        },
        "Saturn": {
            1: "Serious demeanor, slow but steady growth, heavily disciplined.",
            3: "Hard worker, disciplined efforts, steady relationship with siblings.",
            7: "Delay in marriage or an older, mature spouse. Requires commitment.",
            10: "Career requires immense hard work. Success comes later in life."
        },
        "Mercury": {
            1: "Talkative, youthful appearance, highly analytical.",
            5: "Highly intelligent, creative, good at speculation and writing.",
            10: "Career in communications, IT, writing, or analytics.",
            12: "Restless mind, good for research or spiritual studies behind the scenes."
        },
        "Rahu": {
            1: "Strong desire for worldly success, unconventional personality.",
            7: "Unconventional marriage, spouse from different cultural background.",
            10: "Massive thirst for career success, highly ambitious, uses out-of-the-box methods."
        },
        "Ketu": {
            1: "Spiritual, detached, often feels 'out of place' in worldly matters.",
            7: "Detachment from partnerships, spouse may be highly spiritual or distant.",
            12: "Excellent for Moksha (liberation), deep spiritual experiences, foreign lands."
        }
    },
    
    # Lord Placements: Where the ruler of a house goes
    "lord_in_house": {
        7: { # 7th Lord (Marriage/Partnerships)
            1: "Spouse strongly influences your path in life.",
            4: "Spouse brings domestic stability or property.",
            7: "Spouse is strong, independent, and supportive.",
            9: "Marriage brings luck, travel, or spiritual growth.",
            10: "Spouse is career-oriented; marriage boosts your status.",
            12: "Spouse may be from a foreign land or marriage requires spiritual sacrifice."
        },
        10: { # 10th Lord (Career)
            1: "You are a self-made person. Career is your identity.",
            5: "Career through creativity, education, or intelligence.",
            9: "Career brings long-distance travel. Fortune favors professional life.",
            11: "Tremendous gains and networking through career."
        }
    }
}

# Detailed House Descriptions — what each house signifies
HOUSE_DESCRIPTIONS = {
    1: {
        "name": "Lagna (Ascendant)",
        "domain": "Self, Body, Personality",
        "description": "The 1st house is the most personal house. It represents your physical appearance, overall health, vitality, temperament, and the lens through which you perceive the world. It is the foundation of your entire chart — the mask you wear and the first impression you leave."
    },
    2: {
        "name": "Dhana Bhava",
        "domain": "Wealth, Speech, Family",
        "description": "The 2nd house governs accumulated wealth, family lineage, food habits, and the quality of your speech. It shows your relationship with money, savings, and the values instilled by your upbringing. A strong 2nd house indicates financial security and a sweet, persuasive voice."
    },
    3: {
        "name": "Sahaja Bhava",
        "domain": "Courage, Siblings, Communication",
        "description": "The 3rd house rules your courage, willpower, short travels, younger siblings, and all forms of communication — writing, media, and self-expression. It is the house of effort and determination, showing how boldly you pursue your desires."
    },
    4: {
        "name": "Sukha Bhava",
        "domain": "Home, Mother, Emotional Peace",
        "description": "The 4th house represents your home environment, mother, domestic comforts, vehicles, land, and inner emotional peace. It is the foundation of your private life — where you retreat for comfort and security. A strong 4th house indicates a peaceful, happy domestic life."
    },
    5: {
        "name": "Putra Bhava",
        "domain": "Children, Intelligence, Romance",
        "description": "The 5th house governs children, creative intelligence, romance, speculative gains (stocks, gambling), and past-life merit (Purva Punya). It is the house of joy, artistic talent, and the mind's capacity for original thought and learning."
    },
    6: {
        "name": "Ripu/Rog Bhava",
        "domain": "Enemies, Disease, Service",
        "description": "The 6th house rules over enemies, debts, diseases, daily work routines, and service to others. While classified as a Dusthana (difficult house), a strong 6th house actually means you overcome obstacles, defeat competitors, and maintain robust health through discipline."
    },
    7: {
        "name": "Kalatra Bhava",
        "domain": "Marriage, Partnerships, Business",
        "description": "The 7th house is the house of the spouse and all one-to-one partnerships — romantic, business, and legal. It shows the nature of your life partner, the quality of your marriage, and your ability to form meaningful alliances. It directly opposes the 1st house (Self vs. Other)."
    },
    8: {
        "name": "Ayu Bhava",
        "domain": "Longevity, Transformation, Occult",
        "description": "The 8th house governs longevity, sudden events, inheritance, insurance, joint finances with spouse, and deep transformation. It is the house of mystery — covering the occult, tantra, death and rebirth cycles, chronic illness, and hidden knowledge."
    },
    9: {
        "name": "Dharma Bhava",
        "domain": "Father, Fortune, Higher Learning",
        "description": "The 9th house is the most auspicious house (Bhagya Sthana). It rules your father, guru, luck, long-distance travel, higher education, philosophy, religion, and dharma (life purpose). Planets here bring blessings, spiritual wisdom, and fortune in life."
    },
    10: {
        "name": "Karma Bhava",
        "domain": "Career, Public Image, Authority",
        "description": "The 10th house is the midheaven of the chart — your career, public reputation, professional achievements, and relationship with authority figures. It shows how the world sees you, your ambitions, and your contribution to society. The strongest Kendra house."
    },
    11: {
        "name": "Labha Bhava",
        "domain": "Gains, Networks, Aspirations",
        "description": "The 11th house governs your income and gains, fulfillment of desires, social networks, elder siblings, and large organizations. It is the house of abundance — showing how your ambitions materialize into tangible rewards and the quality of your social circle."
    },
    12: {
        "name": "Vyaya Bhava",
        "domain": "Loss, Foreign Lands, Moksha",
        "description": "The 12th house rules expenditure, losses, foreign residence, isolation, hospitalization, sleep quality, and spiritual liberation (Moksha). It is the house of endings and surrender — showing where you let go, what drains your energy, and your connection to the subconscious and the divine."
    }
}

# Gana Personality Descriptions
GANA_DESCRIPTIONS = {
    "Deva": "Deva Gana individuals are noble, generous, and dharmic by nature. They have a natural inclination toward righteousness, are generally well-mannered, and prefer peaceful resolution of conflicts. They are drawn to spirituality and higher learning.",
    "Manushya": "Manushya Gana individuals are practical, ambitious, and balanced. They possess a mix of material desires and moral values. They are highly adaptable, driven by worldly goals, and navigate both spiritual and material worlds comfortably.",
    "Rakshasa": "Rakshasa Gana individuals are fiercely independent, determined, and unconventional. They possess immense willpower and are not afraid to challenge norms. Though often misunderstood, they are protective of their loved ones and have a deep inner strength."
}

# Varna Descriptions
VARNA_DESCRIPTIONS = {
    "Brahmin": "The Brahmin Varna signifies an intellectual and spiritually inclined nature. These individuals excel in teaching, research, writing, and advisory roles. They are natural thinkers and seekers of knowledge.",
    "Kshatriya": "The Kshatriya Varna signifies courage, leadership, and a protective nature. These individuals thrive in positions of authority — military, politics, management, and competitive fields. They are decisive and action-oriented.",
    "Vaishya": "The Vaishya Varna signifies a commercial and enterprising spirit. These individuals are skilled in trade, finance, agriculture, and business. They have a natural talent for wealth creation and resource management.",
    "Shudra": "The Shudra Varna signifies a service-oriented and hardworking nature. These individuals are the backbone of any community — skilled craftsmen, artisans, and dedicated workers. They find fulfillment in tangible, hands-on contribution."
}

# Yoni Descriptions
YONI_DESCRIPTIONS = {
    "Horse": "Swift, energetic, and freedom-loving. You value independence and have a restless spirit that drives you to explore.",
    "Elephant": "Regal, wise, and patient. You carry yourself with dignity and possess immense inner strength and endurance.",
    "Goat": "Gentle, nurturing, and community-oriented. You are adaptable and find comfort in familiar surroundings.",
    "Serpent": "Intense, magnetic, and deeply intuitive. You possess a mysterious aura and powerful regenerative abilities.",
    "Dog": "Loyal, protective, and vigilant. You are fiercely devoted to those you love and have strong instincts.",
    "Cat": "Independent, graceful, and observant. You are self-sufficient, curious, and move through life with quiet elegance.",
    "Rat": "Resourceful, quick-witted, and industrious. You have a sharp mind and can thrive in any environment.",
    "Cow": "Gentle, generous, and stable. You provide nourishment and comfort to those around you with unwavering patience.",
    "Buffalo": "Strong, determined, and hardworking. You possess immense stamina and persevere through any hardship.",
    "Tiger": "Bold, fierce, and commanding. You have natural authority and a powerful presence that demands respect.",
    "Deer": "Graceful, alert, and aesthetic. You have refined tastes, a love for beauty, and a gentle yet cautious nature.",
    "Monkey": "Clever, playful, and adaptable. You have a sharp intellect, love variety, and excel at creative problem-solving.",
    "Mongoose": "Fearless, strategic, and decisive. You confront challenges head-on and possess remarkable survival instincts.",
    "Lion": "Proud, noble, and authoritative. You are a born leader with a commanding presence and generous spirit."
}

def get_planet_in_house_reading(planet: str, house: int) -> str:
    # Use a default fallback if reading is not strictly defined
    return INTERPRETATIONS_DB["planet_in_house"].get(planet, {}).get(house, f"{planet} is placed in House {house}. This affects the themes of this house dynamically.")

def get_lord_in_house_reading(lord_house: int, placement_house: int) -> str:
    return INTERPRETATIONS_DB["lord_in_house"].get(lord_house, {}).get(placement_house, f"The lord of house {lord_house} is in house {placement_house}, linking these two areas of life.")

def get_house_description(house: int) -> dict:
    return HOUSE_DESCRIPTIONS.get(house, {"name": f"House {house}", "domain": "General", "description": f"House {house} governs specific areas of life."})

def get_gana_description(gana: str) -> str:
    return GANA_DESCRIPTIONS.get(gana, "")

def get_varna_description(varna: str) -> str:
    return VARNA_DESCRIPTIONS.get(varna, "")

def get_yoni_description(yoni: str) -> str:
    return YONI_DESCRIPTIONS.get(yoni, "")

# ============================================================
# ADVANCED YOGA & DOSHA DESCRIPTIONS
# ============================================================

YOGA_DESCRIPTIONS = {
    # Panch Mahapurusha Yogas
    "Ruchaka Yoga": "Formed by Mars in own/exalted sign in a Kendra. Grants a warrior's physique, immense courage, leadership in military or sports, and commanding authority. The native is fearless and decisive.",
    "Bhadra Yoga": "Formed by Mercury in own/exalted sign in a Kendra. Grants sharp intellect, eloquent speech, success in business and communication, and a youthful, attractive appearance. The native excels in analysis and trade.",
    "Hamsa Yoga": "Formed by Jupiter in own/exalted sign in a Kendra. Grants wisdom, spiritual depth, high moral character, success in teaching or advisory roles, and widespread respect. The native is a natural counselor.",
    "Malavya Yoga": "Formed by Venus in own/exalted sign in a Kendra. Grants beauty, artistic talent, luxurious lifestyle, harmonious relationships, and refined taste. The native attracts comfort and pleasure naturally.",
    "Shasha Yoga": "Formed by Saturn in own/exalted sign in a Kendra. Grants authority through discipline, success in politics or large organizations, strong work ethic, and eventual rise to power through persistence.",

    # Wealth & Power Yogas
    "Dhana Yoga": "Formed when lords of wealth-giving houses (1, 2, 5, 9, 11) are connected. Indicates strong potential for financial prosperity, inheritance, and material abundance through intelligent effort.",
    "Raja Yoga (Conjunction)": "Formed when a Kendra lord and a Trikona lord conjunct. This is the classical formula for power, authority, and social elevation. The native rises above their circumstances.",
    "Raja Yoga (Parivartana)": "Formed when Kendra and Trikona lords exchange houses. A powerful mutual exchange that links fortune with action, producing sustained success and recognition.",
    "Yoga Karaka": "When one planet lords both a Kendra and a Trikona house for a given Ascendant, it becomes a Yoga Karaka — the single most beneficial planet in the chart. Its periods bring extraordinary results.",

    # Viparita Raja Yogas
    "Harsha Viparita Raja Yoga": "Lord of the 6th in another Dusthana. The native overcomes enemies, diseases, and debts with unusual ease, often turning competitive situations into victories.",
    "Sarala Viparita Raja Yoga": "Lord of the 8th in another Dusthana. The native handles crises, transformations, and hidden matters with remarkable resilience. Gains through insurance, inheritance, or occult knowledge.",
    "Vimala Viparita Raja Yoga": "Lord of the 12th in another Dusthana. The native minimizes losses and expenditure, often gaining from foreign connections, spiritual pursuits, or charitable work.",

    # Cancellation & Reversal
    "Neecha Bhanga Raja Yoga": "Debilitation of a planet is cancelled through specific classical conditions. What was the weakest point in the chart transforms into a source of extraordinary strength, resilience, and eventual triumph.",

    # Sun Yogas
    "Veshi Yoga": "Planet(s) in the 2nd house from the Sun. Enhances the native's reputation, self-expression, and ability to take initiative. Brings material comfort and social standing.",
    "Vashi Yoga": "Planet(s) in the 12th house from the Sun. Enhances the native's influence, charisma, and ability to work behind the scenes. Grants magnetic personality.",
    "Ubhayachari Yoga": "Planets on both sides of the Sun (2nd and 12th). Creates a protective aura around the native. Indicates a well-rounded personality with both initiative and influence.",

    # Moon Yogas
    "Kemadurma Yoga": "No planets in the 2nd or 12th from the Moon. Can indicate periods of emotional isolation, financial struggle, or lack of support. Effect is reduced if Moon is in Kendra or aspected by benefics.",
    "Chandra-Mangal Yoga": "Moon and Mars conjunct. Indicates strong earning potential through courage, real estate, agriculture, or bold enterprise. The native is emotionally driven toward material achievement.",
    "Gajakesari Yoga": "Jupiter and Moon conjunct or in mutual Kendras. One of the most celebrated yogas — grants widespread respect, wisdom, prosperity, and noble character.",

    # Character Yoga
    "Amala Yoga (from Lagna)": "Natural benefic in the 10th from Lagna. Indicates a person of spotless character, noble profession, and public respect. The career is aligned with dharmic values.",
    "Amala Yoga (from Moon)": "Natural benefic in the 10th from Moon. Noble conduct, emotional maturity in professional dealings, and public admiration."
}

DOSHA_DESCRIPTIONS = {
    "Manglik (Kuja) Dosha": "Mars in houses 1, 2, 4, 7, 8, or 12 from Lagna or Moon creates Manglik Dosha. Primarily affects marriage and partnership dynamics — can cause delays, arguments, or incompatibility if not matched properly. Severity varies; many cancellation conditions exist (Mars in own/exalted sign, Jupiter's aspect, etc.).",
    "Kaal Sarp Dosha": "All seven planets hemmed between the Rahu-Ketu axis. Creates a pattern of karmic intensity — the native may experience recurring obstacles, delays, and sudden reversals, but also possesses immense spiritual potential. The struggle often leads to extraordinary transformation.",
    "Sade Sati": "Saturn transiting the 12th, 1st, and 2nd signs from the natal Moon over ~7.5 years. A period of deep karmic testing — challenges in career, relationships, and health. However, it also builds resilience, maturity, and lasting wisdom. Results depend heavily on Saturn's natal dignity."
}

def get_yoga_description(yoga_name: str) -> str:
    """Returns the detailed description for a given yoga name."""
    return YOGA_DESCRIPTIONS.get(yoga_name, f"{yoga_name}: A classical Vedic combination influencing the native's life path.")

def get_dosha_description(dosha_name: str) -> str:
    """Returns the detailed description for a given dosha name."""
    return DOSHA_DESCRIPTIONS.get(dosha_name, f"{dosha_name}: A Vedic astrological defect requiring analysis.")

