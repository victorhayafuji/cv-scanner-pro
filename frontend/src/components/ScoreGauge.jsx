import React from 'react';
import { motion } from 'framer-motion';

export default function ScoreGauge({ score }) {
    // SVG Config
    const radius = 80;
    const stroke = 12;
    const normalizedRadius = radius - stroke * 2;
    const circumference = normalizedRadius * 2 * Math.PI;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
        <div className="flex flex-col items-center justify-center p-8 bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl relative overflow-hidden group hover:border-slate-700 transition-colors">
            {/* Ambient Glow */}
            <div className="absolute inset-0 bg-brand-neon/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700" />

            <div className="relative flex items-center justify-center">
                <svg
                    height={radius * 2}
                    width={radius * 2}
                    className="transform -rotate-90 drop-shadow-[0_0_10px_rgba(163,230,53,0.3)]"
                >
                    {/* Background Ring */}
                    <circle
                        stroke="#0f172a" // slate-900 (track needs to be darker/integrated)
                        strokeWidth={15}
                        fill="transparent"
                        r={normalizedRadius}
                        cx={radius}
                        cy={radius}
                        className="opacity-50"
                    />
                    <circle
                        stroke="#1e293b" // slate-800 (visible track)
                        strokeWidth={15}
                        fill="transparent"
                        r={normalizedRadius}
                        cx={radius}
                        cy={radius}
                    />
                    {/* Progress Ring */}
                    <motion.circle
                        stroke="#a3e635" // brand-neon
                        strokeWidth={15}
                        strokeDasharray={circumference + ' ' + circumference}
                        style={{ strokeDashoffset }}
                        strokeLinecap="round"
                        fill="transparent"
                        r={normalizedRadius}
                        cx={radius}
                        cy={radius}
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset }}
                        transition={{ duration: 1.5, ease: "easeOut" }}
                    />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <motion.span
                        className="text-4xl font-bold text-white tracking-tighter"
                        initial={{ opacity: 0, scale: 0.5 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.5, type: "spring" }}
                    >
                        {score}%
                    </motion.span>
                    <span className="text-xs text-brand-neon font-bold uppercase tracking-[0.2em] mt-1">Match</span>
                </div>
            </div>
            <h3 className="mt-6 text-slate-300 font-medium text-lg">Aderência à Vaga</h3>
        </div>
    );
}
