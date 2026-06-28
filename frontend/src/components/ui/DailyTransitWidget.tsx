"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Sparkles, Calendar, Moon, Sun, Star } from "lucide-react";
import { useUser } from "@/context/UserContext";

export default function DailyTransitWidget() {
  const { primaryProfile } = useUser();
  const [transits, setTransits] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!primaryProfile) return;

    const fetchTransits = async () => {
      setIsLoading(true);
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/transits`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ person: primaryProfile })
        });
        if (res.ok) {
          const data = await res.json();
          setTransits(data);
        }
      } catch (err) {
        console.error("Failed to fetch transits", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchTransits();
  }, [primaryProfile]);

  if (!primaryProfile) return null;

  return (
    <div className="w-full bg-indigo-950/20 border border-indigo-500/30 rounded-3xl p-8 backdrop-blur-xl shadow-2xl relative overflow-hidden">
      
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>

      <div className="flex items-center gap-3 mb-8">
        <Sparkles className="w-6 h-6 text-indigo-400" />
        <h2 className="text-2xl font-bold text-white tracking-wide">Daily Celestial Transits</h2>
        {transits && (
          <span className="ml-auto text-xs font-mono text-indigo-300 uppercase tracking-widest bg-indigo-500/10 px-3 py-1 rounded-full border border-indigo-500/20 flex items-center gap-2">
            <Calendar className="w-3 h-3" />
            {transits.date}
          </span>
        )}
      </div>

      {isLoading ? (
        <div className="animate-pulse space-y-4">
          <div className="h-24 bg-slate-800/50 rounded-xl"></div>
          <div className="h-24 bg-slate-800/50 rounded-xl"></div>
        </div>
      ) : transits && transits.insights ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {transits.insights.map((insight: any, idx: number) => {
            let Icon = Star;
            let color = "text-indigo-400";
            let bg = "bg-indigo-500/10";
            let border = "border-indigo-500/20";
            
            if (insight.planet === "Moon") {
              Icon = Moon;
              color = "text-blue-400";
              bg = "bg-blue-500/10";
              border = "border-blue-500/20";
            } else if (insight.planet === "Sun") {
              Icon = Sun;
              color = "text-amber-400";
              bg = "bg-amber-500/10";
              border = "border-amber-500/20";
            }

            return (
              <motion.div 
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.1 }}
                className={`p-6 rounded-2xl ${bg} border ${border} flex flex-col gap-4`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-5 h-5 ${color}`} />
                  <div>
                    <h3 className={`font-bold ${color}`}>{insight.planet}</h3>
                    <p className="text-[10px] text-slate-400 uppercase tracking-widest">{insight.type}</p>
                  </div>
                </div>
                <p className="text-sm text-slate-300 leading-relaxed">
                  {insight.insight}
                </p>
              </motion.div>
            )
          })}
        </div>
      ) : (
        <p className="text-slate-400 text-sm">Unable to load transits today.</p>
      )}
    </div>
  );
}
