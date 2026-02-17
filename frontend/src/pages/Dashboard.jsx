import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import HeroSection from '../components/HeroSection';
import ScoreGauge from '../components/ScoreGauge';
import SkillBars from '../components/SkillBars';
import BentoGrid from '../components/BentoGrid';

export default function Dashboard() {
    const { logout, user } = useAuth();
    const [files, setFiles] = useState([]);
    const [vaga, setVaga] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFileSelect = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            setFiles(Array.from(e.target.files));
        }
    };

    const handleAnalyze = async () => {
        if (!files || files.length === 0) return;

        setLoading(true);
        setError('');

        try {
            let lastResult = null;

            for (const file of files) {
                const formData = new FormData();
                formData.append('arquivo', file);
                if (vaga) formData.append('vaga', vaga);

                // Axios uses the interceptor/default header set in AuthContext
                const response = await axios.post('http://127.0.0.1:8000/api/v1/analisar-cv/', formData);

                lastResult = response.data;
            }

            setResult(lastResult);
        } catch (err) {
            console.error(err);
            if (err.response && err.response.data && err.response.data.detail) {
                setError(err.response.data.detail);
            } else {
                setError('Erro ao processar o lote de currículos. Verifique se o backend está rodando e se você está logado.');
            }
            if (err.response && err.response.status === 401) {
                logout(); // Auto logout on 401
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100 font-sans selection:bg-brand-neon selection:text-slate-900 pb-20">

            {/* Header */}
            <header className="border-b border-slate-800 bg-slate-950/50 backdrop-blur-md sticky top-0 z-50">
                <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-lg bg-brand-neon flex items-center justify-center font-bold text-slate-900">
                            CV
                        </div>
                        <span className="font-bold text-lg tracking-tight">Engine Pro</span>
                    </div>
                    <nav className="text-sm font-medium text-slate-400 flex items-center gap-6">
                        <Link to="/analytics" className="hover:text-brand-neon transition-colors">
                            Analytics
                        </Link>
                        <div className="hidden md:block">Olá, {user?.email}</div>
                        <button onClick={logout} className="hover:text-red-400 transition-colors">
                            Sair
                        </button>
                    </nav>
                </div>
            </header>

            <main className="max-w-6xl mx-auto px-4 py-8 space-y-8">
                {/* Hero Section */}
                <HeroSection
                    files={files}
                    onFileSelect={handleFileSelect}
                    onVagaChange={setVaga}
                    onAnalyze={handleAnalyze}
                    loading={loading}
                />

                {/* Error Message */}
                {error && (
                    <div className="bg-red-500/10 border border-red-500/50 text-red-500 p-4 rounded-xl">
                        {error}
                    </div>
                )}

                {/* Loading State Skeleton */}
                {loading && !result && (
                    <div className="space-y-6 animate-pulse">
                        <div className="h-40 bg-slate-900 rounded-3xl" />
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div className="h-60 bg-slate-900 rounded-3xl" />
                            <div className="h-60 bg-slate-900 rounded-3xl" />
                        </div>
                    </div>
                )}

                {/* Results - Animate In */}
                <AnimatePresence>
                    {result && !loading && (
                        <motion.div
                            initial={{ opacity: 0, y: 40 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0 }}
                            className="space-y-8"
                        >
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                <div className="lg:col-span-1">
                                    <ScoreGauge score={result.match_percentual || 0} />
                                </div>
                                <div className="lg:col-span-2">
                                    <SkillBars
                                        technical={result.score_tecnico || 0}
                                        seniority={result.score_senioridade || 0}
                                        differential={result.score_diferencial || 0}
                                    />
                                </div>
                            </div>

                            <BentoGrid
                                analysis={result.analise_comparativa}
                                strengths={result.pontos_fortes || []}
                                gaps={result.gaps_tecnicos || []}
                            />
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
}
