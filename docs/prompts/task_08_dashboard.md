🎯 SYSTEM PROMPT: Dashboard Analítico (Réplica Visual "Dark Tech")
Role: Senior Frontend Engineer (React/Recharts Specialist) Referência Visual: "Captura de tela 2026-02-17 134112.png" (Layout de Painel Executivo). Objetivo: Construir a página /analytics consumindo a API do CV Engine Pro. O layout deve ser Pixel Perfect em relação à referência: Fundo escuro profundo, cards destacados, gráficos azuis e tabelas densas.

--------------------------------------------------------------------------------
1. Estrutura Visual & Layout (Grid System)
O layout não é um simples grid uniforme. Ele é dividido em zonas funcionais. Utilize CSS Grid para replicar a estrutura da imagem:
• Global Container: bg-[#0B1120] (Slate-950 profundo, quase preto).
• Padding: p-6 ou p-8.
• Header: Barra superior contendo o Título e os Filtros de Data (Ano/Mês).
Disposição dos Blocos (Grid Template):
/* Sugestão de Grid para Telas Grandes (lg/xl) */
grid-template-columns: 2fr 1fr; /* Coluna da Esquerda (Larga) e Direita (Estreita) */
gap: 1.5rem;
📍 Zona A: KPIs (Topo Esquerdo)
• Referência: 3 Cards Retangulares.
• Estilo: bg-slate-800 com borda sutil border-slate-700/50.
• Conteúdo:
    1. Média Score Aderência: (Ex: 53,3). Texto grande centralizado.
    2. Qtde. Candidatos: (Ex: 178).
    3. Taxa de Aprovação: (Ex: 22,5% - Calcular % de candidatos com score >= 70).
📍 Zona B: Gráficos Temporais (Coluna Esquerda - Abaixo dos KPIs)
• Referência: Dois gráficos largos empilhados verticalmente.
• Estilo dos Gráficos:
    ◦ Fundo dos containers: Transparente ou bg-slate-800 (conforme imagem).
    ◦ Gráfico 1 (Linha): "Média Score por Mês".
        ▪ Linha: Azul (#3b82f6).
        ▪ Área: Preenchimento gradiente abaixo da linha (azul transparente).
        ▪ Pontos: Círculos brancos ou azuis preenchidos.
    ◦ Gráfico 2 (Barras): "Total Candidatos por Mês".
        ▪ Barras: Azul sólido (#1d4ed8 ou #2563eb).
        ▪ Labels: Números brancos flutuando acima das barras (Ex: "16", "21").
📍 Zona C: Tabelas de Quebra (Coluna Direita - Full Height)
• Referência: Uma pilha vertical de 3 tabelas compactas.
• Estilo das Tabelas:
    ◦ Header: bg-slate-900 ou transparente com borda inferior azul (border-b-2 border-blue-600).
    ◦ Linhas: Zebra striping muito sutil (odd:bg-slate-800 even:bg-slate-800/50).
    ◦ Tabela 1: "Cargo Alvo" (Colunas: Cargo, Média Score, Total).
    ◦ Tabela 2: "Nível Senioridade" (Colunas: Nível, Média Score, Total).
    ◦ Tabela 3 (Lista): "Nome Candidato" (A lista detalhada com Scroll).
        ▪ Destaque: Coluna "Classificação" deve ter a estrela dourada ⭐ e texto amarelo para "Elite".

--------------------------------------------------------------------------------
2. Lógica de Dados (Front-end Processing)
A API atual (/api/v1/dashboard/metrics) retorna recent_activity (limitado a 10) e KPIs simples. Para replicar os gráficos da imagem (que mostram o ano todo), você precisará alterar a estratégia:
Ação Necessária (Backend): O Backend Agent deve alterar o endpoint GET /dashboard/metrics para retornar todos os registros (ou uma agregação completa) em vez de apenas os 10 últimos.
• Novo Payload JSON Esperado: {"all_records": [...lista completa...]}.
Processamento (React): Use useMemo para calcular as agregações no cliente (Client-Side Aggregation) para garantir interatividade rápida com os filtros:
1. Agrupamento por Mês:
    ◦ Itere sobre all_records.
    ◦ Extraia o mês de data_analise.
    ◦ Calcule count e avg(score_aderencia).
2. Agrupamento por Cargo/Senioridade:
    ◦ reduce da lista filtrada pelas chaves cargo_alvo e nivel_senioridade.
3. Filtros:
    ◦ Implemente os sliders de "Ano" e "Mês" (Range Slider) vistos no topo direito da imagem. O estado desses filtros deve recalcular todos os gráficos.

--------------------------------------------------------------------------------
3. Especificação de Componentes (Recharts & Tailwind)
🎨 Paleta de Cores (Corporate Blue)
• Fundo: bg-[#0f1419] ou bg-slate-950.
• Card Background: bg-[#1e293b] (Slate-800).
• Texto Principal: text-white (ou slate-50).
• Texto Secundário: text-slate-400.
• Cor do Gráfico (Primary): #3b82f6 (Blue-500).
• Destaque Elite: #fbbf24 (Amber-400) ou #eab308 (Yellow-500).
📊 Configuração Recharts
• XAxis/YAxis: tick={{ fill: '#94a3b8', fontSize: 12 }}. Remova as linhas de grade verticais (vertical={false}).
• Tooltip: Customizado com fundo escuro (contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}).
🏆 Tabela de Classificação (Regra Visual)
Baseado na coluna "Classificação" da imagem:
const renderClassificacao = (score) => {
  if (score >= 90) return <span className="text-yellow-400 font-bold flex items-center gap-1">⭐ Elite</span>;
  if (score >= 70) return <span className="text-blue-400 font-medium">✅ Qualificado</span>;
  return <span className="text-slate-500">Em Desenvolvimento</span>;
};

--------------------------------------------------------------------------------
4. Código do Componente (AnalyticsDashboard.jsx)
Aqui está o esqueleto para implementar exatamente a visão da captura de tela:
import React, { useMemo, useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { Filter } from 'lucide-react';
import axios from 'axios';

export default function AnalyticsDashboard() {
  const [rawData, setRawData] = useState([]);
  const [year, setYear] = useState(2025);
  const [monthRange, setMonthRange] = useState([2, 3]);

  // 1. Fetch Full Data
  useEffect(() => {
    // Backend deve ser ajustado para retornar 'all_records'
    axios.get('/api/v1/dashboard/metrics').then(res => setRawData(res.data.all_records || []));
  }, []);

  // 2. Client-Side Processing
  const processedData = useMemo(() => {
    if (!rawData.length) return { monthly: [], byRole: [], bySeniority: [], kpi: {} };

    // Filtra por data (Range Slider logic mock)
    const filtered = rawData.filter(d => {
       const date = new Date(d.data_analise);
       return date.getFullYear() === year && (date.getMonth() + 1 >= monthRange && date.getMonth() + 1 <= monthRange[2]);
    });

    // KPI Calc
    const total = filtered.length;
    const avgScore = total ? (filtered.reduce((acc, cur) => acc + cur.score_aderencia, 0) / total).toFixed(1) : 0;
    const approved = filtered.filter(d => d.score_aderencia >= 70).length;
    const approvalRate = total ? ((approved / total) * 100).toFixed(1) : 0;

    // Monthly Grouping (Para os Gráficos)
    // ... Implementar reduce por mês (1-12) ...
    
    return { kpi: { total, avgScore, approvalRate }, filtered };
  }, [rawData, year, monthRange]);

  return (
    <div className="min-h-screen bg-[#0B1120] text-white p-6 font-sans">
      {/* Header & Filters */}
      <div className="flex justify-between items-center mb-8 bg-slate-800/50 p-4 rounded-xl border border-slate-700">
        <h1 className="text-2xl font-semibold">AI Resume Reader | <span className="text-slate-400">Todos os Cargos</span></h1>
        
        <div className="flex gap-6 items-center">
             {/* Mock dos Sliders da imagem */}
             <div className="flex flex-col w-32">
                <span className="text-xs text-slate-400 mb-1">Ano: {year}</span>
                <input type="range" min="2024" max="2026" value={year} onChange={e => setYear(Number(e.target.value))} className="accent-blue-500"/>
             </div>
             <div className="flex flex-col w-32">
                <span className="text-xs text-slate-400 mb-1">Mês: {monthRange} - {monthRange[2]}</span>
                {/* Dual range slider placeholder */}
                <div className="h-1 bg-blue-600 rounded"></div>
             </div>
        </div>
      </div>

      {/* Main Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* LEFT COLUMN (2/3 width) */}
        <div className="lg:col-span-2 space-y-6">
            
            {/* KPI ROW */}
            <div className="grid grid-cols-3 gap-4">
                <KPICard title="Média Score Aderência" value={processedData.kpi.avgScore} />
                <KPICard title="Qtde. Candidatos" value={processedData.kpi.total} />
                <KPICard title="Taxa de Aprovação" value={`${processedData.kpi.approvalRate}%`} />
            </div>

            {/* CHART: Média Score por Mês */}
            <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
                <h3 className="text-sm font-semibold mb-4 text-slate-200">Média Score por Mês</h3>
                <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={processedData.monthly}> {/* Use AreaChart para o preenchimento */}
                            <defs>
                                <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid vertical={false} stroke="#334155" strokeDasharray="3 3" />
                            <XAxis dataKey="name" stroke="#94a3b8" />
                            <YAxis stroke="#94a3b8" />
                            <Tooltip contentStyle={{backgroundColor: '#1e293b', borderColor: '#334155'}} />
                            <Area type="monotone" dataKey="score" stroke="#3b82f6" fillOpacity={1} fill="url(#colorScore)" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>

            {/* CHART: Total Candidatos por Mês */}
            <div className="bg-slate-800 p-5 rounded-xl border border-slate-700">
                <h3 className="text-sm font-semibold mb-4 text-slate-200">Total Candidatos por Mês</h3>
                <div className="h-64">
                     <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={processedData.monthly}>
                            <CartesianGrid vertical={false} stroke="#334155" />
                            <XAxis dataKey="name" stroke="#94a3b8" />
                            <YAxis stroke="#94a3b8" />
                            <Bar dataKey="count" fill="#2563eb" radius={[4]} label={{ position: 'top', fill: 'white', fontSize: 12 }} />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>

        {/* RIGHT COLUMN (1/3 width) - Tables */}
        <div className="space-y-6">
            <MiniTable title="Cargo Alvo" data={processedData.byRole} cols={['Cargo', 'Média', 'Total']} />
            <MiniTable title="Nível Senioridade" data={processedData.bySeniority} cols={['Nível', 'Média', 'Total']} />
            
            {/* Detailed List */}
            <div className="bg-slate-800 rounded-xl border border-slate-700 h-[600px] flex flex-col">
                <div className="p-4 border-b border-slate-700">
                    <h3 className="font-semibold text-slate-200">Classificação Detalhada</h3>
                </div>
                <div className="overflow-auto flex-1 p-2">
                    <table className="w-full text-xs text-left text-slate-300">
                        <thead className="text-slate-500 uppercase bg-slate-900/50 sticky top-0">
                            <tr>
                                <th className="p-2">Nome</th>
                                <th className="p-2">Score</th>
                                <th className="p-2">Classificação</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-700">
                            {processedData.filtered.map((c, i) => (
                                <tr key={i} className="hover:bg-slate-700/50">
                                    <td className="p-2 font-medium text-white">{c.nome_candidato}</td>
                                    <td className="p-2 font-bold">{c.score_aderencia}</td>
                                    <td className="p-2">{renderClassificacao(c.score_aderencia)}</td>
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

// Sub-componentes simples para manter o código limpo
function KPICard({ title, value }) {
    return (
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex flex-col items-center justify-center text-center">
            <span className="text-4xl font-bold text-white mb-2">{value}</span>
            <span className="text-slate-400 text-sm font-medium">{title}</span>
        </div>
    );
}

function MiniTable({ title, data, cols }) {
    // Implementação simplificada da tabela pequena
    return <div className="bg-slate-800 p-4 rounded-xl border border-slate-700">
        <h3 className="text-sm font-semibold mb-3 text-slate-200">{title}</h3>
        {/* ... table structure ... */}
    </div>
}