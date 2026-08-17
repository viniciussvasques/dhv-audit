# Dom?nio de Auditoria: Compras & Procurement (Procurement & Sourcing Audit)

## 1. Vis?o Geral
O dom?nio de **Compras & Procurement** foca na auditoria do ciclo de aquisi??es de mercadorias, insumos e servi?os (*Procure-to-Pay*). A finalidade ? assegurar o cumprimento de pol?ticas de compras (compliance), verificar a integridade dos processos de cota??o (*sourcing*), detectar fraudes (carteliza??o, favorecimento, conluio) e identificar diverg?ncias comerciais que gerem perdas financeiras (pre?os faturados maiores do que os acordados em contrato ou pedido de compra).

---

## 2. Fontes de Dados e Documentos Ingestados
- **Pedidos de Compra (Purchase Orders - PO):** Registros estruturados gerados pelo ERP contendo itens, quantidades, pre?os unit?rios e condi??es de pagamento aprovados.
- **Notas Fiscais de Entrada (NF-e / NFS-e):** Documentos XML fiscais das mercadorias ou servi?os entregues pelos fornecedores.
- **Processos de Cota??o (Bids):** Registros de propostas, e-mails de cota??o e planilhas comparativas de fornecedores.
- **Contratos de Fornecedores e Tabelas de Pre?o:** Contratos de fornecimento de longo prazo com tabelas de descontos escalonados por volume.
- **Cadastro de Fornecedores (Vendor Master Data):** Dados cadastrais, s?cios, CNPJs, status fiscal (SINTEGRA/Receita Federal) e contas banc?rias dos fornecedores.

---

## 3. Principais Regras de Auditoria & Cruzamentos (Regras Core)

### A. Triangula??o de Compra (3-Way Matching)
*   **Regra:** Validar se a Nota Fiscal de Entrada condiz rigorosamente com o Pedido de Compra aprovado e com o Registro de Recebimento de Materiais (comprovante de entrega f?sica no estoque).
*   **Cruzamento:** `NF-e (Itens, Quantidade, Pre?o Unit?rio)` vs `Pedido de Compra (PO)` vs `M?dulo de Recebimento F?sico (Estoque)`.
*   **Anomalia:** Pre?o faturado maior que o aprovado no pedido, faturamento de quantidades maiores do que as recebidas ou cobran?a de itens n?o solicitados.

### B. Fracionamento de Compras (Split Purchases)
*   **Regra:** Detectar compras da mesma categoria e fornecedor efetuadas em datas muito pr?ximas com valores fragmentados propositalmente para contornar os limites da al?ada de aprova??o de gerentes ou diretores.
*   **Cruzamento:** `Pedidos de Compra` agrupados por Comprador, Fornecedor, Categoria de Produto e Data (janela de 7 a 15 dias).
*   **Anomalia:** Fracionamento de despesa para burlar o fluxo formal de aprova??o da diretoria (descumprimento de governan?a corporativa).

### C. Conluio e Fraude em Processos de Sourcing (Cota??es Fakes)
*   **Regra:** Auditar a autenticidade das propostas concorrentes no processo de cota??o. Verificar se as cota??es apresentadas para simular concorr?ncia possuem ind?cios de conluio.
*   **Cruzamento:** `Dados Cadastrais dos Proponentes` (S?cios comuns, mesmo IP de envio, mesma data de cria??o de arquivo PDF da proposta, e-mails de contato semelhantes).
*   **Anomalia:** Cota??es "fakes" enviadas pelo mesmo grupo econ?mico ou pelo pr?prio comprador para favorecer uma empresa espec?fica.

### D. Compras de Fornecedores Irregulares ou N?o Homologados
*   **Regra:** Verificar se foram emitidas ordens de compra e pagamentos para fornecedores que n?o constam na lista de fornecedores homologados (SLA de Qualidade) ou que possuem restri??es fiscais/legais vigentes.
*   **Cruzamento:** `Vendor Master` vs `Pedidos de Compra` vs `Cadastro SEFAZ (Sintegra)`.
*   **Anomalia:** Aquisi??o de insumos de fornecedores inativos, inid?neos ou sem homologa??o.

### E. Desvio de Pre?os de Contrato (Price Leakage)
*   **Regra:** Monitorar contratos de fornecimento com tabelas de pre?o fixas ou reajustes peri?dicos homologados, garantindo que as compras ao longo do ano obede?am ? tabela contratual ativa.
*   **Cruzamento:** `NF-e (Valor Unit?rio)` vs `Contratos/Tabela de Pre?o Homologada`.
*   **Anomalia:** Perda de desconto por volume (*leakage*) ou faturamento com reajuste antecipado/n?o contratado.

---

## 4. Algoritmos de Detec??o e M?todos IA
- **An?lise de Grafos de Rela??o (Network Analysis):** Mapeamento de liga??es entre funcion?rios do setor de compras e s?cios das empresas de fornecimento cadastradas (conflito de interesses).
- **An?lise de Metadados de Arquivos (PDF Metadata):** Leitura autom?tica de metadados das propostas de cota??o enviadas por fornecedores concorrentes para verificar se foram geradas pelo mesmo computador ou autor.
- **An?lise de Regress?o de Pre?os:** Identifica??o de itens comprados fora da curva hist?rica de sazonalidade ou do pre?o m?dio de mercado para a categoria.

---

## 5. KPIs e M?tricas de Efici?ncia em Compras
- **Sourcing Compliance Rate:** Percentual de compras de alta al?ada que seguiram estritamente o rito de 3 cota??es v?lidas.
- **Leakage Financeiro em Compras (R$):** Valor total pago a mais por desvios de tabela contratual ou erros no *3-way matching*.
- **Concentra??o de Fornecedores (Herfindahl-Hirschman Index):** Grau de depend?ncia de fornecimento por categoria de produto.
- **Lead Time de Compras:** Tempo transcorrido entre a requisi??o inicial e a entrega do insumo.
