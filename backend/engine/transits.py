from datetime import datetime

class TransitEngine:
    """
    Calculates where the planets are currently (Transit Chart) 
    and overlays them onto a Natal Chart to generate daily/weekly deterministic insights.
    """
    
    def __init__(self, natal_chart: dict, current_positions: dict):
        self.natal_chart = natal_chart
        self.current_positions = current_positions
        
    def _get_house_for_degree(self, degree: float) -> int:
        """Determines which house a given degree falls into based on the natal KP cusps."""
        cusps = self.natal_chart.get("kp_cusps", {})
        if not cusps:
            # Fallback to whole sign houses if KP cusps are missing
            asc_sign = self.natal_chart.get("ascendant", {}).get("sign_number", 1)
            transit_sign = int(degree // 30) + 1
            house = (transit_sign - asc_sign) % 12 + 1
            return house

        # KP Cusp Logic
        # Houses are defined by Cusp 1 to Cusp 2, Cusp 2 to Cusp 3, etc.
        for h in range(1, 13):
            curr_cusp = cusps.get(str(h), {}).get("absolute_degree", 0)
            next_cusp = cusps.get(str((h % 12) + 1), {}).get("absolute_degree", 0)
            
            # Normal case (e.g., Cusp 1 at 10 deg, Cusp 2 at 40 deg)
            if curr_cusp < next_cusp:
                if curr_cusp <= degree < next_cusp:
                    return h
            else:
                # Wrap around 360 case (e.g., Cusp 12 at 350 deg, Cusp 1 at 20 deg)
                if degree >= curr_cusp or degree < next_cusp:
                    return h
                    
        return 1 # Fallback

    def generate_daily_insights(self) -> list:
        """
        Generates deterministic insights based on the current transit positions
        interacting with the user's natal chart.
        """
        insights = []
        
        # 1. Transit Moon (Daily Mood/Focus)
        moon_transit_deg = self.current_positions.get("Moon", {}).get("absolute_degree")
        if moon_transit_deg is not None:
            moon_house = self._get_house_for_degree(moon_transit_deg)
            insights.append(self._get_moon_transit_insight(moon_house))
            
        # 2. Transit Sun (Monthly Theme)
        sun_transit_deg = self.current_positions.get("Sun", {}).get("absolute_degree")
        if sun_transit_deg is not None:
            sun_house = self._get_house_for_degree(sun_transit_deg)
            insights.append(self._get_sun_transit_insight(sun_house))
            
        # 3. Transit Jupiter (Yearly Growth)
        jup_transit_deg = self.current_positions.get("Jupiter", {}).get("absolute_degree")
        if jup_transit_deg is not None:
            jup_house = self._get_house_for_degree(jup_transit_deg)
            insights.append(self._get_jupiter_transit_insight(jup_house))
            
        return insights

    def _get_moon_transit_insight(self, house: int) -> dict:
        interpretations = {
            1: "The Moon is transiting your 1st House today. Focus on self-care, personal projects, and setting intentions. Your emotions are closely tied to your physical vitality right now.",
            2: "The Moon is in your 2nd House of Wealth. You may feel emotionally attached to your finances or possessions today. Good day for budgeting or treating yourself.",
            3: "The Moon is visiting your 3rd House. Communication is key today. Expect a busy day with siblings, neighbors, or short trips. Your mind is restless.",
            4: "The Moon is in your 4th House. A perfect day to stay home, recharge, and connect with family. Emotional security is your top priority today.",
            5: "The Moon transits your 5th House. Creativity, romance, and playfulness are highlighted. Do something fun and express yourself freely.",
            6: "The Moon is in your 6th House. Focus on health routines, organization, and tackling your to-do list. You may feel a strong need to be useful today.",
            7: "The Moon transits your 7th House. Partnerships and one-on-one interactions are emotionally significant today. A great day for compromise and connection.",
            8: "The Moon is in your 8th House. You may feel more introspective or drawn to deep, intense conversations. Avoid power struggles.",
            9: "The Moon visits your 9th House. Your mind craves expansion, learning, or travel. A good day to study something new or break out of your routine.",
            10: "The Moon is in your 10th House. Your career and public image are in focus. You might feel more sensitive to how authority figures perceive you today.",
            11: "The Moon transits your 11th House. Connect with your network, friends, and community. You feel emotionally fulfilled by group activities today.",
            12: "The Moon is in your 12th House. Your energy might be low today. Take time to rest, meditate, and process your subconscious feelings before a new cycle begins."
        }
        return {
            "planet": "Moon",
            "type": "Daily Focus (Changes every 2.5 days)",
            "insight": interpretations.get(house, interpretations[1])
        }

    def _get_sun_transit_insight(self, house: int) -> dict:
        interpretations = {
            1: "The Sun is illuminating your 1st House this month. This is your personal new year. Step into the spotlight and focus on personal reinvention.",
            2: "The Sun is in your 2nd House. Your core focus this month is on building resources, stabilizing your finances, and recognizing your self-worth.",
            3: "The Sun highlights your 3rd House. A busy month for networking, writing, learning, and gathering information. Stay adaptable.",
            4: "The Sun is in your 4th House. Your energy is drawn inward toward home, family, and laying down emotional roots.",
            5: "The Sun transits your 5th House. A month of joy, creativity, and potentially romance. Allow yourself to shine and have fun.",
            6: "The Sun illuminates your 6th House. Time to get organized. Focus on your daily work routines, diet, and practical efficiency.",
            7: "The Sun is in your 7th House. The focus shifts away from 'me' to 'we'. This month is all about relationships, contracts, and finding balance with others.",
            8: "The Sun transits your 8th House. A month of transformation, deep research, and dealing with shared resources or investments.",
            9: "The Sun highlights your 9th House. You are seeking meaning, truth, and perhaps literal or philosophical travel. Expand your horizons.",
            10: "The Sun is in your 10th House. This is a peak career month. You are highly visible to bosses and the public. Push for your professional goals.",
            11: "The Sun transits your 11th House. Focus on your long-term dreams and the communities that support them. Networking is highly favored.",
            12: "The Sun is in your 12th House. A month to wrap up loose ends, rest, and prepare for a new cycle. Don't push too hard right now; trust your intuition."
        }
        return {
            "planet": "Sun",
            "type": "Monthly Theme (Changes every 30 days)",
            "insight": interpretations.get(house, interpretations[1])
        }
        
    def _get_jupiter_transit_insight(self, house: int) -> dict:
        interpretations = {
            1: "Transit Jupiter is in your 1st House. This year brings massive personal growth, optimism, and opportunities to expand your identity.",
            2: "Transit Jupiter is in your 2nd House. A highly auspicious time for financial growth. Your earning potential is expanding.",
            3: "Transit Jupiter is in your 3rd House. Your mind is hungry for knowledge. A great year for writing, speaking, and learning new skills.",
            4: "Transit Jupiter is in your 4th House. You may expand your home, buy real estate, or experience increased peace and joy in your family life.",
            5: "Transit Jupiter is in your 5th House. A fertile year for creativity, investments, and joy. Romance and artistic projects are highly favored.",
            6: "Transit Jupiter is in your 6th House. Opportunities for better working conditions or improved health routines. You may take on more daily responsibilities.",
            7: "Transit Jupiter is in your 7th House. A classic indicator of favorable partnerships, marriage, or beneficial business contracts.",
            8: "Transit Jupiter is in your 8th House. You may benefit from joint finances, inheritances, or deep psychological breakthroughs.",
            9: "Transit Jupiter is in your 9th House. A year of profound philosophical growth, higher education, or significant international travel.",
            10: "Transit Jupiter is in your 10th House. A major career peak. You are likely to receive recognition, promotion, or expanded professional influence.",
            11: "Transit Jupiter is in your 11th House. Your network is expanding. A great time to join groups or see your long-term hopes and wishes materialize.",
            12: "Transit Jupiter is in your 12th House. A time of spiritual protection. You may find great joy in solitude, meditation, or behind-the-scenes work."
        }
        return {
            "planet": "Jupiter",
            "type": "Yearly Growth (Changes every 12 months)",
            "insight": interpretations.get(house, interpretations[1])
        }
