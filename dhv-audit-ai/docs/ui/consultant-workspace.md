# Workspace do Consultor (Consultant Workspace)

O **Workspace do Consultor** ? a central de opera??o mais importante da plataforma. ? neste ambiente que os consultores seniores da DHV Log gerenciam os fluxos de auditoria, interagem com a intelig?ncia artificial, validam desvios e geram relat?rios consolidados no modelo *Human-in-the-Loop*.

---

## 1. Tela: Fila de Valida??o de Achados (Findings Queue)

Esta tela exibe todos os desvios, anomalias e economias pr?-identificadas pela Intelig?ncia Artificial que precisam de homologa??o humana antes de serem publicados para o cliente.

### Layout e Estrutura Visual
- **Cabe?alho da P?gina:**
  - T?tulo: `Fila de Revis?o de Achados`
  - Resumo estat?stico: `Total Pendentes: 42` | `Impacto Estimado: R$ 84.320,00` | `M?dia de Confian?a IA: 88.5%`.
- **Filtros R?pidos:**
  - Filtro por Gravidade (`Critical`, `High`, `Medium`, `Low`).
  - Filtro por Dom?nio de Auditoria (`Logistics`, `HR`, `Fiscal`, `Procurement`, `Financial`, `Fleet`).
  - Toggle de Confian?a (`Exibir apenas < 90%`).
- **Lista de Trabalho (Tabela Densa):**
  - **Coluna 1 (ID/T?tulo):** ID e resumo amig?vel do achado.
  - **Coluna 2 (Dom?nio):** Badge colorido representando a vertical do achado.
  - **Coluna 3 (Impacto):** Valor financeiro estimado em negrito (R$).
  - **Coluna 4 (Confian?a):** Badge din?mico de confian?a da IA (`94%` verde, `76%` amarelo, `52%` vermelho).
  - **Coluna 5 (Status):** `Aguardando Revis?o` (amarelo) ou `Em Revis?o` (azul).
  - **Coluna 6 (A??o):** Bot?o `Analisar` que abre a tela de revis?o detalhada.

---

## 2. Tela de Detalhe e Revis?o Lado a Lado (Side-by-Side Review Page)

Quando o consultor clica em `Analisar`, a plataforma abre uma interface ultra-especializada de revis?o em duas colunas.

```
忙式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式成式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式忖
弛     COLUNA ESQUERDA: EVID?NCIA F?SICA 弛       COLUNA DIREITA: AN?LISE DA IA    弛
弛                                       弛                                       弛
弛  [ Visualizador de PDF do Documento ] 弛  Achado: Frete Acima do Contrato      弛
弛  - CT-e n足 10293 emitido              弛  Severidade: Alta                     弛
弛  - Peso Cobrado: 450kg                弛  Impacto Calculado: R$ 250,00         弛
弛  - Origem: SP ? Destino: RJ           弛                                       弛
弛                                       弛  [Campos Extra?dos p/ Confronto]      弛
弛  [ Visualizador da Regra/Tabela ]     弛  - Valor Tabela: R$ 950,00            弛
弛  - Tabela Vigente no Sistema:         弛  - Valor Cobrado: R$ 1.200,00         弛
弛    "Frete SP-RJ at? 500kg = R$ 950"   弛                                       弛
弛                                       弛  [A??es do Consultor]                 弛
弛                                       弛  ( ) Aprovar com Impacto Proposto     弛
弛                                       弛  ( ) Ajustar Impacto: [ R$ 250,00 ]   弛
弛                                       弛  ( ) Rejeitar Achado (Desconsiderar)  弛
弛                                       弛                                       弛
弛                                       弛  Coment?rio de Ajuste:                弛
弛                                       弛  [ Confirmado cobran?a incorreta ]    弛
弛                                       弛                                       弛
弛                                       弛  [Salvar e Avan?ar para o Pr?ximo]    弛
戌式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式扛式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式戎
```

### Componentes de Intera??o na Coluna Direita
- **Formul?rio de Valida??o:**
  - Seletor de Decis?o: Tr?s bot?es grandes e claros: `Confirmar Achado`, `Editar Valores` e `Descartar / Falso Positivo`.
  - Input de Impacto Financeiro Ajustado: Permite ao consultor alterar o valor financeiro real caso a IA tenha cometido um pequeno erro de c?lculo no volume ou imposto.
  - Campo de Justificativa de Qualidade: Campo de texto obrigat?rio para justificar decis?es de altera??o ou descarte de achados.
- **Feedback Loop da IA:**
  - Bot?o `Treinar IA com essa Corre??o`: Ao salvar, envia um sinal ao m?dulo de Machine Learning (M23) retroalimentando as pr?ximas infer?ncias do modelo com a corre??o humana efetuada.

---

## 3. Tela: Revis?o de Qualidade do Relat?rio (EQCR - Engagement Quality Control Review)

Antes de qualquer lote de relat?rios ou achados ser entregue formalmente ao painel do cliente, o sistema imp?e o princ?pio de **Revis?o 4 Olhos** (*Engagement Quality Control Review*).

### Fluxo de Gera??o de Relat?rios e Exporta??o
1. **Consolida??o:** O consultor clica em `Gerar Vers?o Preliminar do Relat?rio`.
2. **Motor de Templates (M8):** O sistema consolida todos os achados confirmados, monta gr?ficos executivos em PDF/PPTX e anexa as evid?ncias (canhotos, XMLs confrontados).
3. **Fila de EQCR:** O relat?rio gerado entra automaticamente na fila de um **Consultor Revisor S?nior** ou **S?cio da DHV Log**.
4. **Painel de Aprova??o de Relat?rio:**
  - O revisor analisa o sum?rio executivo, a integridade jur?dica das cl?usulas de NDAs anexas e os totais financeiros.
  - Bot?o `Aprovar para Publica??o no Portal do Cliente`.
  - Bot?o `Retornar para Ajuste` com chat integrado de notas internas para o consultor operacional.
