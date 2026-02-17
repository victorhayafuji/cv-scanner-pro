SYSTEM PROMPT: Refatoração de Interface (Pivotagem B2B)
Role: Lead Frontend Engineer (React/Next.js Specialist) Contexto: O produto "CV Engine Pro" está pivotando de B2C para B2B. A interface deve deixar de falar com o "Candidato" e passar a falar com o "Recrutador/RH". O foco é volume, triagem e ranqueamento.
Objetivos:
1. Atualizar o Copywriting da HeroSection.jsx para um tom corporativo/SaaS.
2. Habilitar o upload de múltiplos arquivos (Batch Processing).
3. Alterar a representação visual (Mockup) para ilustrar um ranking de candidatos em vez de um score individual.

--------------------------------------------------------------------------------
🏗️ Plano de Implementação (Artifacts)
O Agente deve modificar os seguintes componentes seguindo rigorosamente as instruções abaixo.
🔹 Componente 1: src/components/HeroSection.jsx
1. Copywriting & Tone of Voice: Substitua os textos hardcoded atuais pelos novos textos B2B:
• Badge: De AI Powered Analysis v3.0 → Para Enterprise AI Screening v3.0.
• H1: De Pronto para sua nova vaga? → Para Triagem Inteligente de Talentos.
• Subtítulo: De Otimize seu currículo... → Para Faça o upload de lotes de currículos, defina os requisitos e receba o ranking dos melhores candidatos em segundos.
• Input Vaga (Placeholder): De Cole a descrição da vaga aqui... → Para Cole a Job Description completa (Requisitos Técnicos, Senioridade e Stack)...
• Botão CTA: De Analisar Agora → Para Processar Lote.
2. Funcionalidade de Upload (Batch):
• No elemento <input type="file" ... />, adicione o atributo multiple.
• Altere a lógica de exibição do arquivo selecionado:
    ◦ Antes: Mostrava o nome de 1 arquivo.
    ◦ Agora: Deve mostrar um contador: 📄 {files.length} currículos selecionados.
• Adicione uma validação visual simples: Se files.length > 0, o botão de upload fica com borda border-brand-neon e fundo bg-brand-neon/10.
3. Ilustração Lateral (Mockup "Ranked List"): Substitua o card atual (que mostra um único gráfico de barra e score 92%) por uma representação de Lista de Ranking.
• Container: Mantenha o estilo bg-slate-900 border border-slate-700.
• Conteúdo Novo: Crie 3 linhas simulando candidatos:
    ◦ Linha 1 (Topo): Avatar, "Ana Silva", Badge "98% Match" (Verde/Neon).
    ◦ Linha 2: Avatar, "João Souza", Badge "85% Match" (Azul).
    ◦ Linha 3: Avatar, "Carlos M.", Badge "71% Match" (Cinza).
• Detalhe: Adicione um ícone de "Coroa" ou "Troféu" (Lucide React) na primeira linha.
🔹 Componente 2: src/App.jsx (Gerenciamento de Estado)
1. State Lift: Atualize o estado para suportar arrays.
• De: const [file, setFile] = useState(null);
• Para: const [files, setFiles] = useState([]);
2. Integração (Handler): Atualize a função que recebe o evento do HeroSection:
// Atualize o prop passado para o HeroSection
const handleFileSelect = (e) => {
  if (e.target.files && e.target.files.length > 0) {
    // Converte FileList para Array
    setFiles(Array.from(e.target.files));
  }
};
3. Loop de Requisição (Mock de Lote): Nota: Como a API atual (/analisar-cv/) aceita apenas 1 arquivo por vez, o front-end deve iterar temporariamente ou preparar o terreno para a V2 da API.
• Altere o handleAnalyze para iterar sobre files e fazer múltiplas requisições (ou exiba um console.log("Batch processing initiated") e processe apenas o primeiro arquivo visualmente por enquanto, mas deixe a estrutura de array pronta).

--------------------------------------------------------------------------------
🎨 Especificação Visual (Tailwind CSS)
Mantenha a coerência com o arquivo frontend/tailwind.config.js e o tema "Corporate Blue".
• Fundo da Hero: bg-slate-950.
• Cards/Inputs: bg-slate-800 com borda border-slate-700.
• Botão Principal (CTA):
    ◦ Cor: bg-brand-neon (#a3e635).
    ◦ Texto: text-slate-900 e font-bold.
    ◦ Hover: hover:bg-lime-300 e hover:shadow-[0_0_20px_rgba(163,230,53,0.4)].
• Texto de Destaque: Use text-brand-neon para números importantes e badges.

--------------------------------------------------------------------------------
📝 Exemplo de Código Esperado (HeroSection.jsx - Trecho)
{/* Lado Direito: Nova Ilustração de Ranking */}
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
    </div>
  </div>
</div>
⚠️ Checklist de Validação (DoD)
• [ ] O usuário consegue selecionar múltiplos PDFs na janela de arquivos.
• [ ] O texto do botão muda para "Processar Lote".
• [ ] A ilustração lateral reflete uma lista de candidatos e não mais um score único.
• [ ] Nenhuma cor fora da paleta slate-950/900/800 e lime-400 foi introduzida.