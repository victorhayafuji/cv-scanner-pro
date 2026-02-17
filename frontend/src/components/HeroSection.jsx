import React, { useRef } from 'react';
import { Upload, FileText, ArrowRight, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

export default function HeroSection({ onFileSelect, onVagaChange, onAnalyze, files, loading }) {
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            // Passa o evento ou os arquivos diretamente, dependendo do contrato. 
            // O App.jsx espera o evento no handled proposto? 
            // O prompt diz: "const handleFileSelect = (e) => { ... }" setando array.
            // Então aqui vamos passar o evento original para manter a assinatura esperada pelo pai.
            onFileSelect(e);
        }
    };

    return (
        <div className="relative overflow-hidden bg-slate-900 rounded-3xl p-8 shadow-2xl border border-slate-800">
            {/* Background Glow */}
            <div className="absolute top-0 right-0 -mr-20 -mt-20 w-80 h-80 bg-brand-neon/10 rounded-full blur-[100px]" />

            <div className="relative z-10 flex flex-col md:flex-row gap-8 items-center">
                {/* Left: Content */}
                <div className="flex-1 space-y-6">
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-brand-neon text-sm font-medium"
                    >
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-neon opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-neon"></span>
                        </span>
                        Enterprise AI Screening v3.0
                    </motion.div>

                    <h1 className="text-5xl md:text-6xl font-bold text-white tracking-tighter leading-tight">
                        Triagem Inteligente <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-neon to-emerald-400">
                            de Talentos
                        </span>
                    </h1>

                    <p className="text-slate-400 text-lg max-w-md">
                        Faça o upload de lotes de currículos, defina os requisitos e receba o ranking dos melhores candidatos em segundos.
                    </p>

                    <div className="space-y-4">
                        {/* Vaga Input */}
                        <div className="relative group">
                            <div className="absolute inset-0 bg-gradient-to-r from-brand-neon/20 to-blue-600/20 rounded-xl blur opacity-0 group-hover:opacity-100 transition duration-500" />
                            <textarea
                                placeholder="Cole a Job Description completa (Requisitos Técnicos, Senioridade e Stack)..."
                                className="relative w-full bg-slate-950 border border-slate-800 text-slate-300 rounded-xl p-4 focus:outline-none focus:ring-2 focus:ring-brand-neon/50 resize-none h-32"
                                onChange={(e) => onVagaChange(e.target.value)}
                            />
                        </div>

                        {/* Actions */}
                        <div className="flex flex-col sm:flex-row gap-4">
                            <input
                                type="file"
                                ref={fileInputRef}
                                className="hidden"
                                accept=".pdf"
                                multiple
                                onChange={handleFileChange}
                            />

                            <button
                                onClick={() => fileInputRef.current?.click()}
                                className={`flex items-center justify-center gap-2 px-6 py-4 rounded-xl border border-dashed border-slate-600 hover:border-brand-neon hover:bg-slate-800/50 transition-all group ${files && files.length > 0 ? 'border-brand-neon bg-brand-neon/10' : ''}`}
                            >
                                {files && files.length > 0 ? (
                                    <>
                                        <FileText className="w-5 h-5 text-brand-neon" />
                                        <span className="text-slate-200 font-medium whitespace-nowrap">📄 {files.length} currículos selecionados</span>
                                    </>
                                ) : (
                                    <>
                                        <Upload className="w-5 h-5 text-slate-400 group-hover:text-brand-neon" />
                                        <span className="text-slate-400 group-hover:text-slate-200">Upload PDFs</span>
                                    </>
                                )}
                            </button>

                            <button
                                onClick={onAnalyze}
                                disabled={!files || files.length === 0 || loading}
                                className="flex-1 flex items-center justify-center gap-2 bg-brand-neon hover:bg-lime-300 active:scale-95 text-slate-900 font-bold py-4 px-8 rounded-full transition-all transform disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_30px_rgba(163,230,53,0.3)] hover:shadow-[0_0_50px_rgba(163,230,53,0.5)]"
                            >
                                {loading ? (
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                ) : (
                                    <>
                                        Processar Lote
                                        <ArrowRight className="w-5 h-5" />
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Right: Illustration (Ranked List Mockup) */}
                <div className="hidden md:flex flex-1 justify-center items-center relative">
                    <div className="relative w-72 bg-slate-900 rounded-2xl border border-slate-700 shadow-2xl p-6 transform rotate-[-3deg]">
                        {/* Header do Mockup */}
                        <div className="flex justify-between items-center mb-6 border-b border-slate-800 pb-4">
                            <span className="text-slate-400 text-xs uppercase tracking-wider">Top Candidates</span>
                            <span className="text-brand-neon text-xs font-bold">AI Ranking</span>
                        </div>

                        {/* Lista de Candidatos */}
                        <div className="space-y-4">
                            {/* Candidato 1 */}
                            <div className="flex items-center gap-3 p-2 bg-slate-800/50 rounded-lg border border-brand-neon/30">
                                <div className="w-8 h-8 rounded-full bg-brand-neon/20 flex items-center justify-center text-brand-neon text-xs font-bold">AS</div>
                                <div className="flex-1">
                                    <div className="h-2 w-20 bg-slate-600 rounded mb-1"></div>
                                    <div className="h-1.5 w-12 bg-slate-700 rounded"></div>
                                </div>
                                <span className="text-brand-neon font-bold text-sm">98%</span>
                            </div>

                            {/* Candidato 2 */}
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-slate-400 text-xs">JS</div>
                                <div className="flex-1">
                                    <div className="h-2 w-16 bg-slate-700 rounded mb-1"></div>
                                    <div className="h-1.5 w-10 bg-slate-800 rounded"></div>
                                </div>
                                <span className="text-blue-500 font-bold text-sm">85%</span>
                            </div>

                            {/* Candidato 3 (Adicionado conforme instructions) */}
                            <div className="flex items-center gap-3 p-2">
                                <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-slate-400 text-xs">CM</div>
                                <div className="flex-1">
                                    <div className="h-2 w-14 bg-slate-700 rounded mb-1"></div>
                                    <div className="h-1.5 w-8 bg-slate-800 rounded"></div>
                                </div>
                                <span className="text-slate-500 font-bold text-sm">71%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
