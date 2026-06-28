/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable @typescript-eslint/no-unused-vars */

interface AdvancedAnalysisProps {
    advancedAnalysis: any;
}

export default function AdvancedAnalysisSection({ advancedAnalysis }: AdvancedAnalysisProps) {
    if (!advancedAnalysis) return null;

    // Gather all advanced yogas
    const allYogas = [
        ...(advancedAnalysis.panch_mahapurusha || []).map((y: any) => ({ ...y, type: "Panch Mahapurusha" })),
        ...(advancedAnalysis.dhana_yogas || []).map((y: any) => ({ ...y, type: "Dhana Yoga" })),
        ...(advancedAnalysis.raja_yogas || []).map((y: any) => ({ ...y, type: "Raja Yoga" })),
        ...(advancedAnalysis.viparita_raja_yogas || []).map((y: any) => ({ ...y, type: "Viparita Raja Yoga" })),
        ...(advancedAnalysis.neecha_bhanga || []).map((y: any) => ({ ...y, name: `Neecha Bhanga (${y.planet})`, description: y.reasons?.join("; "), type: "Neecha Bhanga" })),
        ...(advancedAnalysis.sun_yogas || []).map((y: any) => ({ ...y, type: "Sun Yoga" })),
        ...(advancedAnalysis.moon_yogas || []).map((y: any) => ({ ...y, type: "Moon Yoga" })),
        ...(advancedAnalysis.amala_yoga || []).map((y: any) => ({ ...y, description: `Benefics in the 10th from Moon/Lagna: ${y.planets?.join(", ")}`, type: "Amala Yoga" })),
    ];

    const manglik = advancedAnalysis.manglik_dosha;
    const kaalSarp = advancedAnalysis.kaal_sarp_dosha;
    const sadeSati = advancedAnalysis.sade_sati;

    return (
        <div className="max-w-4xl mx-auto space-y-8 mt-12">
            <h3 className="text-2xl font-semibold text-indigo-200 tracking-wider border-b border-indigo-700/50 pb-4 mb-8">
                Advanced Jyotish Insights
            </h3>

            {/* Dignities & Strengths */}
            <div className="p-6 rounded-xl bg-slate-800/30 border border-indigo-700/50 space-y-4">
                <h4 className="text-xl font-medium text-emerald-300">🪐 Planetary Strengths & Dignities</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {advancedAnalysis.planet_strengths?.map((p: any, i: number) => (
                        <div key={i} className="flex flex-col p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
                            <div className="flex justify-between items-center mb-1">
                                <span className="text-indigo-300 font-bold">{p.planet}</span>
                                <span className={`text-xs font-semibold px-2 py-0.5 rounded ${p.score >= 0 ? "bg-emerald-500/20 text-emerald-300" : "bg-red-500/20 text-red-300"}`}>
                                    Score: {p.score > 0 ? `+${p.score}` : p.score}
                                </span>
                            </div>
                            <span className="text-slate-200 font-medium mb-1">{p.disposition}</span>
                            {p.factors?.length > 0 && (
                                <ul className="text-xs text-slate-400 list-disc list-inside space-y-0.5">
                                    {p.factors.map((f: string, idx: number) => <li key={idx}>{f}</li>)}
                                </ul>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Doshas */}
            <div className="p-6 rounded-xl bg-slate-800/30 border border-red-700/50 space-y-4">
                <h4 className="text-xl font-medium text-red-300">⚠️ Dosha Analysis</h4>
                <div className="space-y-4">
                    {/* Manglik */}
                    <div className="p-4 rounded-lg bg-red-900/20 border border-red-800/30">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-lg font-bold text-red-200">Manglik Dosha</span>
                            <span className={`text-sm font-semibold px-2 py-1 rounded ${manglik?.is_manglik ? "bg-red-500/20 text-red-300" : "bg-emerald-500/20 text-emerald-300"}`}>
                                {manglik?.is_manglik ? "Present" : "Not Present"}
                            </span>
                        </div>
                        {manglik?.is_manglik && (
                            <div className="text-sm text-slate-300 space-y-1">
                                <p>Severity: <span className="font-semibold text-red-300">{manglik.severity}</span></p>
                                {manglik.is_cancelled && <p className="text-emerald-400 font-semibold text-xs mt-1">✓ Dosha is cancelled or neutralized in this chart.</p>}
                                {manglik.detailed_description && <p className="text-slate-400 mt-2 italic">{manglik.detailed_description}</p>}
                            </div>
                        )}
                    </div>

                    {/* Kaal Sarp */}
                    <div className="p-4 rounded-lg bg-orange-900/20 border border-orange-800/30">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-lg font-bold text-orange-200">Kaal Sarp Dosha</span>
                            <span className={`text-sm font-semibold px-2 py-1 rounded ${kaalSarp?.is_present ? "bg-orange-500/20 text-orange-300" : "bg-emerald-500/20 text-emerald-300"}`}>
                                {kaalSarp?.is_present ? "Present" : "Not Present"}
                            </span>
                        </div>
                        {kaalSarp?.is_present && (
                            <div className="text-sm text-slate-300 space-y-1">
                                <p>Type: <span className="font-semibold text-orange-300">{kaalSarp.type}</span></p>
                                {kaalSarp.detailed_description && <p className="text-slate-400 mt-2 italic">{kaalSarp.detailed_description}</p>}
                            </div>
                        )}
                    </div>

                    {/* Sade Sati */}
                    <div className="p-4 rounded-lg bg-purple-900/20 border border-purple-800/30">
                        <div className="flex justify-between items-center mb-2">
                            <span className="text-lg font-bold text-purple-200">Sade Sati (Natal)</span>
                            <span className={`text-sm font-semibold px-2 py-1 rounded ${sadeSati?.is_active ? "bg-purple-500/20 text-purple-300" : "bg-emerald-500/20 text-emerald-300"}`}>
                                {sadeSati?.is_active ? "Active" : "Not Active"}
                            </span>
                        </div>
                        {sadeSati?.is_active && (
                            <div className="text-sm text-slate-300 space-y-1">
                                <p>Phase: <span className="font-semibold text-purple-300">{sadeSati.phase}</span></p>
                                {sadeSati.detailed_description && <p className="text-slate-400 mt-2 italic">{sadeSati.detailed_description}</p>}
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Advanced Yogas */}
            {allYogas.length > 0 && (
                <div className="p-6 rounded-xl bg-gradient-to-br from-indigo-900/20 to-emerald-900/20 border border-emerald-500/30 space-y-4">
                    <h4 className="text-xl font-medium text-emerald-300">🌟 Advanced Yogas & Formations</h4>
                    <div className="space-y-3">
                        {allYogas.map((yoga: any, i: number) => (
                            <div key={i} className="flex flex-col gap-1 p-4 rounded-lg bg-slate-800/60 border border-slate-700/50 shadow-sm">
                                <div className="flex justify-between items-start">
                                    <span className="text-emerald-400 font-bold text-lg">{yoga.name}</span>
                                    <span className="text-xs font-semibold px-2 py-1 bg-slate-700 rounded text-slate-300 uppercase tracking-wider">{yoga.type}</span>
                                </div>
                                {yoga.planet && <p className="text-slate-300 text-sm font-medium">Formed by <span className="text-indigo-300">{yoga.planet}</span></p>}
                                <span className="text-slate-300 text-sm mt-1">{yoga.description || yoga.detailed_description}</span>
                                {yoga.detailed_description && !yoga.description && <span className="text-slate-400 text-xs mt-2 italic border-t border-slate-700/50 pt-2">{yoga.detailed_description}</span>}
                            </div>
                        ))}
                    </div>
                </div>
            )}

        </div>
    );
}
