# Dom?nio de Auditoria: Fiscal & Tribut?rio (Tax & Fiscal Audit)

## 1. Vis?o Geral
O dom?nio de **Fiscal & Tribut?rio** foca na auditoria de conformidade das obriga??es acess?rias, c?lculo de tributos federais, estaduais e municipais, e identifica??o de cr?ditos tribut?rios n?o aproveitados (*tax savings*). O sistema analisa cruzamentos complexos entre arquivos digitais do governo (SPED) e os documentos internos do ERP para mitigar riscos de autua??es e otimizar a carga tribut?ria da empresa.

---

## 2. Fontes de Dados e Documentos Ingestados
- **SPED Fiscal (EFD ICMS/IPI):** Arquivo digital de registro das opera??es com incid?ncia de ICMS e IPI.
- **SPED Contribui??es (EFD Contribui??es):** Arquivo digital de escritura??o da contribui??o para o PIS/Pasep e para a COFINS.
- **XMLs de NF-e (Entradas e Sa?das) e NFS-e (Servi?os):** Notas fiscais eletr?nicas de produtos e servi?os.
- **GIA (Guia de Informa??o e Apura??o do ICMS):** Declara??o estadual de apura??o do imposto.
- **Cadastro de Regras Fiscais:** Matriz tribut?ria por NCM (Nomenclatura Comum do Mercosul), CFOP, UF de origem e destino, regime tribut?rio (Lucro Real, Presumido) e tipo de cliente.

---

## 3. Principais Regras de Auditoria & Cruzamentos (Regras Core)

### A. Cruzamento NF-e vs. Escritura??o SPED (Omiss?o de Entrada/Sa?da)
*   **Regra:** Validar se todas as notas fiscais eletr?nicas (emitidas ou recebidas) constam escrituradas nos blocos correspondentes (Bloco C) do SPED Fiscal.
*   **Cruzamento:** `Chaves de Acesso XML da SEFAZ` vs `Registros C100/C190 do SPED Fiscal`.
*   **Anomalia:** Omiss?o de receita (notas de sa?da n?o escrituradas) ou perda de cr?ditos fiscais leg?timos (notas de entrada n?o aproveitadas).

### B. Incompatibilidade de Al?quota e Erro de CFOP/NCM
*   **Regra:** Auditar se a al?quota e o CFOP (C?digo Fiscal de Opera??es e Presta??es) aplicados na entrada e sa?da de mercadorias est?o corretos de acordo com as diretrizes da Receita Federal e a NCM do produto.
*   **Cruzamento:** `NCM do Item` e `UF de Origem/Destino` vs `CFOP escriturado` e `Al?quota ICMS/PIS/COFINS`.
*   **Anomalia:** Recolhimento a maior ou a menor de tributos por classifica??o err?nea do produto ou uso de CFOP inadequado.

### C. Oportunidades de Cr?ditos de PIS/COFINS N?o Aproveitados
*   **Regra:** Identificar insumos adquiridos (energia el?trica, fretes sobre compras/vendas, embalagens, alugu?is de m?quinas) que geram direito a cr?dito de PIS/COFINS no regime n?o-cumulativo e que n?o foram apropriados pelo setor fiscal.
*   **Cruzamento:** `Notas de Entrada escrituradas sem cr?dito no SPED Contribui??es (Bloco M)` vs `NCMs e Contas Cont?beis de Insumos eleg?veis`.
*   **Anomalia:** Oportunidade perdida de redu??o do imposto a pagar (*saving* tribut?rio).

### D. Duplicidade no Pagamento de ICMS Substitui??o Tribut?ria (ICMS-ST)
*   **Regra:** Verificar se houve nova cobran?a de ICMS-ST em etapas subsequentes da cadeia de distribui??o para produtos cujo imposto j? havia sido retido anteriormente pelo fabricante/importador (regime de substitui??o tribut?ria monof?sica ou ST).
*   **Cruzamento:** `Registo de Entradas (C100/C190)` vs `CST (C?digo de Situa??o Tribut?ria)` e `NCM`.
*   **Anomalia:** Pagamento em duplicidade de ICMS por falta de segrega??o de receitas.

### E. Reten??o na Fonte de Impostos de Servi?os Tomados (NFS-e)
*   **Regra:** Garantir que os impostos federais (PIS, COFINS, CSLL, IRRF) e municipais (ISS) incidentes sobre servi?os tomados de terceiros tenham sido retidos e recolhidos em estrita observ?ncia ? legisla??o local e federal.
*   **Cruzamento:** `NFS-e (Campos de Reten??o)` vs `DARF/GPS de Recolhimento de Reten??es`.
*   **Anomalia:** Falha na reten??o gerando responsabilidade solid?ria por d?bitos tribut?rios de terceiros ou recolhimento de ISS no munic?pio incorreto.

---

## 4. Algoritmos de Detec??o e M?todos IA
- **Motor de Regras Tribut?rias Baseado em Grafos:** Modelagem de depend?ncia para recalcular cadeias de impostos interestaduais que dependem de conv?nios/protocolos fiscais complexos entre estados.
- **Classificador NLP de Itens para Saneamento de Cadastro:** Intelig?ncia artificial treinada para ler descri??es de produtos escrituradas e sugerir a correta classifica??o de NCM e benef?cios fiscais associados (ex: PIS/COFINS monof?sico de autope?as ou bebidas).

---

## 5. KPIs e M?tricas de Auditoria Fiscal
- **Total Tax Saving Identificado (R$):** Valor acumulado de cr?ditos n?o aproveitados identificados e prontos para compensa??o.
- **Risco de Auto de Infra??o Mitigado (R$):** Valor estimado sob risco de multas fiscais devido a incoer?ncias cadastrais ou omiss?es corrigidas preventivamente.
- **?ndice de Saneamento de Cadastro:** Percentual de itens de estoque com NCM e parametriza??o fiscal 100% validados pela IA.
- **Efic?cia da Recupera??o Tribut?ria:** Tempo m?dio entre a detec??o do cr?dito e a homologa??o da compensa??o fiscal.
