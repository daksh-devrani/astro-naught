import { useState } from "react";
import { motion } from "framer-motion";
import { Heart, Activity, MessageCircle, Link, Shield, Users, Save, Share2, Check } from "lucide-react";
import { useUser } from "@/context/UserContext";
import { useRouter } from "next/navigation";

interface CompatibilityDashboardProps {
  report: any;
  personAInfo: any;
  personBInfo: any;
  formData: any;
  isSharedView?: boolean;
}

export default function CompatibilityDashboard({ report, personAInfo, personBInfo, formData, isSharedView = false }: CompatibilityDashboardProps) {
  const { saveMatch } = useUser();
  const router = useRouter();
  const [isSharing, setIsSharing] = useState(false);
  const [shareSuccess, setShareSuccess] = useState(false);

  if (!report) return null;

  const handleShare = async () => {
    setIsSharing(true);
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const sourceCode = urlParams.get('ref');

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/share`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "match",
          input_payload: formData,
          result_payload: { match_report: report, person_a_info: personAInfo, person_b_info: personBInfo },
          source_report_code: sourceCode
        })
      });

      if (res.ok) {
        const data = await res.json();
        const shareUrl = `${window.location.origin}/r/${data.short_code}`;
        await navigator.clipboard.writeText(shareUrl);
        setShareSuccess(true);
        setTimeout(() => setShareSuccess(false), 3000);
      }
    } catch (err) {
      console.error("Failed to share match", err);
    } finally {
      setIsSharing(false);
    }
  };

  const categories = [
    { key: "emotional", title: "Emotional Connection", icon: <Heart className="w-5 h-5" />, color: "bg-pink-500", text: "text-pink-400" },
    { key: "communication", title: "Communication", icon: <MessageCircle className="w-5 h-5" />, color: "bg-blue-500", text: "text-blue-400" },
    { key: "physical", title: "Physical Attraction", icon: <Activity className="w-5 h-5" />, color: "bg-red-500", text: "text-red-400" },
    { key: "long_term", title: "Long-Term Stability", icon: <Shield className="w-5 h-5" />, color: "bg-emerald-500", text: "text-emerald-400" },
    { key: "family", title: "Values & Family", icon: <Users className="w-5 h-5" />, color: "bg-amber-500", text: "text-amber-400" },
  ];

  return (
    <div className="w-full max-w-5xl mx-auto px-4 sm:px-0 space-y-12 mt-12 mb-20 pb-10">
      
      {/* Header Profile Section */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center"
      >
        <div className="flex items-center justify-center gap-6 mb-6">
          <div className="text-right">
            <h2 className="text-3xl font-bold text-white">{personAInfo.name}</h2>
            <p className="text-indigo-300 text-sm uppercase tracking-widest">{personAInfo.ascendant} Ascendant</p>
          </div>
          <div className="p-4 rounded-full bg-slate-800/50 border border-slate-700 relative shadow-[0_0_40px_rgba(236,72,153,0.3)]">
            <Link className="w-6 h-6 text-pink-400" />
          </div>
          <div className="text-left">
            <h2 className="text-3xl font-bold text-white">{personBInfo.name}</h2>
            <p className="text-indigo-300 text-sm uppercase tracking-widest">{personBInfo.ascendant} Ascendant</p>
          </div>
        </div>

        {/* Overall Score */}
        <div className="mt-10 mb-12">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400 mb-4">Overall Compatibility</p>
          <div className="relative w-48 h-48 mx-auto flex items-center justify-center rounded-full bg-slate-900/50 border border-indigo-500/30 shadow-[0_0_60px_rgba(99,102,241,0.2)]">
            <svg className="absolute inset-0 w-full h-full transform -rotate-90">
              <circle cx="96" cy="96" r="88" fill="none" stroke="currentColor" strokeWidth="8" className="text-slate-800" />
              <circle 
                cx="96" cy="96" r="88" 
                fill="none" stroke="currentColor" strokeWidth="8" 
                strokeDasharray="552.92" 
                strokeDashoffset={552.92 - (552.92 * report.overall_score) / 100}
                className="text-indigo-500 transition-all duration-1000 ease-out" 
              />
            </svg>
            <div className="text-center">
              <span className="text-6xl font-black text-white">{report.overall_score}</span>
              <span className="text-2xl text-indigo-400">%</span>
            </div>
          </div>
        </div>

        {/* Ashtakoot 36 Gunas Scorecard */}
        {report.ashtakoot && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="mb-12 max-w-lg mx-auto bg-amber-950/20 border border-amber-500/30 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl"
          >
            <h3 className="text-lg font-bold text-amber-400 uppercase tracking-widest mb-6 flex justify-center items-center gap-2">
              <span className="h-px bg-amber-500/30 flex-1"></span>
              Vedic Ashtakoot Match
              <span className="h-px bg-amber-500/30 flex-1"></span>
            </h3>
            
            <div className="flex justify-center items-end gap-2 mb-8">
              <span className="text-7xl font-black text-white">{report.ashtakoot.total_score}</span>
              <span className="text-2xl text-amber-500/70 mb-2">/ 36 Gunas</span>
            </div>

            <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Varna (Ego)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.varna}/1</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Vashya (Attraction)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.vashya}/2</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Tara (Health)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.tara}/3</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Yoni (Physical)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.yoni}/4</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Maitri (Mental)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.graha_maitri}/5</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Gana (Temperament)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.gana}/6</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Bhakoot (Harmony)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.bhakoot}/7</span>
              </div>
              <div className="flex justify-between border-b border-slate-800 pb-1">
                <span className="text-slate-400">Nadi (Genetic)</span>
                <span className="text-amber-300 font-mono">{report.ashtakoot.breakdown.nadi}/8</span>
              </div>
            </div>
          </motion.div>
        )}
      </motion.div>

      {/* Metrics Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* Progress Bars */}
        <div className="p-6 sm:p-8 rounded-3xl bg-slate-900/60 border border-slate-800 backdrop-blur-xl shadow-2xl space-y-6">
          <h3 className="text-lg font-bold text-white uppercase tracking-widest mb-6">Alignment Breakdown</h3>
          {categories.map((cat, idx) => (
            <motion.div 
              key={cat.key} 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 + idx * 0.1 }}
              className="space-y-2"
            >
              <div className="flex justify-between items-center text-sm">
                <span className={`font-semibold flex items-center gap-2 ${cat.text}`}>
                  {cat.icon} {cat.title}
                </span>
                <span className="text-slate-300 font-mono">{report.categories[cat.key]}%</span>
              </div>
              <div className="h-3 w-full bg-slate-800 rounded-full overflow-hidden">
                <motion.div 
                  initial={{ width: 0 }}
                  animate={{ width: `${report.categories[cat.key]}%` }}
                  transition={{ duration: 1, delay: 0.5 + idx * 0.1 }}
                  className={`h-full ${cat.color} rounded-full`}
                />
              </div>
            </motion.div>
          ))}
        </div>

        {/* Narrative Strengths & Challenges */}
        <div className="space-y-6">
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="p-6 sm:p-8 rounded-3xl bg-indigo-950/20 border border-indigo-500/30 backdrop-blur-xl shadow-2xl"
          >
            <h3 className="text-lg font-bold text-indigo-300 uppercase tracking-widest mb-4 flex items-center gap-2">
              Top Strengths
            </h3>
            <ul className="space-y-3">
              {report.top_strengths.length > 0 ? report.top_strengths.map((str: string, i: number) => (
                <li key={i} className="text-slate-300 text-sm leading-relaxed flex items-start gap-2">
                  <span className="text-indigo-400 mt-0.5">✦</span> {str}
                </li>
              )) : (
                <li className="text-slate-500 italic text-sm">No major strengths detected.</li>
              )}
            </ul>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="p-6 sm:p-8 rounded-3xl bg-rose-950/20 border border-rose-500/30 backdrop-blur-xl shadow-2xl"
          >
            <h3 className="text-lg font-bold text-rose-300 uppercase tracking-widest mb-4 flex items-center gap-2">
              Potential Friction
            </h3>
            <ul className="space-y-3">
              {report.potential_challenges.length > 0 ? report.potential_challenges.map((chl: string, i: number) => (
                <li key={i} className="text-slate-300 text-sm leading-relaxed flex items-start gap-2">
                  <span className="text-rose-400 mt-0.5">◈</span> {chl}
                </li>
              )) : (
                <li className="text-slate-500 italic text-sm">No major friction detected.</li>
              )}
            </ul>
          </motion.div>

        </div>
      </div>

      {/* Actions */}
      <div className="pt-12 flex flex-col md:flex-row justify-center gap-4">
        {!isSharedView && (
          <>
            <button 
              onClick={() => {
                saveMatch({
                  id: Date.now().toString(),
                  name: personBInfo.name,
                  overall_score: report.overall_score,
                  report: report,
                  personInfo: formData.person_b,
                  date_saved: new Date().toLocaleDateString()
                });
                router.push("/dashboard");
              }}
              className="flex items-center justify-center gap-2 px-8 py-4 bg-indigo-600 hover:bg-indigo-500 text-white rounded-full font-bold uppercase tracking-widest text-sm transition-all shadow-[0_0_20px_rgba(79,70,229,0.4)]"
            >
              <Save className="w-5 h-5" /> Save Match to Dashboard
            </button>

            <button 
              onClick={handleShare}
              disabled={isSharing}
              className={`flex items-center justify-center gap-2 px-8 py-4 rounded-full font-bold uppercase tracking-widest text-sm transition-all shadow-[0_0_20px_rgba(236,72,153,0.4)] ${
                shareSuccess 
                  ? "bg-emerald-500 hover:bg-emerald-400 text-white" 
                  : "bg-pink-600 hover:bg-pink-500 text-white"
              }`}
            >
              {isSharing ? (
                <span className="animate-pulse">Generating Link...</span>
              ) : shareSuccess ? (
                <><Check className="w-5 h-5" /> Copied!</>
              ) : (
                <><Share2 className="w-5 h-5" /> Share Report</>
              )}
            </button>
          </>
        )}
      </div>
      
      {/* Footer Branding for Screenshot Sharing */}
      <div className="pt-12 text-center">
        <p className="text-[10px] text-slate-600 uppercase tracking-widest font-mono">
          Generated securely and deterministically with <span className="text-indigo-400 font-bold">Astro-Naught.com</span>
        </p>
      </div>
      
    </div>
  );
}
