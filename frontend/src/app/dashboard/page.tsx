"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { User, Plus, Trash2, Home } from "lucide-react";
import { useUser } from "@/context/UserContext";
import DailyTransitWidget from "@/components/ui/DailyTransitWidget";

export default function DashboardPage() {
  const { primaryProfile, savedMatches, removeMatch } = useUser();
  const router = useRouter();

  if (!primaryProfile) {
    return (
      <div className="min-h-screen bg-[#0b0c10] flex flex-col items-center justify-center text-center px-4">
        <h2 className="text-3xl font-bold text-white mb-4">No Profile Found</h2>
        <p className="text-slate-400 mb-8 max-w-md">You need to set up your primary profile to access the Personal Life OS dashboard.</p>
        <Link href="/" className="px-6 py-3 bg-indigo-600 text-white rounded-full font-bold hover:bg-indigo-700 transition-colors">
          Go to Home & Generate Profile
        </Link>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-[#0b0c10] text-slate-200 font-sans relative overflow-x-hidden pb-20">
      
      {/* Navbar/Header */}
      <nav className="w-full border-b border-white/5 bg-black/40 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 text-indigo-400 hover:text-indigo-300">
            <Home className="w-5 h-5" />
            <span className="font-bold tracking-widest text-sm uppercase">Astro-Naught</span>
          </Link>
          <div className="flex items-center gap-3 bg-slate-900 px-4 py-2 rounded-full border border-slate-800">
            <User className="w-4 h-4 text-slate-400" />
            <span className="text-sm font-medium">{primaryProfile.name}</span>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-12 space-y-12">
        
        {/* Loop 3: Daily Transits */}
        <section>
          <DailyTransitWidget />
        </section>

        {/* Loop 2: Saved Matches */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-white tracking-wide">Saved Matches</h2>
              <p className="text-slate-400 text-sm mt-1">Your personal relationship synastry leaderboard.</p>
            </div>
            <Link 
              href="/match" 
              className="flex items-center gap-2 px-4 py-2 bg-pink-500/20 text-pink-400 border border-pink-500/30 rounded-full hover:bg-pink-500/30 transition-colors text-sm font-bold uppercase tracking-widest"
            >
              <Plus className="w-4 h-4" /> Add Match
            </Link>
          </div>

          {savedMatches.length === 0 ? (
            <div className="p-12 border border-dashed border-slate-700 rounded-3xl flex flex-col items-center justify-center text-center bg-slate-900/30">
              <div className="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center mb-4">
                <User className="w-8 h-8 text-slate-500" />
              </div>
              <p className="text-slate-400">You haven't saved any compatibility matches yet.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {savedMatches.map((match, idx) => (
                <motion.div 
                  key={match.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-slate-900/60 border border-slate-800 rounded-2xl p-6 relative group overflow-hidden"
                >
                  <div className="flex justify-between items-start mb-6">
                    <div>
                      <h3 className="text-xl font-bold text-white">{match.name}</h3>
                      <p className="text-xs text-slate-500 mt-1">Saved: {match.date_saved}</p>
                    </div>
                    <div className="relative w-12 h-12 flex items-center justify-center rounded-full bg-slate-800 border border-indigo-500/30">
                      <svg className="absolute inset-0 w-full h-full transform -rotate-90">
                        <circle cx="24" cy="24" r="20" fill="none" stroke="currentColor" strokeWidth="4" className="text-slate-700" />
                        <circle 
                          cx="24" cy="24" r="20" 
                          fill="none" stroke="currentColor" strokeWidth="4" 
                          strokeDasharray="125.6" 
                          strokeDashoffset={125.6 - (125.6 * match.overall_score) / 100}
                          className="text-pink-500" 
                        />
                      </svg>
                      <span className="text-xs font-bold text-white relative z-10">{match.overall_score}%</span>
                    </div>
                  </div>

                  <div className="space-y-3 mb-6">
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Emotional</span>
                      <span className="text-pink-400 font-mono">{match.report.categories.emotional}%</span>
                    </div>
                    <div className="flex justify-between text-xs">
                      <span className="text-slate-400">Long-Term</span>
                      <span className="text-emerald-400 font-mono">{match.report.categories.long_term}%</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    <button 
                      onClick={() => removeMatch(match.id)}
                      className="p-2 text-slate-500 hover:text-red-400 hover:bg-red-400/10 rounded-lg transition-colors"
                      title="Remove Match"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <button 
                      onClick={() => router.push(`/match?id=${match.id}`)}
                      className="flex-1 py-2 text-center text-xs font-bold uppercase tracking-widest bg-slate-800 text-slate-300 hover:bg-slate-700 rounded-lg transition-colors"
                    >
                      View Details
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </section>

      </div>
    </main>
  );
}
