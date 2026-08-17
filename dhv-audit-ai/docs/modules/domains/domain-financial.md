# Dom?nio de Auditoria: Financeiro & Bancos (Financial & Treasury Audit)

## 1. Vis?o Geral
O dom?nio de **Financeiro & Bancos** foca na auditoria do fluxo de caixa operacional, contas a pagar, contas a receber, tesouraria e rela??es banc?rias (*Treasury*). Seus principais objetivos consistem em identificar desperd?cios de capital de giro (juros e multas por atraso), evitar fraudes financeiras (desvio de pagamentos para contas de terceiros), garantir a fidedignidade da concilia??o banc?ria e otimizar as tarifas de servi?os cobradas pelas institui??es financeiras.

---

## 2. Fontes de Dados e Documentos Ingestados
- **Extratos Banc?rios Eletr?nicos (OFX, CNAB 240):** Registros de todas as movimenta??es e lan?amentos ocorridos nas contas correntes da empresa.
- **DDA (D?bito Direto Autorizado):** Relat?rio de todos os boletos emitidos contra os CNPJs do grupo no sistema banc?rio nacional.
- **Relat?rio de Contas a Pagar (Accounts Payable - AP):** T?tulos agendados, baixados e cancelados no m?dulo financeiro do ERP.
- **Relat?rio de Contas a Receber (Accounts Receivable - AR):** Faturamento, liquida??es, inadimpl?ncia e write-offs.
- **Comprovantes de Transfer?ncias e Pagamentos:** Arquivos de retorno CNAB, logs de pagamento e comprovantes avulsos em PDF.

---

## 3. Principais Regras de Auditoria & Cruzamentos (Regras Core)

### A. Concilia??o Banc?ria Automatizada e Blindagem de Sa?das
*   **Regra:** Validar se todo e qualquer d?bito listado no extrato banc?rio possui um correspondente t?tulo de Contas a Pagar aprovado no ERP e uma Nota Fiscal de suporte v?lida.
*   **Cruzamento:** `Extrato Banc?rio (D?bito)` vs `T?tulos Baixados no ERP` vs `Notas Fiscais de Entrada`.
*   **Anomalia:** Lan?amento de sa?das financeiras ("saques" ou "transfer?ncias") sem t?tulo de suporte no ERP (ind?cio de desvio ou fraude de caixa).

### B. Desvio de Destinat?rio de Pagamento (Fraude do Boleto / Altera??o de Conta)
*   **Regra:** Confrontar o CNPJ benefici?rio do boleto/TED no extrato banc?rio ou arquivo CNAB com o CNPJ do fornecedor homologado no cadastro oficial e no pedido de compra.
*   **Cruzamento:** `Arquivo de Remessa Banc?ria (CNAB)` vs `Cadastro do Fornecedor (Banco e CNPJ)`.
*   **Anomalia:** Pagamento efetuado para conta pessoal de terceiros ou boleto fraudado com altera??o de c?digo de barras (CNPJ benefici?rio diferente do emissor da NF-e).

### C. Pagamento em Duplicidade (Contas a Pagar)
*   **Regra:** Detectar se um mesmo t?tulo ou nota fiscal foi liquidado mais de uma vez, seja por meio de boletos de bancos diferentes, via pix avulso, ou em compet?ncias distintas.
*   **Cruzamento:** `T?tulos Liquidados` filtrados por valor, data de vencimento pr?xima, CNPJ do fornecedor e identificador do documento (n?mero da nota ou fatura).
*   **Anomalia:** Liquida??o dupla do mesmo passivo financeiro.

### D. Perda Financeira por Juros e Multas de Atraso
*   **Regra:** Quantificar o montante pago a t?tulo de juros morat?rios e multas devido a falhas no agendamento e libera??o de pagamentos dentro da data de vencimento.
*   **Cruzamento:** `T?tulos Baixados com Atraso` (Diferen?a de datas entre vencimento e efetiva liquida??o, cruzando com os campos de juros/multa).
*   **Anomalia:** Perda invis?vel de caixa decorrente de inefici?ncias no fluxo de aprova??o de contas a pagar.

### E. Auditoria de Tarifas e Taxas Banc?rias Contratadas
*   **Regra:** Analisar as tarifas banc?rias debitadas no extrato de tarifas das contas correntes e verificar se coincidem com as tabelas negociadas em contrato com as institui??es financeiras.
*   **Cruzamento:** `D?bitos de Tarifa no Extrato OFX` vs `Contrato de Tarifas e Conv?nio de Cobran?a`.
*   **Anomalia:** Cobran?a abusiva de taxas acima do contratado por processamento de boletos, transfer?ncias (TED/Pix) e cust?dia.

---

## 4. Algoritmos de Detec??o e M?todos IA
- **An?lise da Lei de Benford (First-Digit Law):** Auditoria em lan?amentos manuais do contas a pagar para identificar desvios estat?sticos na distribui??o de d?gitos significativos, que costumam revelar fraudes ou manipula??es cont?beis.
- **Clusteriza??o K-Means (Outliers de Pagamento):** Identifica??o de pagamentos fora de padr?es de comportamento habitual do departamento (ex: pagamentos de alto valor efetuados em fins de semana ou feriados).

---

## 5. KPIs e M?tricas de Auditoria Financeira
- **Saving por Recupera??o de Duplicidades:** Valores efetivamente recuperados ou compensados com fornecedores ap?s detec??o de pagamentos duplos.
- **?ndice de Pontualidade de Pagamentos:** Percentual de faturas pagas exatamente no dia do vencimento ou antes (mitigando juros/multas e aproveitando descontos por antecipa??o).
- **Tarifa Banc?ria M?dia por Transa??o:** Custo ponderado de tarifas operacionais cobradas pelas institui??es.
- **Capital de Giro Preservado:** Redu??o de custos e elimina??o de perdas financeiras no contas a pagar.
