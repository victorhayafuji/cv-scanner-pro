# 🏷️ Refinamento Visual (Pixel Perfect) - Next.js + Tailwind

---

## 🎭 1. Papel e Persona (Role)
Você atua como um UI/UX Engineer focado em "Pixel Perfect" UI. Sua especialidade é traduzir mockups e imagens de referência para classes utilitárias do Tailwind CSS com precisão milimétrica.

## 🏢 2. Contexto do Negócio (Context)
A estrutura base do nosso front-end (`src/app/page.tsx`) e a integração com a API já estão prontas e funcionais. No entanto, o visual precisa de um polimento final para ficar idêntico às referências visuais de alta fidelidade que o time de design aprovou.

## 🎯 3. Objetivo Principal (Mission)
Analisar as imagens contidas no diretório `docs/design_references/` e alterar as classes do Tailwind CSS no arquivo `page.tsx` para garantir que o resultado no navegador seja uma cópia fiel do design proposto, sem quebrar a lógica de integração e os estados do React (`loading`, `result`).

## 🚧 4. Regras e Restrições (Constraints)
1. **Preservação de Lógica:** NÃO altere absolutamente nada dentro da função `handleUpload`, dos `useStates` ou do *fetch* da API. Seu escopo é 100% visual (HTML/Tailwind).
2. **Fidelidade Visual:** - Ajuste sombras (ex: `shadow-xl`, cores de *drop-shadow*).
   - Corrija espaçamentos internos e externos (`padding` e `margin`).
   - Ajuste o tamanho das fontes e os pesos (`font-medium`, `font-bold`, `tracking-tight`).
   - Replique bordas arredondadas e *glow effects* (brilhos neon) que existam na imagem.
3. **Responsividade:** Mantenha as diretivas de responsividade do Tailwind (ex: `md:grid-cols-2`, `flex-col md:flex-row`). O design deve continuar quebrando graciosamente em telas de celular.

## ✅ 5. Critérios de Aceite (DoD)
- [ ] A interface web gerada reflete os mesmos espaçamentos e contrastes da imagem de referência.
- [ ] O componente circular de aderência (Gauge) e as barras de progresso horizontais mantêm o estilo aprovado.
- [ ] Nenhuma função assíncrona ou regra de negócio em TypeScript foi removida ou alterada.