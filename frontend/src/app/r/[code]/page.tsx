"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { Sparkles, Heart } from "lucide-react";
import DeterministicDashboard from "@/components/ui/DeterministicDashboard";
import CompatibilityDashboard from "@/components/ui/CompatibilityDashboard";
import { LoadingSpinner } from "@/components/ui/Loading";

export default function SharedReportPage() {
  const params = useParams();
  const router = useRouter();
  const code = params.code as string;

  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [reportData, setReportData] = useState<any>(null);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/v1/share/${code}`);
        if (!res.ok) {
          throw new Error("Report not found or has expired.");
        }
        const data = await res.json();
        setReportData(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    if (code) {
      fetchReport();
    }
  }, [code]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0b0c10] flex items-center justify-center">
        <LoadingSpinner message="Loading Shared Cosmic Blueprint..." />
      </div>
    );
  }

  if (error || !reportData) {
    return (
      <div className="min-h-screen bg-[#0b0c10] flex flex-col items-center justify-center text-center px-4">
        <h2 className="text-3xl font-bold text-white mb-4">Report Not Found</h2>
        <p className="text-slate-400 mb-8 max-w-md">{error || "This shared link is invalid."}</p>
        <Link href="/" className="px-6 py-3 bg-indigo-600 text-white rounded-full font-bold hover:bg-indigo-700 transition-colors">
          Go to Home
        </Link>
      </div>
    );
  }

  const { type, result_payload, input_payload, views } = reportData;

  return (
    <main className="min-h-screen bg-[#0b0c10] text-slate-200 font-sans relative overflow-x-hidden pb-20">
      
      {/* Sticky Conversion Banner */}
      <div className="sticky top-0 z-50 w-full bg-indigo-900/90 backdrop-blur-xl border-b border-indigo-500/30 text-white px-4 py-3 shadow-2xl">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-amber-400" />
            <span className="text-sm font-medium">Someone shared an Astro-Naught report with you.</span>
          </div>
          <Link 
            href={`/?ref=${code}`}
            className="whitespace-nowrap px-4 py-2 bg-white text-indigo-900 font-bold rounded-full text-xs uppercase tracking-widest hover:bg-indigo-50 transition-colors"
          >
            {type === 'match' ? 'See Your Compatibility →' : 'See Your Career Timeline →'}
          </Link>
        </div>
      </div>

      <div className="pt-8">
        {type === "single" && result_payload.chartData && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-10">
              <h2 className="text-4xl font-bold text-amber-50 tracking-wider">
                {result_payload.chartData.personal_info.name}
              </h2>
              <div className="mt-2 text-indigo-300/80 text-sm tracking-widest uppercase flex justify-center gap-4">
                <span>{result_payload.chartData.personal_info.gender}</span>
                <span>•</span>
                <span>{result_payload.chartData.ascendant.sign} Ascendant</span>
              </div>
            </div>
          </div>
        )}

        {type === "single" && result_payload.eventSynthesis && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
             <DeterministicDashboard 
               eventSynthesis={result_payload.eventSynthesis} 
               isSharedView={true} 
             />
          </div>
        )}

        {type === "synthesis" && result_payload.eventSynthesis && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
             <DeterministicDashboard 
               eventSynthesis={result_payload.eventSynthesis} 
               isSharedView={true} 
             />
          </div>
        )}

        {type === "match" && result_payload.match_report && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
             <div className="text-center mb-8">
                <h2 className="text-3xl font-light text-white font-serif flex items-center justify-center gap-3">
                  <Heart className="w-6 h-6 text-pink-500" />
                  Synastry Result
                  <Heart className="w-6 h-6 text-pink-500" />
                </h2>
              </div>
             <CompatibilityDashboard 
               report={result_payload.match_report}
               personAInfo={result_payload.person_a_info}
               personBInfo={result_payload.person_b_info}
               formData={input_payload}
               isSharedView={true} 
             />
          </div>
        )}
      </div>

      {/* Creator View Stats (Ideally we'd check if they are the creator, but we can just show it at the bottom for now) */}
      <div className="max-w-7xl mx-auto px-4 mt-20 text-center border-t border-white/5 pt-8">
        <p className="text-xs font-mono text-slate-500 uppercase tracking-widest">
          Report Views: <span className="text-indigo-400 font-bold">{views}</span>
        </p>
      </div>

    </main>
  );
}
