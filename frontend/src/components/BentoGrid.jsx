import React from 'react';
import { CheckCircle2, AlertTriangle, Quote } from 'lucide-react';
import { motion } from 'framer-motion';

export default function BentoGrid({ analysis, strengths, gaps }) {
    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">

            {/* 1. Análise Comparativa (Grande - Span 2) */}
            <div className="lg:col-span-2 bg-slate-900 rounded-3xl p-8 border border-slate-800 shadow-2xl relative overflow-hidden group hover:border-slate-700 transition-colors">
                <div className="absolute top-0 left-0 w-32 h-32 bg-blue-600/10 rounded-full blur-3xl -ml-10 -mt-10 group-hover:bg-blue-600/20 transition-colors duration-500" />
                <Quote className="w-12 h-12 text-slate-800 mb-6" />
                <h3 className="text-2xl font-bold text-white mb-6 relative z-10">Análise do Especialista</h3>
                <p className="text-slate-300 leading-relaxed text-lg whitespace-pre-wrap relative z-10 font-light">
                    {analysis}
                </p>
            </div>

            {/* 2. Coluna Lateral (Pontos Fortes & Gaps) */}
            <div className="space-y-8">

                {/* Pontos Fortes */}
                <div className="bg-slate-900 rounded-3xl p-8 border border-slate-800 shadow-2xl hover:border-slate-700 transition-colors relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/10 rounded-full blur-2xl -mr-10 -mt-10" />
                    <h4 className="text-emerald-400 font-bold mb-6 flex items-center gap-3 text-lg">
                        <CheckCircle2 className="w-6 h-6" /> Pontos Fortes
                    </h4>
                    <ul className="space-y-4">
                        {strengths.map((item, idx) => (
                            <motion.li
                                key={idx}
                                initial={{ opacity: 0, x: -10 }}
                                animate={{ opacity: 1, x: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                className="flex items-start gap-4 text-slate-300 text-sm font-medium"
                            >
                                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-emerald-400 flex-shrink-0 shadow-[0_0_8px_rgba(52,211,153,0.8)]" />
                                {item}
                            </motion.li>
                        ))}
                    </ul>
                </div>

                {/* Gaps (Estilo Alerta High Contrast) */}
                <div className="bg-brand-neon rounded-3xl p-8 shadow-[0_0_40px_rgba(163,230,53,0.2)] border border-lime-300 relative overflow-hidden">
                    <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-white/20 rounded-full blur-3xl" />
                    <h4 className="text-slate-950 font-extrabold mb-6 flex items-center gap-3 text-lg">
                        <AlertTriangle className="w-6 h-6 stroke-[2.5px]" /> Atenção Necessária
                    </h4>
                    <ul className="space-y-4 relative z-10">
                        {gaps.map((item, idx) => (
                            <li key={idx} className="flex items-start gap-4 text-slate-900 font-bold text-sm">
                                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-slate-950 flex-shrink-0" />
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>

            </div>
        </div>
    );
}
