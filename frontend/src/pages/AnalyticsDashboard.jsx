import React, { useMemo, useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function AnalyticsDashboard() {
    const { user } = useAuth();
    const [rawData, setRawData] = useState([]);
    const [year, setYear] = useState(2025);
    const [startMonth, setStartMonth] = useState(1);
    const [endMonth, setEndMonth] = useState(12);
    const [loading, setLoading] = useState(true);

    // 1. Fetch Full Data
    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/v1/dashboard/metrics')
            .then(res => {
                setRawData(res.data.all_records || []);
                setLoading(false);
            })
            .catch(err => {
                console.error("Erro ao buscar dados analytics:", err);
                setLoading(false);
            });
    }, []);

    // 2. Client-Side Processing
    const processedData = useMemo(() => {
        if (!rawData.length) return { monthly: [], byRole: [], bySeniority: [], kpi: {}, filtered: [] };

        // Validar Range
        const safeStart = Math.min(startMonth, endMonth);
        const safeEnd = Math.max(startMonth, endMonth);

        const filtered = rawData.filter(d => {
            if (!d.data_analise) return false;
            const date = new Date(d.data_analise);
            const month = date.getMonth() + 1;
            return date.getFullYear() === year && (month >= safeStart && month <= safeEnd);
        });

        // KPI Calc
        const total = filtered.length;
        const avgScore = total ? (filtered.reduce((acc, cur) => acc + (cur.score_aderencia || 0), 0) / total).toFixed(1) : 0;
        const approved = filtered.filter(d => (d.score_aderencia || 0) >= 80).length;
        const approvalRate = total ? ((approved / total) * 100).toFixed(1) : 0;

        // Monthly Grouping
        const monthlyData = Array.from({ length: 12 }, (_, i) => {
            const monthNum = i + 1;
            // Mostra apenas meses dentro do range selecionado no gráfico?
            // O usuário pediu slicer de intervalo. Vamos filtrar o gráfico também ou mostrar tudo vazio?
            // Geralmente dashboards mostram apenas o período filtrado.
            if (monthNum < safeStart || monthNum > safeEnd) return null;

            const monthRecs = filtered.filter(d => new Date(d.data_analise).getMonth() + 1 === monthNum);
            const count = monthRecs.length;
            const avg = count ? (monthRecs.reduce((a, b) => a + (b.score_aderencia || 0), 0) / count).toFixed(1) : 0;
            return {
                name: new Date(0, i).toLocaleString('default', { month: 'short' }),
                count,
                score: parseFloat(avg)
            };
        }).filter(Boolean); // Remove meses fora do range

        // Grouping by Role (Cargo) - Top 5
        const roleStats = filtered.reduce((acc, cur) => {
            const role = cur.cargo_alvo || "Desconhecido";
            if (!acc[role]) acc[role] = { count: 0, sumScore: 0 };
            acc[role].count += 1;
            acc[role].sumScore += (cur.score_aderencia || 0);
            return acc;
        }, {});

        const byRole = Object.entries(roleStats)
            .map(([role, stats]) => ({
                role,
                count: stats.count,
                avg: (stats.sumScore / stats.count).toFixed(1)
            }))
            .sort((a, b) => b.count - a.count)
            .slice(0, 5);

        // Grouping by Seniority
        const senStats = filtered.reduce((acc, cur) => {
            const sen = cur.nivel_senioridade || "N/A";
            if (!acc[sen]) acc[sen] = { count: 0, sumScore: 0 };
            acc[sen].count += 1;
            acc[sen].sumScore += (cur.score_aderencia || 0);
            return acc;
        }, {});

        const bySeniority = Object.entries(senStats)
            .map(([sen, stats]) => ({
                seniority: sen,
                count: stats.count,
                avg: (stats.sumScore / stats.count).toFixed(1)
            }))
            .sort((a, b) => b.avg - a.avg);

        return { kpi: { total, avgScore, approvalRate }, filtered, monthly: monthlyData, byRole, bySeniority };
    }, [rawData, year, startMonth, endMonth]);

    const renderClassificacao = (score) => {
        if (score >= 90) return <span className="text-yellow-400 font-bold flex items-center gap-1">⭐ Elite</span>;
        if (score >= 80) return <span className="text-blue-400 font-medium">✅ Qualificado</span>;
        return <span className="text-slate-500">Em Desenvolvimento</span>;
    };

    const months = [
        { v: 1, l: 'Jan' }, { v: 2, l: 'Fev' }, { v: 3, l: 'Mar' }, { v: 4, l: 'Abr' },
        { v: 5, l: 'Mai' }, { v: 6, l: 'Jun' }, { v: 7, l: 'Jul' }, { v: 8, l: 'Ago' },
        { v: 9, l: 'Set' }, { v: 10, l: 'Out' }, { v: 11, l: 'Nov' }, { v: 12, l: 'Dez' }
    ];

    if (loading) return <div className="min-h-screen bg-[#0B1120] flex items-center justify-center text-white">Carregando Analytics...</div>;

    return (
        <div className="min-h-screen bg-[#0B1120] text-white p-6 font-sans">
            {/* Header & Filters */}
            <div className="flex flex-col md:flex-row justify-between items-center mb-8 bg-slate-800/50 p-4 rounded-xl border border-slate-700 gap-4">

                <div className="flex items-center gap-4">
                    <Link to="/" className="p-2 hover:bg-slate-700 rounded-full transition-colors text-slate-400 hover:text-white">
                        <ArrowLeft size={24} />
                    </Link>
                    <div>
                        <h1 className="text-2xl font-semibold">Analytics | <span className="text-slate-400">Visão Geral</span></h1>
                        {user && <span className="text-xs text-slate-500">Logado como: {user.email}</span>}
                    </div>
                </div>

                <div className="flex flex-wrap gap-6 items-center">
                    <div className="flex flex-col w-32">
                        <span className="text-xs text-slate-400 mb-1">Ano: {year}</span>
                        <input
                            type="range"
                            min="2024"
                            max="2026"
                            value={year}
                            onChange={e => setYear(Number(e.target.value))}
                            className="accent-blue-500 cursor-pointer h-1 bg-slate-700 rounded-lg appearance-none"
                        />
                    </div>

                    {/* Intervalo de Meses */}
                    <div className="flex items-center gap-2">
                        <div className="flex flex-col">
                            <span className="text-xs text-slate-400 mb-1">De:</span>
                            <select
                                value={startMonth}
                                onChange={e => setStartMonth(Number(e.target.value))}
                                className="bg-slate-900 border border-slate-700 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-1.5"
                            >
                                {months.map(m => <option key={m.v} value={m.v}>{m.l}</option>)}
                            </select>
                        </div>
                        <span className="text-slate-500 mt-5">-</span>
                        <div className="flex flex-col">
                            <span className="text-xs text-slate-400 mb-1">Até:</span>
                            <select
                                value={endMonth}
                                onChange={e => setEndMonth(Number(e.target.value))}
                                className="bg-slate-900 border border-slate-700 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-1.5"
                            >
                                {months.map(m => <option key={m.v} value={m.v}>{m.l}</option>)}
                            </select>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Grid Layout */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

                {/* LEFT COLUMN - Charts & KPIs */}
                <div className="lg:col-span-2 space-y-6 flex flex-col">
                    {/* KPI ROW */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <KPICard title="Média Score" value={processedData.kpi.avgScore || 0} />
                        <KPICard title="Total Candidatos" value={processedData.kpi.total || 0} />
                        <KPICard title="Aprovação" value={`${processedData.kpi.approvalRate || 0}%`} />
                    </div>

                    {/* CHART: Média Score por Mês */}
                    <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-lg">
                        <h3 className="text-sm font-semibold mb-4 text-slate-200">Tendência de Score</h3>
                        <div className="h-64">
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={processedData.monthly}>
                                    <defs>
                                        <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid vertical={false} stroke="#334155" strokeDasharray="3 3" />
                                    <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                                    <YAxis stroke="#94a3b8" domain={[0, 100]} tick={{ fontSize: 12 }} />
                                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                                    <Area type="monotone" dataKey="score" stroke="#3b82f6" fillOpacity={1} fill="url(#colorScore)" strokeWidth={2} />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>
                    </div>

                    {/* CHART: Total Candidatos por Mês */}
                    <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 shadow-lg">
                        <h3 className="text-sm font-semibold mb-4 text-slate-200">Volume de Candidatos</h3>
                        <div className="h-80">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={processedData.monthly}>
                                    <CartesianGrid vertical={false} stroke="#334155" />
                                    <XAxis dataKey="name" stroke="#94a3b8" tick={{ fontSize: 12 }} />
                                    <YAxis stroke="#94a3b8" allowDecimals={false} tick={{ fontSize: 12 }} />
                                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} cursor={{ fill: 'transparent' }} />
                                    <Bar dataKey="count" fill="#2563eb" radius={[4, 4, 0, 0]} barSize={40} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                </div>

                {/* RIGHT COLUMN - Tables */}
                <div className="space-y-6 flex flex-col">
                    <MiniTable
                        title="Top Cargos"
                        data={processedData.byRole}
                        cols={[{ h: 'Cargo', k: 'role' }, { h: 'Média', k: 'avg' }, { h: 'Qtde', k: 'count' }]}
                    />
                    <MiniTable
                        title="Senioridade"
                        data={processedData.bySeniority}
                        cols={[{ h: 'Nível', k: 'seniority' }, { h: 'Média', k: 'avg' }, { h: 'Qtde', k: 'count' }]}
                    />

                    <div className="bg-slate-800 rounded-xl border border-slate-700 flex flex-col shadow-lg overflow-hidden h-[420px]">
                        <div className="p-4 border-b border-slate-700 bg-slate-800">
                            <h3 className="font-semibold text-slate-200">Ranking Detalhado</h3>
                        </div>
                        <div className="overflow-auto flex-1 p-0 custom-scrollbar relative">
                            <table className="w-full text-xs text-left text-slate-300">
                                <thead className="text-slate-500 uppercase bg-slate-900 sticky top-0 z-10 shadow-sm">
                                    <tr>
                                        <th className="p-3 font-semibold">Nome</th>
                                        <th className="p-3 font-semibold">Cargo</th>
                                        <th className="p-3 text-center font-semibold">Score</th>
                                        <th className="p-3 font-semibold">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-700/50">
                                    {processedData.filtered.map((c, i) => (
                                        <tr key={i} className="hover:bg-slate-700/50 transition-colors">
                                            <td className="p-3 font-medium text-white max-w-[140px] truncate" title={c.nome_candidato}>
                                                {c.nome_candidato}
                                            </td>
                                            <td className="p-3 text-slate-400 text-xs max-w-[120px] truncate" title={c.cargo_alvo}>
                                                {c.cargo_alvo}
                                            </td>
                                            <td className="p-3 font-bold text-center">{c.score_aderencia}</td>
                                            <td className="p-3">{renderClassificacao(c.score_aderencia)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
}

// Sub-componentes
function KPICard({ title, value }) {
    return (
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center shadow-md hover:border-slate-600 transition-colors">
            <span className="text-3xl font-bold text-white mb-1">{value}</span>
            <span className="text-slate-400 text-xs uppercase tracking-wider">{title}</span>
        </div>
    );
}

function MiniTable({ title, data, cols }) {
    return (
        <div className="bg-slate-800 p-4 rounded-xl border border-slate-700 shadow-md">
            <h3 className="text-sm font-semibold mb-3 text-slate-200">{title}</h3>
            <div className="overflow-x-auto custom-scrollbar">
                <table className="w-full text-xs text-left text-slate-300">
                    <thead className="text-slate-500 border-b border-slate-700 bg-slate-800">
                        <tr>
                            {cols.map((col, i) => <th key={i} className="pb-2 font-semibold">{col.h}</th>)}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-700/30">
                        {data.map((row, i) => (
                            <tr key={i}>
                                {cols.map((col, j) => (
                                    <td key={j} className="py-2.5 text-slate-300">
                                        {j === 0 ? <span className="font-medium text-white">{row[col.k]}</span> : row[col.k]}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
