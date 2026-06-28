"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import MatchForm from "@/components/ui/MatchForm";
import CompatibilityDashboard from "@/components/ui/CompatibilityDashboard";

export default function MatchPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [matchData, setMatchData] = useState<any>(null);
  const [submittedData, setSubmittedData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchMatch = async (formData: any) => {
    setIsLoading(true);
    setMatchData(null);
    setSubmittedData(formData);
    setError(null);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"}/api/v1/match`, {
        method: "POST", 
        headers: { "Content-Type": "application/json" }, 
        body: JSON.stringify(formData)
      });

      if (!res.ok) throw new Error("Failed to calculate synastry.");

      const data = await res.json();
      setMatchData(data);
    } catch (err: any) {
      setError(err.message || "An error occurred.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#0b0c10] text-slate-200 selection:bg-pink-500/30 font-sans relative overflow-x-hidden">
      {/* Magical Background Elements */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-[120px]"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-pink-500/10 rounded-full blur-[120px]"></div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        
        {/* Navigation */}
        <Link href="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors mb-12">
          <ArrowLeft className="w-4 h-4" />
          <span className="text-sm font-bold uppercase tracking-widest">Back to Individual Chart</span>
        </Link>

        {/* Dynamic Content Area */}
        <div className="flex flex-col items-center justify-center">

          <AnimatePresence mode="wait">
            {!matchData && (
              <motion.div key="form" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="w-full">
                <MatchForm onSubmit={fetchMatch} isLoading={isLoading} />
              </motion.div>
            )}

            {error && (
              <motion.div 
                key="error-msg"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="text-center p-8 rounded-xl bg-red-500/10 border border-red-500/20 max-w-md mt-10"
              >
                <p className="text-red-400 font-mono text-sm mb-4">{error}</p>
                <button 
                  onClick={() => { setError(null); }}
                  className="text-xs font-bold text-slate-400 hover:text-white underline tracking-widest uppercase"
                >
                  Try Again
                </button>
              </motion.div>
            )}

            {matchData && !isLoading && (
              <motion.div
                key="results"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
                className="w-full"
              >
                <CompatibilityDashboard 
                  report={matchData.match_report} 
                  personAInfo={matchData.person_a_info} 
                  personBInfo={matchData.person_b_info} 
                  formData={submittedData}
                />

                <div className="mt-12 flex justify-center pb-20">
                  <button
                    onClick={() => setMatchData(null)}
                    className="px-6 py-2 rounded-full border border-slate-700 hover:border-pink-500/50 text-slate-400 hover:text-pink-100 transition-colors"
                  >
                    Calculate Another Match
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
