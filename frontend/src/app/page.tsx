/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */
"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import UserInputForm from "@/components/ui/UserInputForm";
import { LoadingSpinner } from "@/components/ui/Loading";
import NorthIndianChart from "@/components/charts/NorthIndianChart";
import { Moon, ChevronLeft, ChevronRight } from "lucide-react";
import AdvancedAnalysisSection from "@/components/ui/AdvancedAnalysisSection";
import KPDataSection from "@/components/ui/KPDataSection";
import DeterministicDashboard from "@/components/ui/DeterministicDashboard";
import TimelineView from "@/components/ui/TimelineView";
import Link from "next/link";
import { useUser } from "@/context/UserContext";
import { useRouter } from "next/navigation";
import LocationPicker from "@/components/ui/LocationPicker";
import { useChartHistory, SavedChart } from "@/hooks/useChartHistory";
import { User, Users } from "lucide-react";

export default function Home() {
  const [viewMode, setViewMode] = useState<"launchpad" | "individual">("launchpad");
  const { history, saveChart, removeChart } = useChartHistory();
  const [isLoading, setIsLoading] = useState(false);
  const [chartData, setChartData] = useState<any>(null);
  const [predictions, setPredictions] = useState<any>(null);
  const [isD9, setIsD9] = useState(false);

  const [isAiLoading, setIsAiLoading] = useState(false);
  const [aiReading, setAiReading] = useState<string | null>(null);
  const [lastSubmittedFormData, setLastSubmittedFormData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const { setPrimaryProfile, primaryProfile } = useUser();
  const router = useRouter();

  const getVargaDescription = (id: string) => {
    switch (id) {
      case "D2": return "The Hora chart (D2) focuses on wealth, assets, and financial prosperity. It divides each sign into two parts, traditionally ruled by the Sun (Solar Hora) and the Moon (Lunar Hora). It reveals how you accumulate and sustain resources.";
      case "D9": return "The Navamsa (D9) is the most critical micro-chart, revealing the internal strength of planets and the true quality of your marriage and partnership. It is said that D1 is the body, but D9 is the soul.";
      case "D12": return "Dwadasamsa (D12) represents your lineage, parents, and ancestral heritage. It shows the subtle influences passed down from your father and mother and your general relationship with your ancestry.";
      case "D60": return "Shastiamsa (D60) is a highly sensitive chart dealing with deep-seated karma and the soul's journey. It is often used for extremely precise timing of events and understanding the root cause of one's destiny.";
      default: return "";
    }
  };

  const getSignName = (num: number) => {
    const signs = ["", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"];
    return signs[num] || "Unknown";
  };

  const [activeCard, setActiveCard] = useState<string | null>(null);
  const [chartSystem, setChartSystem] = useState<"kp" | "vedic">("kp");
  const [stars, setStars] = useState<any[]>([]);

  useEffect(() => {
    setStars(Array.from({ length: 50 }).map((_, i) => ({
      id: i,
      top: `${Math.random() * 100}%`,
      left: `${Math.random() * 100}%`,
      animationDelay: `${Math.random() * 5}s`,
      animationDuration: `${3 + Math.random() * 4}s`
    })));
  }, []);

  const vargas = [
    { id: "D1", name: "D1 (Rasi)", sub: "General Destiny", color: "amber" },
    { id: "D2", name: "D2 (Hora)", sub: "Wealth & Assets", color: "emerald" },
    { id: "D9", name: "D9 (Navamsa)", sub: "Marriage & Fruits", color: "rose" },
    { id: "D12", name: "D12 (Dwadasamsa)", sub: "Parents & Lineage", color: "indigo" },
    { id: "D60", name: "D60 (Shastiamsa)", sub: "Past Karma & Soul", color: "violet" },
  ];

  const handleNextVarga = () => {
    const currentIndex = vargas.findIndex(v => v.id === activeCard);
    if (currentIndex === -1) {
      setActiveCard(vargas[0].id);
    } else {
      setActiveCard(vargas[(currentIndex + 1) % vargas.length].id);
    }
  };

  const handlePrevVarga = () => {
    const currentIndex = vargas.findIndex(v => v.id === activeCard);
    if (currentIndex === -1) {
      setActiveCard(vargas[vargas.length - 1].id);
    } else {
      setActiveCard(vargas[(currentIndex - 1 + vargas.length) % vargas.length].id);
    }
  };

  const fetchChart = async (formData: any) => {
    setIsLoading(true);
    setChartData(null);
    setPredictions(null);
    setAiReading(null);
    setLastSubmittedFormData(formData);

    // Save to history cache
    saveChart(formData);

    try {
      // Instead of just the chart, we fetch the full prediction profile which CONTAINS the chart data implicitly via the rules engine, OR we fetch both.
      // Easiest is to fetch /chart for the grid, and /predictions for the text.
      // Let's do a fast Promise.all to get both the Math Chart and the Interpretations.

      const [chartRes, predRes] = await Promise.all([
        fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/chart`, {
          method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(formData)
        }),
        fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/predictions`, {
          method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(formData)
        })
      ]);

      if (!chartRes.ok || !predRes.ok) throw new Error("Failed to consult the backend.");

      setChartData(await chartRes.json());
      setPredictions(await predRes.json());
      setActiveCard("D1");

    } catch (err: any) {
      setError(err.message || "An error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGetAiReading = async () => {
    setIsAiLoading(true);
    setAiReading(null);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/ai-insights`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...lastSubmittedFormData, preferred_system: chartSystem })
      });
      if (!res.ok) throw new Error("Backend AI error");
      const data = await res.json();
      setAiReading(data.ai_reading);
    } catch (err) {
      setAiReading("Failed to connect to AI engine. Make sure Ollama is running locally with the 'dolphin' model pulled.");
    } finally {
      setIsAiLoading(false);
    }
  };

  // Helper function to map our backend chart dict into the Array<HouseData> the SVG expects
  const mapBackEndToFrontEndHouses = (vargaKey = "D1") => {
    if (!chartData) return [];

    const isD1 = vargaKey === "D1";
    let ascendantSignNumber;
    
    if (isD1) {
      ascendantSignNumber = chartData.ascendant.sign_number;
    } else {
      const field = `${vargaKey.toLowerCase()}_sign_number`;
      ascendantSignNumber = chartData.ascendant[field] || chartData.ascendant.sign_number;
    }

    const housesArray = [];

    for (let h = 1; h <= 12; h++) {
      const rashiNum = ((ascendantSignNumber + h - 2) % 12) + 1;
      const occupants: any[] = [];

      Object.entries(chartData.planets).forEach(([planetName, pData]: [string, any]) => {
        let planetHouseNum;
        
        if (isD1) {
          planetHouseNum = chartSystem === "kp" 
            ? (pData.house_kp || pData.house) 
            : (pData.house_vedic || pData.house);
        } else {
          // For Vargas, we use Whole Sign: ((Varga_Sign - Varga_Asc_Sign) % 12) + 1
          const vSignNum = pData[`${vargaKey.toLowerCase()}_sign_number`] || pData.sign_number;
          const dist = (vSignNum - ascendantSignNumber);
          planetHouseNum = ((dist < 0 ? dist + 12 : dist) % 12) + 1;
        }

        if (planetHouseNum === h) {
          occupants.push({
            name: planetName,
            degree: pData.degree_in_sign,
            isExalted: vargaKey === "D9" ? pData.is_navamsa_exalted : pData.is_exalted,
            isDebilitated: vargaKey === "D9" ? pData.is_navamsa_debilitated : pData.is_debilitated,
            isVargottama: vargaKey === "D9" ? pData.is_vargottama : false,
            isPushkara: vargaKey === "D9" ? pData.is_pushkara : false
          });
        }
      });

      housesArray.push({
        houseNumber: h,
        rashiNumber: rashiNum,
        planets: occupants
      });
    }
    return housesArray;
  };

  return (
    <main className="min-h-screen bg-[#0b0c10] text-slate-200 selection:bg-amber-500/30 font-sans relative overflow-x-hidden">
      {/* Magical Background Starfield */}
      <div className="magical-bg">
        {stars.map((star) => (
          <div
            key={`star-${star.id}`}
            className="star"
            style={{
              top: star.top,
              left: star.left,
              width: `${1 + star.id % 2}px`,
              height: `${1 + star.id % 2}px`,
              animationDelay: star.animationDelay,
              animationDuration: star.animationDuration,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-16 sm:px-6 lg:px-8">

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <div className="flex justify-center mb-4">
            <div className="p-3 bg-indigo-500/10 rounded-full border border-indigo-500/20 shadow-[0_0_30px_rgba(99,102,241,0.2)]">
              <Moon className="w-8 h-8 text-amber-300" />
            </div>
          </div>
          <h1 className="text-4xl md:text-6xl font-black tracking-tight magical-text-gradient mb-4">
            ASTRO-NAUGHT
          </h1>
          <p className="text-lg text-indigo-300/80 font-medium tracking-wide max-w-2xl mx-auto mb-8">
            Deterministic logic meets precise celestial mechanics.
          </p>
        </motion.div>

        {/* Dynamic Content Area */}
        <div className="flex flex-col items-center justify-center w-full max-w-4xl mx-auto">

          <AnimatePresence mode="wait">
            {!chartData && !isLoading && viewMode === "launchpad" && (
              <motion.div 
                key="launchpad"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="w-full flex flex-col items-center gap-12"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-3xl">
                  <button
                    onClick={() => setViewMode("individual")}
                    className="p-8 rounded-3xl bg-indigo-950/40 border border-indigo-500/30 backdrop-blur-xl hover:bg-indigo-900/50 hover:border-indigo-400 hover:shadow-[0_0_40px_rgba(99,102,241,0.2)] transition-all flex flex-col items-center justify-center gap-4 group"
                  >
                    <div className="p-4 bg-indigo-500/20 rounded-full group-hover:scale-110 transition-transform">
                      <User className="w-10 h-10 text-indigo-400" />
                    </div>
                    <h2 className="text-2xl font-bold text-white tracking-wide">Individual Reading</h2>
                    <p className="text-indigo-300/70 text-sm text-center">Generate comprehensive D1, D9, D12, and D60 charts with AI synthesis.</p>
                  </button>

                  <Link
                    href="/match"
                    className="p-8 rounded-3xl bg-pink-950/40 border border-pink-500/30 backdrop-blur-xl hover:bg-pink-900/50 hover:border-pink-400 hover:shadow-[0_0_40px_rgba(236,72,153,0.2)] transition-all flex flex-col items-center justify-center gap-4 group"
                  >
                    <div className="p-4 bg-pink-500/20 rounded-full group-hover:scale-110 transition-transform">
                      <Users className="w-10 h-10 text-pink-400" />
                    </div>
                    <h2 className="text-2xl font-bold text-white tracking-wide">Partner Matching</h2>
                    <p className="text-pink-300/70 text-sm text-center">Calculate Synastry, Ashtakoot 36-Gunas, and deep planetary compatibility.</p>
                  </Link>
                </div>

                {history.length > 0 && (
                  <div className="w-full mt-8">
                    <h3 className="text-lg font-mono text-indigo-300/60 uppercase tracking-widest mb-6 flex items-center gap-4">
                      <span className="h-px bg-indigo-500/20 flex-1"></span>
                      Recent Charts
                      <span className="h-px bg-indigo-500/20 flex-1"></span>
                    </h3>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                      {history.map((chart) => (
                        <div 
                          key={chart.id}
                          className="p-4 rounded-xl bg-slate-900/50 border border-slate-700/50 hover:border-indigo-500/50 cursor-pointer transition-colors relative group"
                          onClick={() => {
                            setViewMode("individual");
                            fetchChart(chart);
                          }}
                        >
                          <h4 className="text-white font-semibold truncate pr-6">{chart.name}</h4>
                          <p className="text-xs text-slate-400 font-mono mt-1">{chart.date} • {chart.time}</p>
                          <button 
                            onClick={(e) => { e.stopPropagation(); removeChart(chart.id); }}
                            className="absolute top-3 right-3 text-slate-500 hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
                          >
                            ×
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {!chartData && !isLoading && viewMode === "individual" && (
              <motion.div key="form-container" className="w-full relative" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <button 
                  onClick={() => setViewMode("launchpad")}
                  className="absolute -top-12 left-0 flex items-center gap-2 text-indigo-400 hover:text-white transition-colors text-sm font-mono uppercase tracking-widest"
                >
                  <ChevronLeft className="w-4 h-4" /> Back to Home
                </button>
                <UserInputForm key="form" onSubmit={fetchChart} isLoading={isLoading} />
              </motion.div>
            )}

            {isLoading && (
              <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                <LoadingSpinner message="Consulting the Cosmos..." />
              </motion.div>
            )}

            {error && (
              <motion.div 
                key="error-msg"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="text-center p-8 rounded-xl bg-red-500/10 border border-red-500/20 max-w-md"
              >
                <p className="text-red-400 font-mono text-sm mb-4">{error}</p>
                <button 
                  onClick={() => { setError(null); setChartData(null); }}
                  className="text-xs font-bold text-slate-400 hover:text-white underline tracking-widest uppercase"
                >
                  Try Again
                </button>
              </motion.div>
            )}

            {chartData && predictions && !isLoading && (
              <motion.div
                key="results"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="w-full"
              >
                {/* Dashboard Header */}
                <div className="text-center mb-10">
                  <h2 className="text-4xl font-bold text-amber-50 tracking-wider">
                    {chartData.personal_info.name}
                  </h2>
                  <div className="mt-2 text-indigo-300/80 text-sm tracking-widest uppercase flex justify-center gap-4">
                    <span>{chartData.personal_info.gender}</span>
                    <span>•</span>
                    <span>{chartData.ascendant.sign} Ascendant ({chartData.ascendant.degree.toFixed(2)}°)</span>
                  </div>
                </div>

                {/* CHART SYSTEM TOGGLE */}
                <div className="flex justify-center mb-12">
                  <div className="bg-slate-800/50 p-1 rounded-xl flex flex-col sm:flex-row gap-2 border border-slate-700/50 shadow-inner">
                    <button 
                      onClick={() => setChartSystem("kp")}
                      className={`px-6 py-2 rounded-lg text-sm tracking-wider font-bold transition-all ${chartSystem === "kp" ? "bg-indigo-600 text-white shadow-lg" : "text-slate-400 hover:text-slate-200"}`}
                    >
                      KP Chart (Placidus)
                    </button>
                    <button 
                      onClick={() => setChartSystem("vedic")}
                      className={`px-6 py-2 rounded-lg text-sm tracking-wider font-bold transition-all ${chartSystem === "vedic" ? "bg-amber-600 text-white shadow-lg text-shadow-sm" : "text-slate-400 hover:text-slate-200"}`}
                    >
                      Vedic Chart (Whole Sign)
                    </button>
                  </div>
                </div>

                {/* Flashcards Deck Section */}
                <div className="relative w-full max-w-6xl mx-auto mb-20">
                  {/* Side Navigation Buttons */}
                  <div className="absolute top-1/2 -translate-y-1/2 left-0 z-[60] pointer-events-auto">
                    <button 
                      onClick={handlePrevVarga}
                      className="p-4 rounded-full bg-slate-800/80 border border-amber-500/20 text-amber-500 hover:bg-indigo-600 hover:text-white transition-all shadow-2xl backdrop-blur-md"
                    >
                      <ChevronLeft className="w-8 h-8" />
                    </button>
                  </div>
                  
                  <div className="absolute top-1/2 -translate-y-1/2 right-0 z-[60] pointer-events-auto">
                    <button 
                      onClick={handleNextVarga}
                      className="p-4 rounded-full bg-slate-800/80 border border-amber-500/20 text-amber-500 hover:bg-indigo-600 hover:text-white transition-all shadow-2xl backdrop-blur-md"
                    >
                      <ChevronRight className="w-8 h-8" />
                    </button>
                  </div>

                  {/* Deck Container */}
                  <div className="relative h-[650px] w-full flex justify-center items-center flashcard-container">
                    <AnimatePresence initial={false}>
                      {vargas.map((v, idx) => {
                        const activeIdx = vargas.findIndex(x => x.id === activeCard);
                        const isActive = activeCard === v.id;
                        
                        // Calculate relative position for the "stack"
                        let offset = idx - (activeIdx === -1 ? Math.floor(vargas.length / 2) : activeIdx);
                        
                        // Circular logic for the stack when something is active
                        if (activeIdx !== -1) {
                          if (offset > 2) offset -= vargas.length;
                          if (offset < -2) offset += vargas.length;
                        }

                        return (
                          <motion.div
                            key={v.id}
                            onClick={() => setActiveCard(isActive ? null : v.id)}
                            initial={false}
                            animate={{
                              zIndex: isActive ? 100 : 50 - Math.abs(offset),
                              scale: isActive ? 1.15 : activeCard ? 0.75 : 1,
                              x: isActive ? 0 : activeCard ? `${offset * 110}%` : `${offset * 45}%`,
                              y: isActive ? 0 : activeCard ? 50 : 0,
                              rotate: isActive ? 0 : activeCard ? offset * 15 : offset * 3,
                              opacity: activeCard && !isActive ? 0.4 : 1,
                              filter: activeCard && !isActive ? "blur(3px)" : "none",
                            }}
                            transition={{
                              type: "spring",
                              stiffness: 260,
                              damping: 25,
                              mass: 1
                            }}
                            className="absolute cursor-pointer will-change-transform"
                          >
                            <div className={`p-4 sm:p-8 rounded-2xl parchment ${isActive ? "magical-border ring-4 ring-indigo-500/20" : "border border-amber-900/10"} w-[300px] sm:w-[500px] flex flex-col items-center justify-center`}>
                              <div className="mb-4 text-center">
                                <h3 className={`text-2xl font-bold ${isActive ? 'magical-text-gradient' : 'text-amber-900/80'}`}>{v.name}</h3>
                                <p className="text-[10px] text-amber-900/60 uppercase tracking-widest font-black">{v.sub}</p>
                              </div>
                              <NorthIndianChart
                                title=""
                                houses={mapBackEndToFrontEndHouses(v.id)}
                              />
                              {!activeCard && (
                                <div className="mt-6 flex flex-col items-center gap-1">
                                  <p className="text-[10px] font-bold text-amber-800/40 uppercase tracking-widest animate-pulse">Invoke Wisdom</p>
                                  <div className="w-12 h-1 bg-gradient-to-r from-transparent via-amber-500/20 to-transparent"></div>
                                </div>
                              )}
                            </div>
                          </motion.div>
                        );
                      })}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Predictions Reveal Section */}
                <div className="min-h-[500px] w-full">
                  <AnimatePresence mode="wait">
                    {!activeCard && (
                      <motion.div
                        key="select-prompt"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="text-center text-amber-200/50 italic text-xl font-serif mt-20"
                      >
                        Select a chart from the deck to reveal its secrets...
                      </motion.div>
                    )}

                    {activeCard === "D1" && (
                      <motion.div
                        key="d1-predictions"
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -30 }}
                        transition={{ duration: 0.5 }}
                        className="w-full"
                      >
                        {/* MOON PROFILE CARD (Classical / Vedic only) */}
                        {predictions.moon_profile && chartSystem === "vedic" && (
                          <div className="max-w-4xl mx-auto mb-12">
                            <div className="p-6 rounded-2xl bg-gradient-to-br from-indigo-900/30 to-purple-900/20 border border-indigo-500/30 shadow-xl space-y-5">
                              <h3 className="text-2xl font-semibold text-indigo-200 tracking-wider flex items-center gap-2">
                                🌙 Moon Profile — Nakshatra Attributes
                              </h3>
                              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4">
                                <div className="p-3 rounded-lg bg-slate-800/50 text-center">
                                  <p className="text-xs text-slate-400 uppercase tracking-widest">Nakshatra</p>
                                  <p className="text-lg font-bold text-amber-300 mt-1">{predictions.moon_profile.nakshatra}</p>
                                  <p className="text-xs text-slate-500">Pada {predictions.moon_profile.pada}</p>
                                </div>
                                <div className="p-3 rounded-lg bg-slate-800/50 text-center">
                                  <p className="text-xs text-slate-400 uppercase tracking-widest">Gana</p>
                                  <p className="text-lg font-bold text-emerald-300 mt-1">{predictions.moon_profile.gana}</p>
                                </div>
                                <div className="p-3 rounded-lg bg-slate-800/50 text-center">
                                  <p className="text-xs text-slate-400 uppercase tracking-widest">Varna</p>
                                  <p className="text-lg font-bold text-cyan-300 mt-1">{predictions.moon_profile.varna}</p>
                                </div>
                                <div className="p-3 rounded-lg bg-slate-800/50 text-center">
                                  <p className="text-xs text-slate-400 uppercase tracking-widest">Yoni</p>
                                  <p className="text-lg font-bold text-pink-300 mt-1">{predictions.moon_profile.yoni}</p>
                                </div>
                              </div>
                              <div className="space-y-3 text-sm">
                                {predictions.moon_profile.gana_description && (
                                  <div className="p-3 rounded-lg bg-slate-800/30">
                                    <span className="text-emerald-400 font-semibold">Gana ({predictions.moon_profile.gana}): </span>
                                    <span className="text-slate-300">{predictions.moon_profile.gana_description}</span>
                                  </div>
                                )}
                                {predictions.moon_profile.varna_description && (
                                  <div className="p-3 rounded-lg bg-slate-800/30">
                                    <span className="text-cyan-400 font-semibold">Varna ({predictions.moon_profile.varna}): </span>
                                    <span className="text-slate-300">{predictions.moon_profile.varna_description}</span>
                                  </div>
                                )}
                                {predictions.moon_profile.yoni_description && (
                                  <div className="p-3 rounded-lg bg-slate-800/30">
                                    <span className="text-pink-400 font-semibold">Yoni ({predictions.moon_profile.yoni}): </span>
                                    <span className="text-slate-300">{predictions.moon_profile.yoni_description}</span>
                                  </div>
                                )}
                                <div className="p-3 rounded-lg bg-slate-800/30">
                                  <span className="text-violet-400 font-semibold">Nadi: </span>
                                  <span className="text-slate-300">{predictions.moon_profile.nadi} (Ayurvedic Constitution)</span>
                                </div>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* INSIGHTS DASHBOARD — ALL 12 HOUSES (Classical / Vedic only) */}
                        {chartSystem === "vedic" && (
                          <div className="max-w-4xl mx-auto space-y-8">
                            <h3 className="text-2xl font-semibold text-amber-200 tracking-wider border-b border-slate-700/50 pb-4 mb-8">
                              Complete House Analysis (Bhava Vichar)
                            </h3>

                            {Object.entries(predictions)
                            .filter(([key]) => key.startsWith("house_"))
                            .sort(([a], [b]) => parseInt(a.split("_")[1]) - parseInt(b.split("_")[1]))
                            .map(([key, data]: [string, any]) => (
                              <div key={key} className="p-6 rounded-xl bg-slate-800/30 border border-slate-700/50 space-y-4">
                                <div>
                                  <h4 className="text-xl font-medium text-indigo-200">
                                    {data.house_name ? `House ${data.house} — ${data.house_name}` : `House ${data.house}`}
                                  </h4>
                                  {data.house_domain && (
                                    <p className="text-xs text-amber-400/70 uppercase tracking-widest mt-1">{data.house_domain}</p>
                                  )}
                                  {data.house_description && (
                                    <p className="text-sm text-slate-400 mt-2 leading-relaxed">{data.house_description}</p>
                                  )}
                                </div>

                                <div className="space-y-2 pt-2 border-t border-slate-700/30">
                                  {data.occupants?.length > 0 ? data.occupants.map((occ: any, i: number) => (
                                    <div key={i} className="flex gap-2">
                                      <span className="text-amber-400 font-bold shrink-0">{occ.planet} Placed:</span>
                                      <span className="text-slate-300">
                                        {occ.reading}
                                        {occ.is_combust && <span className="ml-2 text-red-400 text-xs font-semibold uppercase">🔥 Combust</span>}
                                      </span>
                                    </div>
                                  )) : (
                                    <p className="text-slate-500 text-sm italic">No planets occupy this house directly.</p>
                                  )}

                                  {data.lord_analysis && data.lord_analysis.lord && (
                                    <div className="flex gap-2">
                                      <span className="text-indigo-400 font-bold shrink-0">{data.lord_analysis.lord} (Lord):</span>
                                      <span className="text-slate-300">{data.lord_analysis.reading} (Placed in H{data.lord_analysis.placement_house} {data.lord_analysis.placement_sign})</span>
                                    </div>
                                  )}

                                  {data.aspects?.length > 0 && (
                                    <div className="flex gap-2">
                                      <span className="text-cyan-400 font-bold shrink-0">Aspects:</span>
                                      <span className="text-slate-300">Receiving aspect from {data.aspects.join(", ")}.</span>
                                    </div>
                                  )}
                                </div>
                              </div>
                            ))}

                          {/* Classical Yogas Section */}
                          {predictions.classical_yogas && predictions.classical_yogas.length > 0 && (
                            <div className="p-6 rounded-xl bg-gradient-to-br from-amber-900/20 to-indigo-900/20 border border-amber-500/30 space-y-4">
                              <h4 className="text-xl font-medium text-amber-300">✨ Classical Yogas Detected</h4>
                              <div className="space-y-3">
                                {predictions.classical_yogas.map((yoga: any, i: number) => (
                                  <div key={i} className="flex flex-col gap-1 p-3 rounded-lg bg-slate-800/40">
                                    <span className="text-amber-400 font-bold">{yoga.name}</span>
                                    <span className="text-slate-300 text-sm">{yoga.description}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                        )}

                        {/* ADVANCED JYOTISH SECTION (Classical / Vedic only) */}
                        {predictions.advanced_analysis && chartSystem === "vedic" && (
                          <AdvancedAnalysisSection advancedAnalysis={predictions.advanced_analysis} />
                        )}

                        {predictions.kp_analysis && chartSystem === "kp" && (
                          <KPDataSection kpAnalysis={predictions.kp_analysis} chartData={chartData} />
                        )}
                      </motion.div>
                    )}

                    {activeCard && activeCard !== "D1" && (
                      <motion.div
                        key={`${activeCard}-predictions`}
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -30 }}
                        transition={{ duration: 0.5 }}
                        className="max-w-4xl mx-auto space-y-8"
                      >
                        <div className="p-8 rounded-2xl parchment magical-border text-center space-y-6 shadow-2xl">
                          <h3 className="text-3xl font-serif text-amber-900 tracking-wider">
                            {activeCard === "D9" ? "Navamsa (D9) Revelations" : 
                             activeCard === "D2" ? "Hora (D2) Wealth Insights" : 
                             activeCard === "D12" ? "Dwadasamsa (D12) Lineage" : 
                             "Shastiamsa (D60) Soul Purpose"}
                          </h3>
                          <div className="w-16 h-px bg-amber-800/30 mx-auto"></div>
                          <p className="text-lg text-amber-950/80 italic leading-relaxed max-w-2xl mx-auto">
                            {getVargaDescription(activeCard)}
                          </p>

                          {/* Generalized Varga Planetary Mapping Table */}
                          <div className="mt-8 p-6 bg-white/40 rounded-xl border border-amber-800/20 text-left shadow-inner overflow-hidden">
                            <h4 className="text-xl font-bold text-amber-900 mb-4">{activeCard} Component Analysis</h4>
                            <div className="overflow-x-auto">
                              <table className="w-full text-sm text-left text-amber-950/80">
                                <thead className="text-xs text-amber-900 uppercase bg-amber-500/10 border-b border-amber-800/20">
                                  <tr>
                                    <th className="px-4 py-3 font-bold rounded-tl-lg">Planet</th>
                                    <th className="px-4 py-3 font-bold">D1 Rashi</th>
                                    <th className="px-4 py-3 font-bold">{activeCard} Sign</th>
                                    <th className="px-4 py-3 font-bold">Division</th>
                                    <th className="px-4 py-3 font-bold rounded-tr-lg">Notes</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  {/* Ascendant */}
                                  <tr className="border-b border-amber-800/10 bg-amber-50/30">
                                    <td className="px-4 py-3 font-bold">Ascendant</td>
                                    <td className="px-4 py-3">{chartData.ascendant.sign}</td>
                                    <td className="px-4 py-3 font-semibold text-amber-900">
                                      {getSignName(chartData.ascendant[`${activeCard.toLowerCase()}_sign_number`])}
                                    </td>
                                    <td className="px-4 py-3">{chartData.ascendant[`${activeCard.toLowerCase()}_sign_number`]}/
                                      {activeCard === "D2" ? "2" : activeCard === "D9" ? "9" : activeCard === "D12" ? "12" : "60"}
                                    </td>
                                    <td className="px-4 py-3">
                                      {activeCard === "D9" && chartData.ascendant.is_vargottama && <span className="inline-block px-2 py-0.5 mr-1 bg-amber-200 text-amber-800 rounded text-xs font-bold">⭐ VARGOTTAMA</span>}
                                    </td>
                                  </tr>

                                  {Object.entries(chartData.planets).map(([planet, p]: [string, any]) => (
                                    <tr key={planet} className="border-b border-amber-800/10 hover:bg-amber-100/40 transition-colors">
                                      <td className="px-4 py-3 font-bold">{planet}</td>
                                      <td className="px-4 py-3">{p.sign}</td>
                                      <td className="px-4 py-3 font-semibold text-amber-900">
                                        {p[`${activeCard.toLowerCase()}_sign`] || getSignName(p[`${activeCard.toLowerCase()}_sign_number`])}
                                      </td>
                                      <td className="px-4 py-3">{p[`${activeCard.toLowerCase()}_sign_number`]}/
                                        {activeCard === "D2" ? "2" : activeCard === "D9" ? "9" : activeCard === "D12" ? "12" : "60"}
                                      </td>
                                      <td className="px-4 py-3">
                                        {activeCard === "D9" && p.is_vargottama && <span className="inline-block px-2 py-0.5 mr-1 bg-amber-200 text-amber-800 rounded text-xs font-bold">⭐ VARGOTTAMA</span>}
                                        {activeCard === "D9" && p.is_navamsa_exalted && <span className="inline-block px-2 py-0.5 mr-1 bg-emerald-200 text-emerald-800 rounded text-xs font-bold">↑ EXALTED</span>}
                                        {activeCard === "D9" && p.is_navamsa_debilitated && <span className="inline-block px-2 py-0.5 bg-red-200 text-red-800 rounded text-xs font-bold">↓ DEBILITATED</span>}
                                      </td>
                                    </tr>
                                  ))}
                                </tbody>
                              </table>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>

        {/* --- EVENT SYNTHESIZER (LIFE EVENTS ORACLE) --- */}
        {predictions && predictions.event_synthesis && (
          <DeterministicDashboard eventSynthesis={predictions.event_synthesis} formData={lastSubmittedFormData} />
        )}

        {/* --- DASHA TIMELINE VIEW --- */}
        {predictions && predictions.dasha_timeline && (
          <TimelineView timeline={predictions.dasha_timeline} />
        )}

        {/* --- SAVE PROFILE ACTION --- */}
        {chartData && (
          <div className="mt-12 flex justify-center pb-20">
            <button
              onClick={() => {
                const profilePayload = {
                  ...lastSubmittedFormData,
                  preferred_system: "kp"
                };
                setPrimaryProfile(profilePayload);
                router.push("/dashboard");
              }}
              className="px-8 py-4 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold uppercase tracking-widest text-sm hover:scale-105 transition-all shadow-[0_0_30px_rgba(79,70,229,0.3)]"
            >
              Save as Primary Profile & View Dashboard
            </button>
          </div>
        )}

        {/* --- MAGICAL AI INSIGHTS --- */}
        {/* LOCAL AI INTERGRATION BLOCK (HIDDEN FOR DETERMINISTIC FREE TIER) */}
        {/* 
        <div className="mt-20 max-w-4xl mx-auto">
          <button onClick={handleGetAiReading} disabled={isAiLoading} className="w-full relative group overflow-hidden rounded-xl bg-gradient-to-r from-amber-500 to-indigo-600 p-[1px]">
            <div className="absolute inset-0 bg-gradient-to-r from-amber-500 to-indigo-600 opacity-70 group-hover:opacity-100 blur transition-opacity duration-300"></div>
            <div className="relative flex items-center justify-center gap-2 bg-slate-900/90 px-8 py-4 rounded-xl transition-all duration-300 group-hover:bg-opacity-0">
              <span className="font-bold text-white tracking-widest uppercase text-sm">
                {isAiLoading ? "Channeling AI Astrologer (Dolphin)..." : "Ask Local AI Astrologer (Dolphin)"}
              </span>
            </div>
          </button>
          {aiReading && (
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-12 p-10 rounded-2xl bg-slate-900/80 border border-indigo-500/30 shadow-2xl shadow-indigo-500/10 text-slate-200 leading-relaxed whitespace-pre-wrap font-serif text-lg">
              {aiReading}
            </motion.div>
          )}
        </div> 
        */}

                <div className="mt-20 flex justify-center pb-20">
                  <button
                    onClick={() => setChartData(null)}
                    className="px-6 py-2 rounded-full border border-slate-700 hover:border-amber-500/50 text-slate-400 hover:text-amber-100 transition-colors"
                  >
                    Calculate Another Chart
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

        </div>
      </div>
    </main>
  );
}
