from datetime import datetime, timedelta

# The sequence of Vimshottari Dasha lords and their total duration in years (sum = 120)
DASHA_LORDS = [
    {"planet": "Ketu", "years": 7},
    {"planet": "Venus", "years": 20},
    {"planet": "Sun", "years": 6},
    {"planet": "Moon", "years": 10},
    {"planet": "Mars", "years": 7},
    {"planet": "Rahu", "years": 18},
    {"planet": "Jupiter", "years": 16},
    {"planet": "Saturn", "years": 19},
    {"planet": "Mercury", "years": 17}
]

# Total number of days in the Vimshottari Dasha cycle (using 365.2425 for leap year accuracy)
TOTAL_DASHA_YEARS = 120

class DashaCalculator:
    def __init__(self, moon_nakshatra_index: int, moon_degree_in_nakshatra: float, birth_date: datetime):
        """
        Calculates the Vimshottari Dasha sequence.
        moon_nakshatra_index: 0 to 26 (Ashwini = 0, Revati = 26)
        moon_degree_in_nakshatra: Degree elapsed within the current 13.3333 degree Nakshatra
        birth_date: Datetime of birth
        """
        self.moon_index = moon_nakshatra_index
        self.moon_degree = moon_degree_in_nakshatra
        self.birth_date = birth_date
        
        # Determine the starting Dasha Lord. The sequence repeats every 9 nakshatras.
        self.starting_lord_index = self.moon_index % 9
        
    def calculate_dashas(self, target_date=None):
        if not target_date:
            target_date = datetime.now()
            
        # 1 Nakshatra = 13.3333 degrees = 800 minutes
        # Find fraction of nakshatra remaining
        nakshatra_length = 360.0 / 27.0
        fraction_remaining = (nakshatra_length - self.moon_degree) / nakshatra_length
        
        # Calculate balance of starting Dasha at birth
        starting_lord = DASHA_LORDS[self.starting_lord_index]
        balance_years = starting_lord["years"] * fraction_remaining
        
        # Generator for the timeline
        periods = []
        current_date = self.birth_date
        
        # First Mahadasha (partial)
        end_date = current_date + timedelta(days=balance_years * 365.2425)
        periods.append({
            "mahadasha": starting_lord["planet"],
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "end_date_obj": end_date,
            "lord_index": self.starting_lord_index
        })
        current_date = end_date
        
        # Subsequent Mahadashas (Full)
        lord_count = len(DASHA_LORDS)
        for i in range(1, lord_count):
            lord_idx = (self.starting_lord_index + i) % lord_count
            lord = DASHA_LORDS[lord_idx]
            
            end_date = current_date + timedelta(days=lord["years"] * 365.2425)
            periods.append({
                "mahadasha": lord["planet"],
                "start": current_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "end_date_obj": end_date,
                "lord_index": lord_idx
            })
            current_date = end_date
            
        # Find current Mahadasha
        current_md = None
        for p in periods:
            start_dt = datetime.strptime(p["start"], "%Y-%m-%d")
            end_dt = p["end_date_obj"]
            if start_dt <= target_date < end_dt:
                current_md = p
                break
                
        # If found, calculate Antardasha (Sub-period)
        if current_md:
            md_lord_idx = current_md["lord_index"]
            md_total_years = DASHA_LORDS[md_lord_idx]["years"]
            
            # Antardasha always starts with the Mahadasha lord
            ad_start = datetime.strptime(current_md["start"], "%Y-%m-%d")
            current_ad = None
            
            for i in range(lord_count):
                ad_lord_idx = (md_lord_idx + i) % lord_count
                ad_lord = DASHA_LORDS[ad_lord_idx]
                
                # Formula: (MD Years * AD Years) / 120
                ad_years = (md_total_years * ad_lord["years"]) / TOTAL_DASHA_YEARS
                ad_end = ad_start + timedelta(days=ad_years * 365.2425)
                
                if ad_start <= target_date < ad_end:
                    current_ad = {
                        "antardasha": ad_lord["planet"],
                        "start": ad_start.strftime("%Y-%m-%d"),
                        "end": ad_end.strftime("%Y-%m-%d")
                    }
                    break
                    
                ad_start = ad_end
                
            # Calculate Pratyantara Dasha (Sub-Sub Period) if Antardasha found
            current_pd = None
            if current_ad:
                ad_lord_idx_computed = None
                for i in range(lord_count):
                    idx = (md_lord_idx + i) % lord_count
                    if DASHA_LORDS[idx]["planet"] == current_ad["antardasha"]:
                        ad_lord_idx_computed = idx
                        break
                
                if ad_lord_idx_computed is not None:
                    ad_total_years = (md_total_years * DASHA_LORDS[ad_lord_idx_computed]["years"]) / TOTAL_DASHA_YEARS
                    pd_start = datetime.strptime(current_ad["start"], "%Y-%m-%d")
                    
                    for i in range(lord_count):
                        pd_lord_idx = (ad_lord_idx_computed + i) % lord_count
                        pd_lord = DASHA_LORDS[pd_lord_idx]
                        
                        # Pratyantara duration = (AD_years * PD_years) / 120
                        pd_years = (ad_total_years * pd_lord["years"]) / TOTAL_DASHA_YEARS
                        pd_end = pd_start + timedelta(days=pd_years * 365.2425)
                        
                        if pd_start <= target_date < pd_end:
                            current_pd = {
                                "pratyantara": pd_lord["planet"],
                                "start": pd_start.strftime("%Y-%m-%d"),
                                "end": pd_end.strftime("%Y-%m-%d")
                            }
                            break
                        pd_start = pd_end

            return {
                "current_mahadasha": current_md["mahadasha"] if current_md else "Unknown",
                "mahadasha_end": current_md["end"] if current_md else "Unknown",
                "current_antardasha": current_ad["antardasha"] if current_ad else None,
                "antardasha_end": current_ad["end"] if current_ad else None,
                "current_pratyantara": current_pd["pratyantara"] if current_pd else None,
                "pratyantara_end": current_pd["end"] if current_pd else None
            }
            
        return {"error": "Date out of 120-year bound"}

    def get_full_timeline(self):
        """
        Calculates the complete 120-year Mahadasha and Antardasha sequence.
        Returns a list of Mahadasha objects, each containing its Antardashas.
        """
        # 1. Calculate all Mahadashas
        nakshatra_length = 360.0 / 27.0
        fraction_remaining = (nakshatra_length - self.moon_degree) / nakshatra_length
        starting_lord_idx = self.starting_lord_index
        starting_lord = DASHA_LORDS[starting_lord_idx]
        
        balance_years = starting_lord["years"] * fraction_remaining
        
        timeline = []
        current_date = self.birth_date
        lord_count = len(DASHA_LORDS)
        
        for i in range(lord_count):
            l_idx = (starting_lord_idx + i) % lord_count
            lord = DASHA_LORDS[l_idx]
            
            years = balance_years if i == 0 else lord["years"]
            end_date = current_date + timedelta(days=years * 365.2425)
            
            mahadasha = {
                "lord": lord["planet"],
                "start": current_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "antardashas": []
            }
            
            # 2. Calculate Antardashas for this Mahadasha
            ad_start = current_date
            md_total_years = lord["years"] # Always use full years for ratio
            
            for j in range(lord_count):
                ad_l_idx = (l_idx + j) % lord_count
                ad_lord = DASHA_LORDS[ad_l_idx]
                
                # Formula: (MD Years * AD Years) / 120
                ad_years = (md_total_years * ad_lord["years"]) / TOTAL_DASHA_YEARS
                
                # For first Mahadasha, we might need to skip some Antardashas 
                # that were already over at birth.
                ad_end = ad_start + timedelta(days=ad_years * 365.2425)
                
                # Check if this sub-period at least partially falls within the Mahadasha's range
                # (Relevant for the first partial Mahadasha)
                if ad_end > current_date:
                    effective_ad_start = max(ad_start, current_date)
                    if effective_ad_start < end_date:
                        mahadasha["antardashas"].append({
                            "lord": ad_lord["planet"],
                            "start": effective_ad_start.strftime("%Y-%m-%d"),
                            "end": min(ad_end, end_date).strftime("%Y-%m-%d")
                        })
                
                ad_start = ad_end
                
            timeline.append(mahadasha)
            current_date = end_date
            
        return timeline

    def is_dasha_lord_significator(self, significators: dict, check_houses: list = None) -> dict:
        """
        Checks if the current dasha lords are significators of specific houses.
        
        Args:
            significators: The KP significator table from chart data
            check_houses: Optional list of house numbers to check (e.g., [2, 7, 11] for marriage)
        
        Returns:
            Dict showing which dasha lords are significators of which houses
        """
        dasha_data = self.calculate_dashas()
        if "error" in dasha_data:
            return dasha_data
        
        result = {
            "mahadasha": {"lord": dasha_data["current_mahadasha"], "signifies_houses": []},
            "antardasha": {"lord": dasha_data.get("current_antardasha"), "signifies_houses": []},
            "pratyantara": {"lord": dasha_data.get("current_pratyantara"), "signifies_houses": []}
        }
        
        for period_key in ["mahadasha", "antardasha", "pratyantara"]:
            lord = result[period_key]["lord"]
            if not lord:
                continue
            
            for h_num in range(1, 13):
                h_key = h_num if h_num in significators else str(h_num)
                if h_key not in significators:
                    continue
                for level in ["L1", "L2", "L3", "L4"]:
                    if lord in significators[h_key].get(level, []):
                        result[period_key]["signifies_houses"].append(h_num)
                        break
        
        # If specific houses requested, check alignment
        if check_houses:
            alignment = {}
            for period_key in ["mahadasha", "antardasha", "pratyantara"]:
                houses = result[period_key]["signifies_houses"]
                matching = [h for h in houses if h in check_houses]
                alignment[period_key] = {
                    "aligned": len(matching) > 0,
                    "matching_houses": matching
                }
            result["house_alignment"] = alignment
        
        return result

# Quick test
if __name__ == "__main__":
    # Moon at 10 deg in Krittika (Index 2). 
    birth = datetime(1998, 6, 14)
    dasha = DashaCalculator(2, 10.0, birth)
    result = dasha.calculate_dashas()
    print(f"Mahadasha: {result['current_mahadasha']} (ends {result['mahadasha_end']})")
    print(f"Antardasha: {result.get('current_antardasha')} (ends {result.get('antardasha_end')})")
    print(f"Pratyantara: {result.get('current_pratyantara')} (ends {result.get('pratyantara_end')})")

