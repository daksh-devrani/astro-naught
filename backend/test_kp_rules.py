"""
KP Rules Verification Script — Tests the full KP pipeline.
Math Engine → Astrology Engine → KP Evaluator → Compiler
"""
import sys
import os
import json

# Project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.engine.math_engine import VedicMathEngine
from backend.engine.astrology import AstrologyEngine
from backend.engine.compiler import PredictionCompiler
from backend.engine.dasha import DashaCalculator
from backend.rules.kp_evaluator import KPEvaluator

PASS = "✓"
FAIL = "✗"

def test_section(name, test_fn):
    """Run a test and print result."""
    try:
        result = test_fn()
        print(f"  {PASS} {name}")
        return True
    except AssertionError as e:
        print(f"  {FAIL} {name}: {e}")
        return False
    except Exception as e:
        print(f"  {FAIL} {name}: EXCEPTION — {e}")
        return False

def main():
    print("=" * 70)
    print("KP ASTROLOGY RULES — FULL VERIFICATION")
    print("=" * 70)
    
    passed = 0
    total = 0
    
    # --------- Setup: Generate Chart ---------
    print("\n[1] CHART GENERATION (KP Mode)")
    print("-" * 50)
    
    math_engine = VedicMathEngine()
    astro_engine = AstrologyEngine()
    
    math_res = math_engine.calculate_positions(1998, 6, 14, 5, 0, 28.6139, 77.2090, "kp")
    chart = astro_engine.generate_chart(math_res, "KP")
    
    def test_chart_basics():
        assert "ascendant" in chart, "No ascendant in chart"
        assert "planets" in chart, "No planets in chart"
        assert "kp_cusps" in chart, "No kp_cusps in chart"
        assert "kp_significators" in chart, "No kp_significators in chart"
        assert "houses" in chart, "No houses in chart"
        assert len(chart["planets"]) == 9, f"Expected 9 planets, got {len(chart['planets'])}"
    
    total += 1; passed += test_section("Chart structure valid", test_chart_basics)
    
    print(f"    Ascendant: {chart['ascendant']['sign']} ({chart['ascendant']['sign_number']})")
    print(f"    Moon: {chart['planets']['Moon']['sign']} H{chart['planets']['Moon']['house']}")
    
    # --------- Sub-Lord Accuracy ---------
    print(f"\n[2] SUB-LORD ACCURACY")
    print("-" * 50)
    
    def test_sublords_present():
        for p_name, p_data in chart["planets"].items():
            assert "kp_star_lord" in p_data, f"{p_name} missing kp_star_lord"
            assert "kp_sub_lord" in p_data, f"{p_name} missing kp_sub_lord"
            assert "kp_sub_sub_lord" in p_data, f"{p_name} missing kp_sub_sub_lord"
    
    total += 1; passed += test_section("All planets have star/sub/sub-sub lords", test_sublords_present)
    
    def test_sublords_valid():
        valid_planets = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"}
        for p_name, p_data in chart["planets"].items():
            assert p_data["kp_star_lord"] in valid_planets, f"{p_name} invalid star lord: {p_data['kp_star_lord']}"
            assert p_data["kp_sub_lord"] in valid_planets, f"{p_name} invalid sub lord: {p_data['kp_sub_lord']}"
    
    total += 1; passed += test_section("Sub-lords are valid planet names", test_sublords_valid)
    
    for p_name in ["Sun", "Moon", "Mars"]:
        p = chart["planets"][p_name]
        print(f"    {p_name}: Star={p['kp_star_lord']}, Sub={p['kp_sub_lord']}, Sub-Sub={p['kp_sub_sub_lord']}")
    
    # --------- KP Number Mapping ---------
    print(f"\n[3] KP NUMBER SYSTEM (1-249)")
    print("-" * 50)
    
    def test_kp_numbers():
        for p_name, p_data in chart["planets"].items():
            assert "kp_number" in p_data, f"{p_name} missing kp_number"
            kn = p_data["kp_number"]
            assert 1 <= kn <= 249, f"{p_name} KP number out of range: {kn}"
    
    total += 1; passed += test_section("All planets have valid KP numbers (1-249)", test_kp_numbers)
    
    def test_cusp_kp_numbers():
        for h_num, cusp in chart["kp_cusps"].items():
            assert "kp_number" in cusp, f"Cusp {h_num} missing kp_number"
            kn = cusp["kp_number"]
            assert 1 <= kn <= 249, f"Cusp {h_num} KP number out of range: {kn}"
    
    total += 1; passed += test_section("All cusps have valid KP numbers", test_cusp_kp_numbers)
    
    for p_name in ["Sun", "Moon", "Mars"]:
        print(f"    {p_name}: KP# {chart['planets'][p_name]['kp_number']}")
    
    # --------- 4-Fold Significators ---------
    print(f"\n[4] 4-FOLD SIGNIFICATORS")
    print("-" * 50)
    
    evaluator = KPEvaluator(chart)
    
    def test_significators():
        for h in range(1, 13):
            sig = evaluator.get_significators(h)
            assert sig["house"] == h
            assert "levels" in sig
            assert "ordered" in sig
    
    total += 1; passed += test_section("Significators computed for all 12 houses", test_significators)
    
    sig7 = evaluator.get_significators(7)
    print(f"    House 7 significators: {sig7['ordered']}")
    print(f"    House 7 L1: {sig7['levels'].get('L1', [])}")
    
    # --------- Ruling Planets ---------
    print(f"\n[5] RULING PLANETS")
    print("-" * 50)
    
    def test_ruling_planets():
        rp = evaluator.get_ruling_planets()
        assert "day_lord" in rp
        assert "moon_sign_lord" in rp
        assert "moon_star_lord" in rp
        assert "lagna_sign_lord" in rp
        assert "lagna_star_lord" in rp
        assert len(rp["unique_ruling_planets"]) > 0
    
    total += 1; passed += test_section("Ruling planets computed with 5 components", test_ruling_planets)
    
    rp = evaluator.get_ruling_planets()
    print(f"    Day Lord: {rp['day_lord']}")
    print(f"    Moon Sign Lord: {rp['moon_sign_lord']}")
    print(f"    Moon Star Lord: {rp['moon_star_lord']}")
    print(f"    Unique RPs: {rp['unique_ruling_planets']}")
    
    # --------- Promise Analysis ---------
    print(f"\n[6] CUSP PROMISE ANALYSIS")
    print("-" * 50)
    
    def test_promise_analysis():
        promise_7 = evaluator.analyze_cusp_promise(7)
        assert "cusp_sub_lord" in promise_7
        assert promise_7["cusp_sub_lord"] is not None
        assert "sub_lord_signifies_houses" in promise_7
    
    total += 1; passed += test_section("Cusp promise analysis produces valid output", test_promise_analysis)
    
    p7 = evaluator.analyze_cusp_promise(7)
    print(f"    7th cusp sub-lord: {p7['cusp_sub_lord']}")
    print(f"    Sub-lord signifies: {p7['sub_lord_signifies_houses']}")
    for query, data in p7.get("analyses", {}).items():
        print(f"    → {query}: {'PROMISED' if data['is_promised'] else 'NOT PROMISED'} ({data['strength']})")
    
    # --------- Dasha with Pratyantara ---------
    print(f"\n[7] DASHA WITH PRATYANTARA")
    print("-" * 50)
    
    from datetime import datetime
    moon_nak = chart["planets"]["Moon"]
    nak_idx = moon_nak.get("nakshatra", "")
    # Use degree to calculate nakshatra index
    moon_deg = moon_nak["absolute_degree"]
    nak_length = 360.0 / 27.0
    nak_index = int(moon_deg // nak_length)
    deg_in_nak = moon_deg - (nak_index * nak_length)
    
    dasha = DashaCalculator(nak_index, deg_in_nak, datetime(1998, 6, 14))
    dasha_result = dasha.calculate_dashas()
    
    def test_dasha_pratyantara():
        assert "current_mahadasha" in dasha_result
        assert "current_antardasha" in dasha_result
        assert "current_pratyantara" in dasha_result
        assert dasha_result["current_pratyantara"] is not None, "Pratyantara should be calculated"
    
    total += 1; passed += test_section("Dasha includes Pratyantara (sub-sub-sub)", test_dasha_pratyantara)
    
    print(f"    Mahadasha: {dasha_result['current_mahadasha']} (ends {dasha_result['mahadasha_end']})")
    print(f"    Antardasha: {dasha_result.get('current_antardasha')} (ends {dasha_result.get('antardasha_end')})")
    print(f"    Pratyantara: {dasha_result.get('current_pratyantara')} (ends {dasha_result.get('pratyantara_end')})")
    
    # --------- Full Pipeline ---------
    print(f"\n[8] FULL KP PIPELINE (Compiler)")
    print("-" * 50)
    
    def test_full_pipeline():
        compiler = PredictionCompiler(chart)
        profile = compiler.build_full_profile()
        
        assert "kp_analysis" in profile, "Missing kp_analysis in output"
        kp = profile["kp_analysis"]
        assert "promise_analysis" in kp, "Missing promise_analysis"
        assert "significator_table" in kp, "Missing significator_table"
        assert "ruling_planets" in kp, "Missing ruling_planets"
        assert "kp_cusps" in kp, "Missing kp_cusps"
        return profile
    
    total += 1; passed += test_section("Full KP pipeline produces valid JSON", test_full_pipeline)
    
    def test_kp_profile_method():
        compiler = PredictionCompiler(chart)
        kp_profile = compiler.build_kp_profile()
        
        assert "promise_analysis" in kp_profile
        assert "significator_table" in kp_profile
        assert "ruling_planets" in kp_profile
        assert "kp_cusps" in kp_profile
    
    total += 1; passed += test_section("build_kp_profile() produces complete KP output", test_kp_profile_method)
    
    # --------- Dasha Significator Check ---------
    print(f"\n[9] DASHA-SIGNIFICATOR CONNECTION")
    print("-" * 50)
    
    def test_dasha_significator():
        sig_check = dasha.is_dasha_lord_significator(chart["kp_significators"], [2, 7, 11])
        assert "mahadasha" in sig_check
        assert "antardasha" in sig_check
        assert "house_alignment" in sig_check
    
    total += 1; passed += test_section("Dasha-Significator alignment check works", test_dasha_significator)
    
    sig_check = dasha.is_dasha_lord_significator(chart["kp_significators"], [2, 7, 11])
    print(f"    MD {sig_check['mahadasha']['lord']} signifies: {sig_check['mahadasha']['signifies_houses']}")
    print(f"    AD {sig_check['antardasha']['lord']} signifies: {sig_check['antardasha']['signifies_houses']}")
    print(f"    Marriage alignment (2,7,11): {sig_check['house_alignment']}")
    
    # --------- Summary ---------
    print(f"\n{'=' * 70}")
    print(f"VERIFICATION COMPLETE: {passed}/{total} tests passed")
    if passed == total:
        print(f"🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
