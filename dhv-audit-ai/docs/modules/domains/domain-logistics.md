# Dom?nio de Auditoria: Log?stica & Fretes (Logistics & Freight Audit)

## 1. Vis?o Geral
O dom?nio de **Log?stica & Fretes** foca na auditoria inteligente de toda a cadeia de transporte, visando ? redu??o direta de custos (*saving*), conformidade contratual com transportadoras e otimiza??o operacional da distribui??o. O m?dulo analisa criticamente os documentos de transporte e as notas fiscais de mercadorias para identificar distor??es tarif?rias, erros de cobran?a e descumprimento de SLAs.

---

## 2. Fontes de Dados e Documentos Ingestados
- **CT-e (Conhecimento de Transporte Eletr?nico):** Arquivos XML e PDFs de transporte rodovi?rio, a?reo e multimodal.
- **NF-e (Nota Fiscal Eletr?nica):** XML das notas fiscais das mercadorias transportadas (para extrair pesos, volumes, valores das mercadorias e destinat?rios).
- **MDF-e (Manifesto Eletr?nico de Documentos Fiscais):** XML de consolida??o de carga.
- **Tabelas de Frete Contratadas:** Planilhas ou cadastros de tabelas com taxas negociadas por regi?o, faixa de peso, tipo de ve?culo, pra?a e ped?gios.
- **Ocorr?ncias e Registros de Entrega (SLAs):** Arquivos de retorno das transportadoras (CONED, OCO) contendo datas e status das entregas.

---

## 3. Principais Regras de Auditoria & Cruzamentos (Regras Core)

### A. Auditoria de Tarifas (Tabela de Fretes)
*   **Regra:** Verificar se a tarifa cobrada no CT-e condiz exatamente com a tabela contratada com a transportadora para aquela rota (origem/destino) e faixa de peso/volume.
*   **Cruzamento:** `CT-e (Valor do Frete Peso + Frete Valor)` vs `Tabela de Fretes Cadastrada`.
*   **Anomalia:** Cobran?a acima do negociado (sobrepre?o).

### B. Diverg?ncia de Cubagem (Peso Cubado vs Peso Real)
*   **Regra:** Auditar se o c?lculo do peso cubado cobrado pela transportadora segue as regras da ANTT e do contrato (ex: fator de cubagem de 300 kg/m©ø para rodovi?rio fracionado).
*   **Cruzamento:** `NF-e (Dimens?es/Volume)` vs `CT-e (Peso Cubado Faturado)`.
*   **Anomalia:** Cubagem superdimensionada pela transportadora para cobrar tarifas maiores.

### C. Duplicidade de Cobran?a (CT-es Duplicados)
*   **Regra:** Garantir que um mesmo frete ou entrega de mercadoria n?o seja faturado duas vezes pela transportadora (ou por transportadoras distintas).
*   **Cruzamento:** `Chave de Acesso da NF-e` e `Chave de Acesso do CT-e` em m?ltiplos lotes de faturamento.
*   **Anomalia:** Cobran?a duplicada da mesma entrega.

### D. Cobran?a de Taxas Acess?rias N?o Negociadas
*   **Regra:** Verificar se taxas adicionais como Ad Valorem, GRIS (taxa de gerenciamento de risco), TRT (taxa de restri??o de tr?nsito), TDE (taxa de dif?cil acesso) e ped?gios fracionados est?o de acordo com o contrato ou se s?o abusivas.
*   **Cruzamento:** Itens de despesa do `CT-e` vs `Regras Contratuais`.
*   **Anomalia:** Inclus?o de taxas n?o aprovadas ou c?lculo incorreto do Ad Valorem sobre o valor real da nota.

### E. Descumprimento de Prazos (OTIF - On-Time In-Full)
*   **Regra:** Comparar as datas de entrega real registradas nos comprovantes digitais (canhotos) com o prazo limite prometido em contrato.
*   **Cruzamento:** `MDF-e/CT-e (Data de Emiss?o + SLA de rota)` vs `Canhoto/Ocorr?ncia (Data de Entrega)`.
*   **Anomalia:** Atraso sistem?tico que d? direito a estorno ou multas contratuais.

---

## 4. Algoritmos de Detec??o e M?todos IA
- **Machine Learning (An?lise de Outliers):** Detec??o de picos de custo por km rodado por rota espec?fica ou transportadora.
- **RAG (Retrieval-Augmented Generation) com NLP:** Extra??o autom?tica de regras contratuais complexas em PDFs de propostas comerciais de transporte para alimentar o motor de regras.
- **Deduplica??o Fuzzy:** Identifica??o de entregas re-faturadas onde h? pequenas varia??es no n?mero do documento ou datas, mas os volumes e valores coincidem.

---

## 5. KPIs e M?tricas de Redu??o de Custos (Savings)
- **Saving Identificado por Frete:** Total de diverg?ncias financeiras encontradas que podem ser glosadas ou contestadas.
- **Custo M?dio por Tonelada-Km (TKM):** Efici?ncia financeira por rota e modal.
- **?ndice de Acertos de Faturamento:** Percentual de CT-es cobrados de forma 100% correta pelas transportadoras parceiras.
- **SLA Fulfillment Rate (OTIF):** Percentual de entregas realizadas dentro do prazo contratado.
