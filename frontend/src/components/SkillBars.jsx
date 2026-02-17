import React from 'react';
import { motion } from 'framer-motion';

export default function SkillBars({ technical, seniority, differential }) {
    const metrics = [
        { label: "Hard Skills", value: technical, max: 50, color: "bg-brand-accent" },
        { label: "Senioridade", value: seniority, max: 30, color: "bg-purple-500" },
        { label: "Diferenciais", value: differential, max: 20, color: "bg-pink-500" },
    ];

    return (
        <div className="flex flex-col justify-center gap-8 p-8 bg-slate-900 rounded-3xl border border-slate-800 shadow-2xl h-full">
            {metrics.map((metric, index) => {
                const percentage = (metric.value / metric.max) * 100;

                return (
                    <div key={metric.label} className="w-full space-y-3">
                        <div className="flex justify-between items-end">
                            <span className="text-sm font-semibold text-slate-400 uppercase tracking-wider">{metric.label}</span>
                            <div className="flex items-baseline gap-1">
                                <span className="text-xl font-bold text-white">{metric.value}</span>
                                <span className="text-sm text-slate-600 font-medium">/{metric.max}</span>
                            </div>
                        </div>
                        <div className="w-full bg-slate-950 rounded-full h-3 p-[2px] shadow-inner border border-slate-800/50">
                            <motion.div
                                className={`h-full rounded-full ${metric.color} shadow-[0_0_10px_currentColor]`}
                                initial={{ width: 0 }}
                                animate={{ width: `${percentage}%` }}
                                transition={{ duration: 1, delay: index * 0.2, type: "spring" }}
                            />
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
