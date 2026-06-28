import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, TrendingUp, AlertTriangle, CheckCircle, Share2, Check, X } from "lucide-react";

interface DeterministicDashboardProps {
  eventSynthesis: Record<string, any>;
  formData?: any;
  isSharedView?: boolean;
}

export default function DeterministicDashboard({ eventSynthesis, formData, isSharedView = false }: DeterministicDashboardProps) {
  const [isSharing, setIsSharing] = useState(false);
  const [shareSuccess, setShareSuccess] = useState(false);
  const [explainingTopic, setExplainingTopic] = useState<string | null>(null);
  const [explanationResult, setExplanationResult] = useState<string | null>(null);

  if (!eventSynthesis) return null;

  const handleExplain = async (topic: string, context: string) => {
    setExplainingTopic(topic);
    setExplanationResult(null);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/explain`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, context })
      });
      if (res.ok) {
        const data = await res.json();
        setExplanationResult(data.explanation);
      } else {
        setExplanationResult("The AI Translator is currently offline. Please configure the GEMINI_API_KEY.");
      }
    } catch (err) {
      setExplanationResult("Failed to connect to the AI Translator.");
    }
  };

  const handleShare = async () => {
    setIsSharing(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/share`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "synthesis",
          input_payload: formData,
          result_payload: { eventSynthesis }
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
      console.error("Failed to share", err);
    } finally {
      setIsSharing(false);
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto space-y-8 mt-12">
      <div className="text-center mb-10">
        <div className="flex justify-center mb-4">
          {!isSharedView && (
            <button 
              onClick={handleShare}
              disabled={isSharing}
              className={`flex items-center gap-2 px-6 py-2 rounded-full font-bold uppercase tracking-widest text-xs transition-all shadow-lg ${
                shareSuccess 
                  ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/50" 
                  : "bg-white/5 border border-white/10 text-white hover:bg-white/10"
              }`}
            >
              {isSharing ? (
                <span className="animate-pulse">Generating Link...</span>
              ) : shareSuccess ? (
                <><Check className="w-4 h-4" /> Copied!</>
              ) : (
                <><Share2 className="w-4 h-4" /> Share Report</>
              )}
            </button>
          )}
        </div>
        <h2 className="text-4xl md:text-5xl font-light text-white font-serif flex items-center justify-center gap-4">
          <Sparkles className="w-8 h-8 text-amber-400" />
          The Astrologer&apos;s Oracle
          <Sparkles className="w-8 h-8 text-amber-400" />
        </h2>
        <p className="text-indigo-300/80 mt-4 tracking-wide max-w-2xl mx-auto">
          Deterministic analysis driven by classical rules and exact mathematical cusps.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {Object.entries(eventSynthesis).map(([key, event]: [string, any], index: number) => (
          <motion.div
            key={key}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
            className="p-6 md:p-8 rounded-2xl bg-black/40 backdrop-blur-xl border border-white/10 shadow-2xl relative overflow-hidden group"
          >
            {/* Subtle Gradient Glow */}
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />

            <div className="flex justify-between items-start mb-6 relative z-10">
              <h3 className="text-2xl font-semibold text-white tracking-wide">{event.topic}</h3>
              <div className="flex flex-col items-end gap-1">
                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${event.confidence_score >= 0.8 ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : event.confidence_score >= 0.5 ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'}`}>
                  {Math.round(event.confidence_score * 100)}% Confidence
                </span>
              </div>
            </div>

            <div className="space-y-6 relative z-10">
              {/* Strengths */}
              {event.reasoning && event.reasoning.length > 0 && (
                <div className="space-y-2">
                  <div className="flex items-center gap-2 text-indigo-300 mb-2">
                    <CheckCircle className="w-4 h-4" />
                    <h4 className="text-sm font-bold uppercase tracking-widest">Strengths & Indicators</h4>
                  </div>
                  <div className="p-4 rounded-xl bg-indigo-950/30 border border-indigo-500/20">
                    <ul className="space-y-2">
                      {event.reasoning.map((r: string, i: number) => (
                        <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                          <span className="text-indigo-400 mt-1">✦</span>
                          <span className="leading-relaxed">{r}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* Ideal Path vs Pitfalls */}
              <div className="grid grid-cols-1 gap-4 mt-2">
                {event.path_a && (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-emerald-400 mb-2">
                      <TrendingUp className="w-4 h-4" />
                      <h4 className="text-sm font-bold uppercase tracking-widest">Ideal Path</h4>
                    </div>
                    <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/20 text-slate-300 text-sm leading-relaxed">
                      {event.path_a}
                    </div>
                  </div>
                )}
                
                {event.path_b && (
                  <div className="space-y-2 mt-2">
                    <div className="flex items-center gap-2 text-rose-400 mb-2">
                      <AlertTriangle className="w-4 h-4" />
                      <h4 className="text-sm font-bold uppercase tracking-widest">Pitfalls to Avoid</h4>
                    </div>
                    <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-500/20 text-slate-300 text-sm leading-relaxed">
                      {event.path_b}
                    </div>
                  </div>
                )}
              </div>
              
              <button 
                onClick={() => handleExplain(event.topic, event.reasoning?.join(" ") || "")}
                className="mt-6 flex items-center justify-center gap-2 w-full py-2 bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 rounded-lg text-indigo-300 text-xs uppercase tracking-widest font-bold transition-colors"
              >
                <Sparkles className="w-4 h-4" /> Explain This
              </button>
            </div>
            
            {/* Technical Metadata Footer */}
            {event.technical_details && (
              <div className="mt-8 pt-4 border-t border-white/5 text-[10px] text-slate-500 font-mono uppercase tracking-tighter opacity-60">
                Data: {event.technical_details} | KP: {event.kp_verdict}
              </div>
            )}
          </motion.div>
        ))}
      </div>

      {/* AI Explanation Modal */}
      <AnimatePresence>
        {explainingTopic && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm"
          >
            <motion.div 
              initial={{ scale: 0.95, y: 20 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.95, y: 20 }}
              className="bg-slate-900 border border-indigo-500/30 p-8 rounded-2xl shadow-2xl max-w-lg w-full relative"
            >
              <button 
                onClick={() => setExplainingTopic(null)}
                className="absolute top-4 right-4 text-slate-400 hover:text-white"
              >
                <X className="w-6 h-6" />
              </button>
              
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-indigo-500/20 rounded-lg">
                  <Sparkles className="w-6 h-6 text-indigo-400" />
                </div>
                <h3 className="text-xl font-bold text-white capitalize">
                  Explaining: {explainingTopic.replace("_", " ")}
                </h3>
              </div>

              {!explanationResult ? (
                <div className="flex flex-col items-center justify-center py-12 gap-4">
                  <div className="w-8 h-8 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
                  <p className="text-slate-400 text-sm font-medium animate-pulse">Translating astrological math...</p>
                </div>
              ) : (
                <div className="text-slate-200 leading-relaxed text-lg font-serif bg-indigo-950/30 p-6 rounded-xl border border-indigo-500/20">
                  {explanationResult}
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
