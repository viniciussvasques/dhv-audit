# Dom?nio de Auditoria: Recursos Humanos & Folha de Pagamento (HR & Payroll Audit)

## 1. Vis?o Geral
O dom?nio de **Recursos Humanos & Folha de Pagamento** foca na auditoria cont?nua de folhas de pagamento, recolhimento de encargos sociais, cumprimento de conven??es coletivas de trabalho (CCT) e controle de ponto. O objetivo principal ? mitigar passivos trabalhistas, identificar fraudes internas (funcion?rios fantasma, horas extras indevidas) e otimizar custos com benef?cios e impostos sobre a folha.

---

## 2. Fontes de Dados e Documentos Ingestados
- **Folha de Pagamento Anal?tica:** Relat?rios de proventos e descontos detalhados por funcion?rio e rubrica (sistema de folha ERP, ex: RM Labore, Protheus SIGAGPE).
- **Eventos do eSocial:** Arquivos XML dos eventos peri?dicos (`S-1200` - Remunera??o, `S-1210` - Pagamentos, `S-2200` - Admiss?o, `S-2230` - Afastamentos).
- **Registros de Ponto Eletr?nico:** Arquivos espelho de ponto, batidas di?rias (padr?o Portaria 671 do MTE) e relat?rios de banco de horas.
- **Guias de Encargos Fiscais:** DCTFWeb, guias de FGTS (GRF/GRRF) e DARF de INSS e IRRF.
- **Acordos e Conven??es Coletivas (CCT):** Regulamentos de sindicatos que estabelecem pisos salariais, adicionais de horas extras, adicionais noturnos e aux?lios.

---

## 3. Principais Regras de Auditoria & Cruzamentos (Regras Core)

### A. Auditoria de Horas Extras vs. Registro de Ponto
*   **Regra:** Auditar se as horas extras pagas na folha de pagamento correspondem estritamente ?s horas registradas e validadas no sistema de ponto, aplicando os percentuais corretos da CCT (ex: 50%, 100%).
*   **Cruzamento:** `Folha de Pagamento (Rubrica Horas Extras)` vs `Espelho de Ponto (Saldo do M?s)`.
*   **Anomalia:** Horas extras pagas sem correspond?ncia no ponto ou erro na taxa multiplicadora de c?lculo.

### B. Benef?cios Indevidos em Per?odo de Afastamento ou F?rias
*   **Regra:** Verificar se colaboradores afastados por licen?a m?dica, licen?a-maternidade ou em gozo de f?rias continuam recebendo benef?cios de uso exclusivo em servi?o ativo (ex: Vale Transporte, Vale Refei??o/Alimenta??o).
*   **Cruzamento:** `Hist?rico de Afastamentos/F?rias (S-2230)` vs `Demonstrativo de Cr?dito de Benef?cios`.
*   **Anomalia:** Desperd?cio de recursos com concess?o indevida de vales e aux?lios-transporte.

### C. Diverg?ncia de Recolhimento de Encargos (INSS/FGTS)
*   **Regra:** Recalcular de forma independente as bases e valores de INSS, FGTS e IRRF devidos para cada colaborador e confrontar com o valor de fato declarado/recolhido na DCTFWeb e FGTS Digital.
*   **Cruzamento:** `Bases de C?lculo da Folha` vs `Guias Recolhidas` vs `eSocial S-1200`.
*   **Anomalia:** Sub-recolhimento (gerando risco de multas fiscais) ou recolhimento em duplicidade sobre verbas indenizat?rias (gerando oportunidade de recupera??o tribut?ria).

### D. Identifica??o de "Funcion?rios Fantasma" e Diverg?ncia Cadastral
*   **Regra:** Confrontar o cadastro ativo da folha de pagamento com as bases do eSocial, do controle de acesso f?sico das catracas e logs de logins de TI.
*   **Cruzamento:** `Folha de Pagamento` vs `eSocial (S-2200)` vs `Logs de Catraca/VPN/AD`.
*   **Anomalia:** Pagamento de sal?rios para cadastros inativos, demitidos ou "fantasmas" que n?o registram atividade corporativa.

### E. Risco Trabalhista por F?rias Vencidas em Dobro
*   **Regra:** Mapear colaboradores que est?o prestes a vencer o per?odo concessivo de f?rias (24 meses ap?s a admiss?o ou per?odo aquisitivo anterior), gerando obrigatoriedade de pagamento em dobro.
*   **Cruzamento:** `Hist?rico de Admiss?es/Per?odos Aquisitivos` vs `F?rias Gozadas`.
*   **Anomalia:** Alerta de risco iminente de autua??o tribut?ria ou pagamento duplo de f?rias por neglig?ncia operacional.

---

## 4. Algoritmos de Detec??o e M?todos IA
- **Algoritmo de An?lise de Padr?o Temporal (Ponto Coerente):** Identifica??o autom?tica de marca??es de ponto id?nticas e sem varia??o de minutos ("ponto brit?nico"), o que invalida juridicamente o registro de ponto.
- **Detec??o de Anomalias de Rubrica (Outlier Detection):** Modelagem estat?stica para detectar picos at?picos de comiss?es, b?nus ou adicionais pagos a colaboradores de um mesmo cargo/setor.

---

## 5. KPIs e M?tricas de Mitiga??o de Passivos
- **Passivo Trabalhista Estimado (R$):** Valor total sob risco devido a f?rias vencidas, excesso de horas extras acumuladas e falta de descanso obrigat?rio de 11h entre jornadas.
- **?ndice de Absente?smo:** Percentual de aus?ncias e atestados m?dicos de forma agrupada por setor/gestor.
- **Saving de Benef?cios:** Redu??o de custos com a suspens?o de benef?cios a funcion?rios de f?rias ou afastados.
- **Diverg?ncia Tribut?ria Identificada:** Diferen?a entre o c?lculo do sistema e o valor pago de impostos, destacando cr?ditos pass?veis de compensa??o.
