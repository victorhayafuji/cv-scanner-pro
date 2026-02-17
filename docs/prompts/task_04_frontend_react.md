🎨 Design System & UI Specification (Dark Tech)
1. Paleta de Cores (Tailwind CSS)
O visual é "Dark Mode Nativo", transmitindo alta tecnologia e foco.
• Background Principal (Canvas): bg-slate-950 (Um preto azulado profundo, não preto absoluto #000).
• Superfícies (Cards): bg-slate-900 com bordas sutis border border-slate-800.
• Ação Primária (CTA): bg-lime-400 (O verde neon da Imagem e).
    ◦ Estado Hover: hover:bg-lime-300.
    ◦ Texto do Botão: text-slate-950 font-bold (Contraste máximo).
• Ação Secundária / Destaques: text-blue-600 ou bg-blue-600 (O azul elétrico das barras de progresso na Imagem).
• Semântica de Feedback (API):
    ◦ Score Alto / Pontos Fortes: text-emerald-400 (Variação do Lime para texto).
    ◦ Gaps / Alertas: text-rose-500 (Vermelho suave para manter legibilidade no escuro).
• Tipografia:
    ◦ H1/H2: text-slate-50 (Branco gelo).
    ◦ Parágrafos: text-slate-400 (Cinza médio para reduzir fadiga visual).
2. Tipografia e Formas
Baseado na suavidade dos elementos das imagens e.
• Arredondamento (Border Radius):
    ◦ Cards Grandes: rounded-2xl ou rounded-3xl (Bem arredondado, estilo "App Mobile").
    ◦ Botões: rounded-full (Pill shape, conforme botão "Generate workout plan" na Imagem).
    ◦ Inputs/Tags: rounded-lg.
• Sombras e Profundidade:
    ◦ Cards: shadow-xl com uma leve cor colorida difusa: shadow-slate-900/50.
    ◦ Glow Effect (Opcional): Elementos de destaque podem ter um ring-2 ring-lime-400/20.
• Fonte: Inter ou Outfit (Google Fonts). Sans-serif geométrica.

--------------------------------------------------------------------------------
3. Mapeamento de Componentes vs. API
Aqui conectamos o JSON retornado pela rota POST /api/v1/analisar-cv/ aos elementos visuais das imagens.
A. Área de Upload (Hero Section)
• Referência Visual: Imagem (Card "Ready for Your Transformation?").
• Comportamento:
    ◦ Substituir o texto "Ready for Your Transformation?" por "Pronto para sua nova vaga?".
    ◦ Substituir a imagem do halterofilista por uma ilustração 3D abstrata de documentos ou foguete.
    ◦ Botão Lime Green: "Analisar meu CV Agora". Ao clicar, abre o explorador de arquivos (Input file hidden).
    ◦ Input de Vaga: Um textarea com fundo escuro (bg-slate-950) integrado ao card antes do botão.
B. O Score Geral (match_percentual)
• Referência Visual: Imagem (Os círculos com números "01", "02", "03").
• Implementação:
    ◦ Transformar o círculo pequeno em um Radial Progress Grande.
    ◦ Cor do anel: stroke-lime-400.
    ◦ Centro: O valor numérico grande (ex: "85%").
    ◦ Legenda: "Aderência à Vaga".
C. Métricas Detalhadas (Barras de Progresso)
• Referência Visual: Imagem (Cards "Body Building", "Calorie Burning").
• Dados da API: score_tecnico (0-50), score_senioridade (0-30), score_diferencial (0-20).
• Implementação:
    ◦ Usar o estilo exato das barras azuis da Imagem.
    ◦ Label "Strength" -> Vira "Hard Skills" (score_tecnico).
    ◦ Label "Cardio" -> Vira "Senioridade" (score_senioridade).
    ◦ Barra preenchida com bg-blue-600 sobre trilho bg-slate-800.
D. Gaps e Pontos Fortes (Cards Bento Grid)
• Referência Visual: Imagem (O grid irregular "More than just a workout").
• Dados da API: pontos_fortes (Lista) e gaps_tecnicos (Lista).
• Implementação:
    ◦ Card Esquerdo (Grande): "Análise Comparativa" (Texto corrido da analise_comparativa).
    ◦ Card Direito Superior (Azul/Escuro): "Pontos Fortes". Listar os itens com ícones de Check Verde (text-lime-400).
    ◦ Card Direito Inferior (Lime/Vibrante): "Gaps Identificados".
        ▪ Inversão de cor: Fundo bg-lime-400, Texto text-slate-900.
        ▪ Listar os gaps como itens de atenção.

--------------------------------------------------------------------------------
4. Estrutura do Layout (Wireframe Textual)
[ Container Principal (max-w-6xl mx-auto px-4 py-8 bg-slate-950) ]
|
+-- [ Header: Logo "CV Engine" (Branco) + Menu ]
|
+-- [ Hero Section (Referência Imagem 4) ]
|   |-- Título: "Aumente suas chances de entrevista"
|   |-- Form: [ Upload PDF ] + [ Textarea Vaga ]
|   |-- Botão CTA (Lime): "Gerar Análise"
|
+-- [ Loading State ] (Skeleton dark mode pulsante)
|
+-- [ Results Grid (Aparece após API 200 OK) ]
    |
    +-- [ Linha 1: KPIs Principais ]
    |   |-- Coluna Esq: Gauge Chart (Match %)
    |   |-- Coluna Dir: 3 Barras de Progresso (Skills, Senioridade, Diferencial)
    |       (Referência Imagem 2)
    |
    +-- [ Linha 2: Insights Detalhados (Referência Imagem 3 - Bento Grid) ]
    |   |-- Card Grande (2 colunas): Parecer da IA (Texto)
    |   |-- Coluna Lateral:
    |       |-- Card Topo: Lista Pontos Fortes (Ícones Verdes)
    |       |-- Card Base: Lista Gaps (Estilo Alerta)
    |
    +-- [ Linha 3: Call to Action Final ]
        |-- Botão Outline: "Baixar Relatório PDF"
        |-- Botão Primary: "Reescrever CV com IA" (Chama endpoint /otimizar)
Observação para o Dev React: Lembre-se de configurar o tailwind.config.js para estender as cores:
theme: {
  extend: {
    colors: {
      brand: {
        dark: '#0f172a', // Slate-900 base
        neon: '#a3e635', // Lime-400
        accent: '#2563eb', // Blue-600
      }
    }
  }
}