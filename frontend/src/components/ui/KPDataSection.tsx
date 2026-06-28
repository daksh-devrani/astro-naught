/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import { motion } from "framer-motion";
import { Table, Zap, Info } from "lucide-react";

interface KPDataSectionProps {
    kpAnalysis: any;
    chartData: any;
}

export default function KPDataSection({ kpAnalysis, chartData }: KPDataSectionProps) {
    if (!kpAnalysis || !chartData) return null;

    const significators = kpAnalysis.significators || {};
    const cusps = kpAnalysis.cusps || {};
    const planets = chartData.planets || {};

    return (
        <div className="max-w-6xl mx-auto space-y-12 mt-16 px-4">
            <div className="flex flex-col items-center mb-8">
                <h3 className="text-3xl font-black tracking-tighter magical-text-gradient mb-2 uppercase">
                    KP ASTROLOGY ENGINE
                </h3>
                <div className="h-1 w-32 bg-gradient-to-r from-amber-500 to-indigo-500 rounded-full"></div>
            </div>

            {/* 4-Level Significators */}
            <div className="p-8 rounded-2xl bg-slate-900/40 backdrop-blur-xl border border-indigo-500/30 shadow-2xl">
                <div className="flex items-center gap-3 mb-6">
                    <Zap className="w-6 h-6 text-amber-400" />
                    <h4 className="text-xl font-bold text-white tracking-wide">4-Level Significators Table</h4>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-indigo-500/20 text-indigo-300 text-xs uppercase tracking-widest">
                                <th className="py-4 px-4 font-black">House</th>
                                <th className="py-4 px-4 font-black">L1 (Star of Occ.)</th>
                                <th className="py-4 px-4 font-black">L2 (Occupant)</th>
                                <th className="py-4 px-4 font-black">L3 (Star of Owner)</th>
                                <th className="py-4 px-4 font-black">L4 (Owner)</th>
                            </tr>
                        </thead>
                        <tbody className="text-slate-200">
                            {Object.entries(significators).map(([num, sigs]: [string, any]) => (
                                <tr key={num} className="border-b border-slate-800/50 hover:bg-indigo-500/5 transition-colors">
                                    <td className="py-4 px-4 font-bold text-amber-400">House {num}</td>
                                    <td className="py-4 px-4 text-sm">{sigs.L1.join(", ") || "—"}</td>
                                    <td className="py-4 px-4 text-sm">{sigs.L2.join(", ") || "—"}</td>
                                    <td className="py-4 px-4 text-sm">{sigs.L3.join(", ") || "—"}</td>
                                    <td className="py-4 px-4 text-sm">{sigs.L4.join(", ") || "—"}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
                <p className="mt-4 text-[10px] text-slate-500 italic flex items-center gap-1">
                    <Info className="w-3 h-3" /> Note: L1 is the strongest significator in the KP system.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Cuspal Sub-lords */}
                <div className="p-6 rounded-2xl bg-slate-900/40 backdrop-blur-xl border border-slate-800 shadow-xl">
                    <h4 className="text-lg font-bold text-indigo-300 mb-6 flex items-center gap-2">
                        <Zap className="w-5 h-5" /> House Cusps (Placidus)
                    </h4>
                    <div className="space-y-3">
                        {Object.entries(cusps).map(([num, data]: [string, any]) => (
                            <div key={num} className="flex items-center justify-between p-3 rounded-lg bg-slate-800/30 border border-slate-700/50">
                                <div className="flex flex-col">
                                    <span className="text-xs font-bold text-slate-500 uppercase tracking-tighter">Cusp {num}</span>
                                    <span className="text-sm font-medium text-amber-200">{data.sign} {Math.floor(data.degree % 30)}°</span>
                                </div>
                                <div className="flex gap-4">
                                    <div className="flex flex-col items-center">
                                        <span className="text-[10px] text-slate-500 uppercase">Star</span>
                                        <span className="text-xs font-bold text-indigo-300">{data.star_lord}</span>
                                    </div>
                                    <div className="flex flex-col items-center">
                                        <span className="text-[10px] text-slate-500 uppercase">Sub</span>
                                        <span className="text-xs font-bold text-emerald-400">{data.sub_lord}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Planetary Sub-lords */}
                <div className="p-6 rounded-2xl bg-slate-900/40 backdrop-blur-xl border border-slate-800 shadow-xl">
                    <h4 className="text-lg font-bold text-indigo-300 mb-6 flex items-center gap-2">
                        <Zap className="w-5 h-5" /> Planetary Sub-lords
                    </h4>
                    <div className="grid grid-cols-1 gap-3">
                        {Object.entries(planets).map(([name, data]: [string, any]) => (
                            <div key={name} className="flex items-center justify-between p-3 rounded-lg bg-slate-800/30 border border-slate-700/50">
                                <div className="flex items-center gap-3">
                                    <span className="w-8 h-8 flex items-center justify-center rounded-full bg-indigo-500/10 text-indigo-400 font-bold text-xs ring-1 ring-indigo-500/20">
                                        {name.substring(0, 2)}
                                    </span>
                                    <span className="text-sm font-bold text-slate-200">{name}</span>
                                </div>
                                <div className="flex gap-6">
                                    <div className="flex flex-col items-center">
                                        <span className="text-[10px] text-slate-500 uppercase">Star</span>
                                        <span className="text-xs font-semibold text-indigo-400">{data.kp_star_lord}</span>
                                    </div>
                                    <div className="flex flex-col items-center">
                                        <span className="text-[10px] text-slate-500 uppercase">Sub</span>
                                        <span className="text-xs font-semibold text-emerald-400">{data.kp_sub_lord}</span>
                                    </div>
                                    <div className="flex flex-col items-center">
                                        <span className="text-[10px] text-slate-500 uppercase">Sub-Sub</span>
                                        <span className="text-xs font-semibold text-amber-500">{data.kp_sub_sub_lord}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
