"""
Verification script for Advanced Jyotish Rules.
Tests the full pipeline: Math Engine -> Astrology Engine -> Rule Evaluator -> Compiler.
"""
import sys
import os
import json

# Project root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.engine.math_engine import VedicMathEngine
from backend.engine.astrology import AstrologyEngine
from backend.engine.compiler import PredictionCompiler
from backend.rules.evaluator import RuleEvaluator

def main():
    print("=" * 70)
    print("ADVANCED JYOTISH RULES — VERIFICATION TEST")
    print("=" * 70)
    
    # Test case: 14 June 1998, 5:00 UTC, Delhi
    print("\n[1] Generating chart for: 14 June 1998, 05:00 UTC, Delhi (28.61, 77.21)")
    math_res = VedicMathEngine().calculate_positions(1998, 6, 14, 5, 0, 28.6139, 77.2090)
    chart = AstrologyEngine().generate_chart(math_res)
    
    print(f"    Ascendant: {chart['ascendant']['sign']} ({chart['ascendant']['sign_number']})")
    print(f"    Moon: {chart['planets']['Moon']['sign']} H{chart['planets']['Moon']['house']}")
    print(f"    Houses populated: {sum(1 for h in chart['houses'].values() if h)}/12\n")
    
    # Test Evaluator
    evaluator = RuleEvaluator(chart)
    advanced = evaluator.evaluate_all_advanced()
    
    # --- Planet Dignities ---
    print("[2] PLANET DIGNITIES")
    print("-" * 50)
    for d in advanced["planet_dignities"]:
        print(f"    {d['planet']:10s} → {d['dignity']:16s} (score: {d['dignity_score']:+d})")
    
    # --- Panch Mahapurusha ---
    print(f"\n[3] PANCH MAHAPURUSHA YOGAS ({len(advanced['panch_mahapurusha'])} found)")
    print("-" * 50)
    for y in advanced["panch_mahapurusha"]:
        print(f"    ✓ {y['name']}: {y['planet']} ({y['dignity']}) in H{y['house']}")
    if not advanced["panch_mahapurusha"]:
        print("    (none found)")
    
    # --- Dhana Yogas ---
    print(f"\n[4] DHANA YOGAS ({len(advanced['dhana_yogas'])} found)")
    print("-" * 50)
    for y in advanced["dhana_yogas"]:
        print(f"    ✓ {y['description']}")
    if not advanced["dhana_yogas"]:
        print("    (none found)")
    
    # --- Raja Yogas ---
    print(f"\n[5] RAJA YOGAS ({len(advanced['raja_yogas'])} found)")
    print("-" * 50)
    for y in advanced["raja_yogas"]:
        print(f"    ✓ {y['name']}: {y.get('description', '')}")
    if not advanced["raja_yogas"]:
        print("    (none found)")
    
    # --- Viparita Raja Yogas ---
    print(f"\n[6] VIPARITA RAJA YOGAS ({len(advanced['viparita_raja_yogas'])} found)")
    print("-" * 50)
    for y in advanced["viparita_raja_yogas"]:
        print(f"    ✓ {y['name']}: {y['planet']} (H{y['lord_of']} → H{y['placed_in']})")
    if not advanced["viparita_raja_yogas"]:
        print("    (none found)")
    
    # --- Neecha Bhanga ---
    print(f"\n[7] NEECHA BHANGA RAJA YOGA ({len(advanced['neecha_bhanga'])} found)")
    print("-" * 50)
    for y in advanced["neecha_bhanga"]:
        print(f"    ✓ {y['planet']}: {'; '.join(y['reasons'])}")
    if not advanced["neecha_bhanga"]:
        print("    (none found)")
    
    # --- Sun Yogas ---
    print(f"\n[8] SUN YOGAS ({len(advanced['sun_yogas'])} found)")
    print("-" * 50)
    for y in advanced["sun_yogas"]:
        print(f"    ✓ {y['name']}: {y.get('description', '')}")
    if not advanced["sun_yogas"]:
        print("    (none found)")
    
    # --- Moon Yogas ---
    print(f"\n[9] MOON YOGAS ({len(advanced['moon_yogas'])} found)")
    print("-" * 50)
    for y in advanced["moon_yogas"]:
        print(f"    ✓ {y['name']}: {y.get('description', '')}")
    if not advanced["moon_yogas"]:
        print("    (none found)")
    
    # --- Amala Yoga ---
    print(f"\n[10] AMALA YOGA ({len(advanced['amala_yoga'])} found)")
    print("-" * 50)
    for y in advanced["amala_yoga"]:
        print(f"    ✓ {y['name']}: {', '.join(y['planets'])}")
    if not advanced["amala_yoga"]:
        print("    (none found)")
    
    # --- Doshas ---
    print("\n[11] DOSHA ANALYSIS")
    print("-" * 50)
    manglik = advanced["manglik_dosha"]
    print(f"    Manglik: {'YES' if manglik['is_manglik'] else 'NO'} | Severity: {manglik['severity']} | Cancelled: {manglik.get('is_cancelled', False)}")
    
    kaal_sarp = advanced["kaal_sarp_dosha"]
    print(f"    Kaal Sarp: {'YES — ' + kaal_sarp.get('type', '') if kaal_sarp['is_present'] else 'NO'}")
    
    sade_sati = advanced["sade_sati"]
    print(f"    Sade Sati (natal): {'YES — ' + sade_sati.get('phase', '') if sade_sati['is_active'] else 'NO'}")
    
    # --- Planet Strengths ---
    print(f"\n[12] PLANET STRENGTH SUMMARY")
    print("-" * 50)
    for s in advanced["planet_strengths"]:
        factors = f" [{'; '.join(s['factors'])}]" if s['factors'] else ""
        print(f"    {s['planet']:10s} → {s['disposition']:12s} (score {s['score']:+d}){factors}")
    
    # --- Compiler Integration ---
    print(f"\n[13] COMPILER INTEGRATION TEST")
    print("-" * 50)
    compiler = PredictionCompiler(chart)
    full_profile = compiler.build_full_profile()
    has_advanced = "advanced_analysis" in full_profile
    print(f"    'advanced_analysis' key present: {has_advanced}")
    if has_advanced:
        adv_keys = list(full_profile["advanced_analysis"].keys())
        print(f"    Sub-keys: {', '.join(adv_keys)}")
        print(f"    Total sub-sections: {len(adv_keys)}")
    
    # Structure validation
    expected_keys = ["planet_dignities", "panch_mahapurusha", "dhana_yogas", "raja_yogas",
                     "viparita_raja_yogas", "neecha_bhanga", "sun_yogas", "moon_yogas",
                     "amala_yoga", "manglik_dosha", "kaal_sarp_dosha", "sade_sati", "planet_strengths"]
    
    missing = [k for k in expected_keys if k not in full_profile.get("advanced_analysis", {})]
    if missing:
        print(f"    ⚠ MISSING KEYS: {missing}")
    else:
        print(f"    ✓ All {len(expected_keys)} expected sub-sections present!")
    
    print("\n" + "=" * 70)
    print("VERIFICATION COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
