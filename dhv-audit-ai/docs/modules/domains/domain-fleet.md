# Dom?nio de Auditoria: Frota & TMS (Fleet & Fleet Operations Audit)

## 1. Vis?o Geral
O dom?nio de **Frota & TMS** foca na auditoria operacional e financeira de frotas pr?prias e subcontratadas (*terceirizados/agregados*). O objetivo primordial ? o controle minucioso dos principais ofensores de custo de uma frota (combust?vel, manuten??o, pneus e ped?gios) e a preven??o de fraudes, desvios e inefici?ncias na condu??o de ve?culos e ordens de transporte.

---

## 2. Fontes de Dados e Documentos Ingestados
- **Bilhetes de Telemetria e Rastreamento (GPS):** Dados contendo posi??es lat/long, velocidade, RPM e eventos de igni??o.
- **Transa??es de Cart?o de Abastecimento:** Registros eletr?nicos (ex: Ticket Log, Sem Parar, Valecard) contendo datas, postos, placas, od?metros, volumes e valores de combust?vel.
- **Ordens de Servi?o de Manuten??o (OS):** PDFs e registros estruturados das pe?as e servi?os realizados nas oficinas, internos ou externos.
- **Controle e Invent?rio de Pneus:** Registros de n?mero de fogo de pneus, medi??es de sulcos e movimenta??es (trocas de eixos/recapagem).
- **Passagens de Ped?gio Eletr?nico:** Registros de passagens em p?rticos de ped?gios com cobran?a via tag autom?tica.

---

## 3. Principais Regras de Auditoria & Cruzamentos (Regras Core)

### A. Fraudes em Abastecimento (M?dia de Consumo e Capacidade de Tanque)
*   **Regra:** Auditar se a quantidade de combust?vel faturada no posto ultrapassa a capacidade nominal do tanque do ve?culo e se o od?metro informado faz sentido f?sico com a transa??o anterior.
*   **Cruzamento:** `Cart?o de Abastecimento (Litros abastecidos, Od?metro)` vs `Ficha T?cnica do Ve?culo (Capacidade de Tanque)` vs `GPS (Localiza??o na hora da transa??o)`.
*   **Anomalia:** Abastecimento de volume superior ? capacidade f?sica do tanque, abastecimento de combust?vel inadequado (ex: gasolina em motor a diesel) ou transa??es realizadas com o ve?culo distante geograficamente do posto.

### B. Desvio de Rota e Uso de Ve?culo Fora do Expediente
*   **Regra:** Detectar se os ve?culos da empresa foram utilizados em rotas n?o planejadas pela opera??o, ou em hor?rios n?o autorizados de fins de semana e madrugadas.
*   **Cruzamento:** `GPS (Trajeto e Hor?rios)` vs `Planejamento de Rotas (TMS)` vs `Escala de Trabalho do Motorista`.
*   **Anomalia:** Uso pessoal de ve?culos da frota corporativa, gerando custos de combust?vel, pneus e riscos de sinistro n?o planejados.

### C. Auditoria de Cobran?a de Ped?gios (Eixos Suspensos)
*   **Regra:** Verificar se a concession?ria de ped?gio faturou a tarifa com base na quantidade real de eixos em contato com a pista, identificando cobran?as indevidas sobre eixos que estavam suspensos (ve?culo vazio).
*   **Cruzamento:** `Passagens de Ped?gio (Eixos faturados)` vs `GPS / Sensor de Eixo / MDF-e (Status de carregamento: Vazio/Carregado)`.
*   **Anomalia:** Pagamento de tarifa cheia de ped?gio para caminh?es transitando sem carga e com eixos devidamente suspensos.

### D. Fraudes e Desvios no Ciclo de Vida de Pneus
*   **Regra:** Rastrear a vida ?til de cada pneu (identificado por n?mero de fogo ou chip RFID), evitando a fraude de "troca de pneus novos por usados" e garantindo a correta recapagem no momento t?cnico ideal.
*   **Cruzamento:** `Invent?rio de Pneus` vs `Notas Fiscais de Compra` vs `Hist?rico de Manuten??o e OS`.
*   **Anomalia:** Sumi?o inexplic?vel de pneus novos ou descarte prematuro antes do limite t?cnico de desgaste do sulco.

### E. Superfaturamento e Pe?as N?o Trocadas em Manuten??es
*   **Regra:** Comparar o pre?o unit?rio das pe?as e horas-homem aplicados na ordem de servi?o de manuten??o com a tabela referencial de mercado e auditar a frequ?ncia de substitui??o de pe?as de desgaste r?pido.
*   **Cruzamento:** `Ordem de Servi?o (Pe?as/M?o de Obra)` vs `Tabela Referencial (MOP)` vs `Hist?rico de Trocas do Ve?culo`.
*   **Anomalia:** Troca recorrente e injustificada da mesma pe?a de alta durabilidade em prazos muito curtos (ind?cio de faturamento de pe?as n?o instaladas de fato ou desvios de estoque).

---

## 4. Algoritmos de Detec??o e M?todos IA
- **Algoritmo de Detec??o de Padr?o Geogr?fico (Geo-fencing/Anomalias):** Identifica??o autom?tica de paradas prolongadas em locais n?o homologados como postos de combust?vel, hot?is credenciados ou centros de distribui??o.
- **Redes Neurais Recorrentes (RNN) para Consumo:** Modelo preditivo baseado em intelig?ncia artificial que calcula o consumo esperado de combust?vel para cada trecho rodovi?rio, considerando a carga carregada, altitude/relevo do trajeto, vento e estilo de dire??o do motorista (telemetria), sinalizando desvios acima de 5%.

---

## 5. KPIs de Gest?o de Frota e Custos
- **Custo de Combust?vel por Km Rodado (CPK):** Indicador de efici?ncia energ?tica global da frota.
- **MTBF (Mean Time Between Failures):** Tempo m?dio entre falhas mec?nicas, avaliando a qualidade das manuten??es.
- **Tire Cost-per-Kilometer (CPK-Pneu):** Custo de amortiza??o e manuten??o de pneus por km rodado.
- **Sinistros e Multas por Milh?o de Km:** ?ndice de seguran?a operacional da frota.
