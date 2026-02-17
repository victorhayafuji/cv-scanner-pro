# 🏷️ Cálculo de Score Determinístico (Python-Side)
**Versão:** 1.0.0 | **Status:** Validated

## 🎯 Missão
Desacoplar o cálculo aritmético do LLM. A IA deve apenas auditar e pontuar categorias individuais, enquanto o Python realiza a soma final do `match_percentual`.

## 🚧 Regras de Pontuação (Rubrica Fixa)
1. **Técnico (0-50 pts):** Hard skills e ferramentas.
2. **Senioridade (0-30 pts):** Fit de cargo e tempo de XP.
3. **Diferenciais (0-20 pts):** Formação e extras.

## ✅ Critérios de Aceite
- [ ] Modelos Pydantic atualizados com campos de score parciais.
- [ ] Prompt da IA focado em atribuição de notas por categoria.
- [ ] Soma realizada via Python antes da persistência no BI.