# Metodologia de Auditoria Zero-Waste (Contabilidade Total de Ativos e Despesas)

Esta especifica??o define a **Metodologia de Auditoria Zero-Waste (Contabilidade Total)** do `dhv-audit-ai`. Projetada para revolucionar o mercado de auditoria tradicional, ela vai al?m de simples faturamentos e amostragem de grandes transa??es: seu escopo consiste em **auditar cada centavo, cada ativo, cada item f?sico e cada segundo de trabalho**, eliminando micro-desperd?cios e inefici?ncias operacionais invis?veis (desde gastos com papelaria e canetas sem uso at? a deprecia??o e efici?ncia de ve?culos de frota por ano/modelo).

---

## 1. O Conceito: "Contabilidade Total" (Granularidade Absoluta)

A auditoria tradicional foca na **materialidade estat?stica** (ignora transa??es abaixo de um limiar, por exemplo, R$ 5.000,00). A Metodologia Zero-Waste inverte essa l?gica usando IA para **analisar 100% dos lan?amentos com materialidade zero**, capturando o efeito cumulativo de milhares de micro-vazamentos de caixa.

```
忙式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式忖
弛                       AUDITORIA TRADICIONAL                             弛
弛   Analisa apenas faturas ￣ R$ 5.000 (Amostragem) ? Ignora o Resto       弛
戌式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式成式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式戎
                                    ∪
忙式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式忖
弛                     AUDITORIA ZERO-WASTE (IA)                          弛
弛   Analisa 100% das transa??es (Papelaria, Consumo, Pe?as, Horas, etc.) 弛
弛   ? Captura o efeito cumulativo de micro-desperd?cios (Soma de Centavos)弛
戌式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式式戎
```

---

## 2. Pilares de An?lise Granular da Contabilidade Total

### A. Micro-Despesas e Consum?veis (Suprimentos de Escrit?rio e Materiais N?o Utilizados)
*   **O Problema Comum:** Compras descentralizadas de materiais (canetas, papel, toners, copos descart?veis) que ficam obsoletos no estoque interno, desaparecem ou s?o superfaturados.
*   **Regra de Auditoria IA:**
  - **Triangula??o de Consumo real:** `XML de Entrada de Papelaria (Quantidade de Canetas/Papel)` vs `Requisi??es de Almoxarifado` vs `Controle de Usu?rios Ativos`.
  - **Diferencia??o Sem?ntica:** A IA agrupa compras de suprimentos de escrit?rio por funcion?rio e sinaliza anomalias de taxa de consumo (ex: 50 canetas por colaborador ao m?s).
  - **Insumos Ociosos (Sinaliza??o de Obsolesc?ncia):** Identifica??o de itens parados em estoque de almoxarifado sem movimenta??o por mais de 90 dias, sugerindo interrup??o de compra e liquida??o do estoque antes de novas aquisi??es.

### B. Manuten??o de Ve?culos, Idade da Frota (Ano do Ve?culo) e Efici?ncia
A plataforma implementa um modelo de **Custo Total de Propriedade & Efici?ncia de Ativos (TCO-A)** para cada placa de ve?culo:
*   **M?trica de Curva de Deprecia??o vs. Manuten??o:**
    A IA calcula a rela??o entre o **Ano do Ve?culo (Idade)** e a **Frequ?ncia/Custo de Manuten??o**. 
    - Se um ve?culo ano `2015` consome mais combust?vel (baixa efici?ncia de km/L) e gera mais ordens de servi?o de manuten??o corretiva do que o custo de amortiza??o de um ve?culo novo de ano `2024`, a IA gera automaticamente uma recomenda??o de **desinvestimento/renova??o de ativo**.
*   **Confronto de Pe?as Usadas vs. Novas:**
    - A IA cruza o hist?rico de Ordens de Servi?o (OS) com as Notas Fiscais de Pe?as. Se o sistema apontar uma troca de embreagem a cada 6 meses no mesmo ve?culo, a plataforma sinaliza um desvio (ind?cio de pe?a de m? qualidade, m? condu??o do motorista ou fraude de faturamento de pe?a n?o instalada).

### C. Horas Extras e Produtividade Inativa
*   **O Problema Comum:** Horas extras sistem?ticas decorrentes de inefici?ncia de processos ou desvios de conduta ("estender o hor?rio" sem necessidade real).
*   **Regra de Auditoria IA:**
  - **Cruzamento de Produtividade Ativa:** `Espelho de Ponto (Horas Extras Registradas)` vs `Logs de Produ??o do ERP / Logins em Sistemas` vs `Entradas/Sa?das de Carga no TMS`.
  - **Anomalia de Ociosidade Pagando Horas:** A IA identifica colaboradores que registraram 2 horas extras, mas cujos computadores de trabalho ou sistemas de faturamento n?o registraram nenhuma atividade de teclado/mouse ou entrada de dados nos ?ltimos 120 minutos da jornada (hora extra fantasma/ociosa).

---

## 3. O "Motor Centavo a Centavo" (C?lculos de Fra??es de Precis?o)

Para se posicionar como a melhor auditoria do mercado, a plataforma adota t?cnicas de micro-precis?o financeira:

1. **Auditoria de Arredondamento Financeiro:** 
   An?lise sistem?tica das d?zimas peri?dicas em notas fiscais, c?lculos de frete de peso cubado e juros. A plataforma recalcula os impostos com 4 casas decimais e confronta com o valor emitido. Arredondamentos feitos de forma indevida a favor de fornecedores (ex: R$ 0,02 por nota) em volumes de 500.000 notas fiscais representam um vazamento silencioso de **R$ 10.000,00**.
2. **Double-Invoice Check por Metadados de Linha:**
   Tradicionalmente, a deduplica??o de notas foca no n?mero do documento. O motor Zero-Waste analisa o **Item da Nota (NCM/Descri??o)**. Se um fornecedor emite duas notas com n?meros diferentes em dias consecutivos, contendo exatamente os mesmos itens, quantidades e valores de frete, a IA emite um alerta de faturamento duplicado fraudulento.

---

## 4. O Dashboard "Vazamento Zero" (Leakage Dashboard)

Esta nova visualiza??o foca na exibi??o detalhada de cada centavo recuper?vel:

- **Indicador de Micro-Desperd?cio (Micro-Waste Gauge):** Exibe a soma de todas as anomalias abaixo de R$ 50,00 que, somadas, representam valores volumosos.
- **Gr?fico de Efici?ncia de Ativo por Placa e Ano:** Um gr?fico de dispers?o (*scatter plot*) onde o eixo Y ? o custo de manuten??o por km rodado e o eixo X ? o ano do ve?culo, destacando instantaneamente as frotas obsoletas.
- **Tabela de Invent?rio Ocioso (Dead-Stock Table):** Exibe materiais de expediente e pe?as de reposi??o que foram comprados mas est?o h? meses sem consumo real, sugerindo devolu??o ao fornecedor ou remanejamento de filiais.

---

## 5. Implementa??o T?cnica: Algoritmo original BMV-PAE

A materializa??o da metodologia Zero-Waste ? realizada de forma nativa e program?tica na plataforma atrav?s do **Brazilian Multi-Vector Probabilistic Audit Engine (BMV-PAE)** localizado em `src/domain/statistical_audit.py`.

Este motor probabil?stico original avalia transa??es cruzando tr?s vetores matem?ticos complementares:

### A. Teste de Benford Chi-Quadrado ($p$-valor)
Mede a conformidade dos primeiros d?gitos significativos dos valores financeiros de 100% dos documentos com base na distribui??o logar?tmica natural:
$$P(d) = \log_{10}\left(1 + \frac{1}{d}\right), \quad d \in \{1, \dots, 9\}$$
Desvios estat?sticos severos ($p\text{-valor} < 0.05$) calculados sobre a distribui??o amostral pelo teste Chi-Quadrado com 8 graus de liberdade sinalizam manipula??es manuais ou falsifica??es sistem?ticas de notas.

### B. Probabilidade de Outliers por Z-Score
Aplica c?lculo de dispers?o normal sobre os pre?os unit?rios de mercadorias ou servi?os tomados de mesma classifica??o fiscal brasileira (mesmo NCM ou servi?o):
$$Z = \frac{x - \mu}{\sigma}$$
Valores extremos ($|Z| > 3.0$) representam distor??es grosseiras com probabilidade de ocorr?ncia natural menor que $0.27\%$, revelando superfaturamento ou erros fiscais grosseiros que infringem o Regulamento do ICMS e do SPED.

### C. Anomalia Temporal de Frequ?ncia por Poisson
Mede a probabilidade de ocorr?ncia de clusters at?picos de eventos em uma mesma janela temporal (horas extras de um funcion?rio no mesmo dia ou pedidos de compra sucessivos para o mesmo fornecedor) com base no hist?rico comportamental daquela entidade espec?fica ($\lambda$):
$$P(X \ge k) = 1 - \sum_{i=0}^{k-1} \frac{\lambda^i e^{-\lambda}}{i!}$$
Surtos de frequ?ncia com probabilidade infinitesimal sugerem fracionamento de compras para burlar al?adas ou lan?amento artificial de horas extras na CLT (Art. 59).

---

## 6. Diagn?stico e Perfilamento de Recursos Comparativo (EPCE-Engine)

O motor **MPE-IR (Motor de Perfilamento e Efici?ncia Individual de Recursos)**, implementado de forma original em `src/domain/resource_efficiency.py`, introduz a auditoria comparativa de performance em circunst?ncias id?nticas (*peer-to-peer cohorts*). Ele ? projetado para auditar o rendimento e os custos de cada colaborador, motorista, ativo f?sico ou sistema de software contratado, e projetar a perda financeira anual acumulada.

### A. O Algoritmo de Coorte Homog?nea (Benchmarking de Pares)
Para evitar compara??es injustas (como comparar um motorista de rota plana com um de rota montanhosa, ou um digitador de notas complexas com um de notas simples), o sistema constr?i coortes homog?neas din?micas baseadas em:
- `activity_type`: Tipo de atividade (ex: `delivery_route`, `invoice_parsing`).
- `context_key`: Contexto id?ntico de opera??o (ex: rota espec?fica `SP-RJ`, ou tipo de documento `NFS-e_manual`).

### B. C?lculo de Efici?ncia Relativa
Para cada recurso dentro da coorte, calcula-se o custo unit?rio por output produzido ($CU$) e o rendimento por hora de trabalho ($RH$):
$$CU = \frac{\text{Custo Total Incorrido}}{\text{Unidades Produzidas}}$$
$$RH = \frac{\text{Unidades Produzidas}}{\text{Tempo Decorrido em Horas}}$$

A efici?ncia relativa comparativa ($E$) de um recurso ? expressa em uma escala de $0.0$ a $1.0$, onde $1.0$ representa a melhor pr?tica encontrada (menor custo unit?rio de opera??o na coorte):
$$E = \frac{CU_{\text{best}}}{CU_{\text{target}}}$$

### C. Proje??o de Desperd?cio Anualizado Cumulativo (Leakage Projection)
Caso o recurso possua um custo unit?rio acima da **Mediana dos Pares** daquela mesma coorte, a plataforma quantifica o preju?zo financeiro anualizado caso a lideran?a n?o realize treinamento ou substitui??o daquele recurso:
$$\text{Vazamento Anual} = (CU_{\text{target}} - CU_{\text{median}}) \times \text{Produ??o Anual Projetada}$$

A produ??o anual ? projetada de forma linear baseada na taxa hist?rica do recurso extrapolada para um ano operacional padr?o de 1.800 horas produtivas:
$$\text{Produ??o Anual Projetada} = RH_{\text{target}} \times 1800$$

### D. Casos de Sucesso em Auditoria de Recursos e Ativos

1. **Efici?ncia de Combust?vel em Frota (Motorista A vs. Motorista B):**
   - **Caso:** Motorista A e Motorista B realizam o trajeto `SP-RJ` no mesmo tipo de ve?culo (ano/modelo equivalente).
   - **Diagn?stico:** O Motorista B possui custo de combust?vel de R$ 1,50/Km, enquanto o Motorista A possui custo de R$ 2,50/Km (devido ao seu estilo de condu??o agressivo sinalizado por picos de RPM na telemetria).
   - **Insight:** O motor MPE-IR calcula que o Motorista A est? gerando um desperd?cio invis?vel anualizado de **R$ 27.000,00** em compara??o ao par mediano, permitindo o direcionamento preciso para treinamento de dire??o econ?mica.
2. **Desempenho de Sistemas / ERPs vs. Humanos (Digitadores de Notas):**
   - **Caso:** An?lise de digitadores manuais de notas fiscais de servi?os tomados (`NFSe_manual`).
   - **Diagn?stico:** O sistema aponta que o Colaborador C tem um rendimento de apenas 5 notas/hora (gerando um custo por nota de R$ 6,00), enquanto a m?dia/mediana da equipe ? de 10 notas/hora (custo de R$ 3.000,00 ao ano desperdi?ado por falta de rendimento).
   - **Insight:** O sistema prop?e a automatiza??o definitiva deste recurso pelo m?dulo de OCR com IA (M2), que opera com custo unit?rio de R$ 0,10 por nota, gerando ganho de escala imediato.


