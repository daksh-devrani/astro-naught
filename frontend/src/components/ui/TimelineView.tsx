import { motion } from "framer-motion";
import { Clock, Star, Calendar } from "lucide-react";
import { useState, useEffect } from "react";

interface Antardasha {
  lord: string;
  start: string;
  end: string;
}

interface Mahadasha {
  lord: string;
  start: string;
  end: string;
  antardashas: Antardasha[];
}

interface TimelineViewProps {
  timeline: Mahadasha[];
}

export default function TimelineView({ timeline }: TimelineViewProps) {
  const [currentDate, setCurrentDate] = useState<Date | null>(null);

  useEffect(() => {
    setCurrentDate(new Date());
  }, []);

  if (!timeline || timeline.length === 0 || !currentDate) return null;

  const isCurrentPeriod = (start: string, end: string) => {
    const startDate = new Date(start);
    const endDate = new Date(end);
    return currentDate >= startDate && currentDate < endDate;
  };

  const isPastPeriod = (end: string) => {
    const endDate = new Date(end);
    return currentDate >= endDate;
  };

  const getLordColor = (lord: string) => {
    switch (lord) {
      case "Sun": return "text-amber-500 border-amber-500 bg-amber-500/10";
      case "Moon": return "text-slate-300 border-slate-300 bg-slate-300/10";
      case "Mars": return "text-red-500 border-red-500 bg-red-500/10";
      case "Mercury": return "text-emerald-400 border-emerald-400 bg-emerald-400/10";
      case "Jupiter": return "text-yellow-400 border-yellow-400 bg-yellow-400/10";
      case "Venus": return "text-pink-400 border-pink-400 bg-pink-400/10";
      case "Saturn": return "text-blue-500 border-blue-500 bg-blue-500/10";
      case "Rahu": return "text-indigo-400 border-indigo-400 bg-indigo-400/10";
      case "Ketu": return "text-orange-500 border-orange-500 bg-orange-500/10";
      default: return "text-slate-400 border-slate-400 bg-slate-400/10";
    }
  };

  // Find the index of the active Mahadasha to auto-scroll or emphasize if needed
  const activeIndex = timeline.findIndex(md => isCurrentPeriod(md.start, md.end));

  return (
    <div className="w-full max-w-4xl mx-auto mt-20 mb-20">
      <div className="text-center mb-12">
        <h2 className="text-4xl font-light text-white font-serif flex items-center justify-center gap-4">
          <Clock className="w-8 h-8 text-indigo-400" />
          The Timeline (Dasha)
          <Clock className="w-8 h-8 text-indigo-400" />
        </h2>
        <p className="text-indigo-300/80 mt-4 tracking-wide max-w-xl mx-auto">
          Your 120-year chronological destiny map, highlighting the active chapters of your life.
        </p>
      </div>

      <div className="relative pl-4 md:pl-8">
        {/* The main vertical line */}
        <div className="absolute top-0 bottom-0 left-[26px] md:left-[42px] w-1 bg-gradient-to-b from-indigo-900/50 via-purple-500/30 to-indigo-900/50 rounded-full" />

        {timeline.map((md, idx) => {
          const isCurrentMd = isCurrentPeriod(md.start, md.end);
          const isPastMd = isPastPeriod(md.end);
          
          // We don't want to render the full 120 years un-collapsed, let's just render the current, past 1, and future 2 for clarity, 
          // or render all but collapse the antardashas for non-current ones.
          
          return (
            <motion.div 
              key={idx}
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ duration: 0.5, delay: idx * 0.05 }}
              className={`relative mb-12 ${isPastMd ? 'opacity-50' : 'opacity-100'}`}
            >
              {/* Timeline Node */}
              <div className={`absolute -left-2 md:-left-2 w-10 h-10 rounded-full flex items-center justify-center border-4 border-[#0b0c10] z-10 
                ${isCurrentMd ? 'bg-indigo-500 scale-125 shadow-[0_0_20px_rgba(99,102,241,0.6)]' : 'bg-slate-800'}`}
              >
                {isCurrentMd ? <Star className="w-5 h-5 text-white animate-pulse" /> : <Calendar className="w-4 h-4 text-slate-400" />}
              </div>

              {/* Mahadasha Card */}
              <div className={`ml-14 md:ml-20 p-6 rounded-2xl border transition-all duration-300
                ${isCurrentMd ? 'bg-indigo-900/20 border-indigo-500/50 shadow-lg' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`}
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-2">
                  <div className="flex items-center gap-3">
                    <h3 className="text-2xl font-bold text-white tracking-wider">
                      {md.lord} Mahadasha
                    </h3>
                    {isCurrentMd && (
                      <span className="px-3 py-1 bg-indigo-500 text-white text-xs font-bold uppercase tracking-widest rounded-full">
                        Active Now
                      </span>
                    )}
                  </div>
                  <div className="text-sm font-mono text-slate-400 bg-black/30 px-3 py-1 rounded-lg">
                    {new Date(md.start).toLocaleDateString('en-GB', {day: '2-digit', month: '2-digit', year: 'numeric'})} — {new Date(md.end).toLocaleDateString('en-GB', {day: '2-digit', month: '2-digit', year: 'numeric'})}
                  </div>
                </div>

                {/* Sub-periods (Antardashas) */}
                {/* Only show antardashas for the current Mahadasha to avoid overwhelming UI */}
                {isCurrentMd && (
                  <div className="mt-6 pt-6 border-t border-indigo-500/20">
                    <h4 className="text-sm font-bold text-indigo-300 uppercase tracking-widest mb-4">
                      Sub-Chapters (Antardashas)
                    </h4>
                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                      {md.antardashas.map((ad, adIdx) => {
                        const isCurrentAd = isCurrentPeriod(ad.start, ad.end);
                        const isPastAd = isPastPeriod(ad.end);
                        const lordColors = getLordColor(ad.lord);
                        
                        return (
                          <div 
                            key={adIdx}
                            className={`p-3 rounded-xl border flex flex-col gap-1 transition-all
                              ${isCurrentAd ? 'bg-indigo-500/20 border-indigo-400 shadow-inner scale-105 z-10' : 
                                isPastAd ? 'bg-black/20 border-slate-800/50 opacity-60' : 'bg-slate-800/30 border-slate-700/50'}`}
                          >
                            <div className="flex items-center justify-between">
                              <span className={`font-bold ${isCurrentAd ? 'text-indigo-200' : 'text-slate-300'}`}>
                                {ad.lord}
                              </span>
                              {isCurrentAd && <div className="w-2 h-2 rounded-full bg-indigo-400 animate-ping" />}
                            </div>
                            <span className="text-[10px] text-slate-400 font-mono">
                              {new Date(ad.start).toLocaleDateString('en-GB', {day: '2-digit', month: '2-digit', year: 'numeric'})} to {new Date(ad.end).toLocaleDateString('en-GB', {day: '2-digit', month: '2-digit', year: 'numeric'})}
                            </span>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          )
        })}
      </div>
    </div>
  );
}
