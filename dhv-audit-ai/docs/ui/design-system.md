# Design System: Elementos de Marca, Tokens & Componentes Reutiliz?veis

O **DHV Audit AI Design System** ? constru?do sobre uma abordagem moderna, corporativa e de alto desempenho, otimizada para visualiza??o densa de dados (*data-dense dashboards*) e fluxos avan?ados de revis?o de intelig?ncia artificial.

---

## 1. Identidade de Marca & Paleta de Cores (Brand Identity)

A identidade visual equilibra a sobriedade corporativa da DHV Log com a tecnologia de ponta da Intelig?ncia Artificial. Adota-se um tema h?brido (Dark-first para workspace de consultores e Light-clean para o portal executivo de clientes).

### Paleta de Cores Prim?rias e Secund?rias
- **Primary (Blue Corporate):** `#0F172A` (Slate 900) e `#1E3A8A` (Dark Blue) - Transmite autoridade, confian?a e solidez.
- **Secondary (Tech Cyan):** `#06B6D4` (Cyan 500) - Usado para destacar a??es de intelig?ncia artificial, agentes ativos e insights autom?ticos.
- **Success (Green Metric):** `#10B981` (Emerald 500) - Utilizado para representar economias capturadas (*savings*), documentos processados com sucesso e status "Aprovado/Validado".
- **Warning (Orange Risk):** `#F59E0B` (Amber 500) - Usado para anomalias de m?dia gravidade e revis?es necess?rias de m?dia confian?a.
- **Danger (Red Critical):** `#EF4444` (Red 500) - Representa desvios graves, fraudes, duplicidade cr?tica e erros de sistema.
- **Backgrounds:**
  - *Light Mode (Portal Cliente):* `#F8FAFC` (Slate 50) com cart?es em `#FFFFFF`.
  - *Dark Mode (Workspace Consultor):* `#0B0F19` (Deep Navy) com cart?es em `#161D30` (Semi-glassmorphism).

---

## 2. Efeitos Visuais, Sidebar & Header (Visual Effects)

### A. Efeito Glassmorphism & Blurs
Para dar profundidade tecnol?gica ? interface, os pain?is flutuantes e cart?es no Workspace de Consultores utilizam efeito de desfoque de fundo (*backdrop-blur*):
- `background: rgba(22, 29, 48, 0.85)`
- `backdrop-filter: blur(12px)`
- `border: 1px solid rgba(255, 255, 255, 0.08)`
- `box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37)`

### B. Sidebar Lateral Interativa (Responsive Sidebar)
- **Design:** Fundo escuro Deep Navy com gradiente sutil na borda direita (`border-r border-slate-800`).
- **Anima??es & Transi??es:** Transi??o suave de largura (`transition-all duration-300 ease-in-out`) ao contrair/expandir.
- **Efeito Hover:** Itens do menu mudam de cor com uma transi??o suave. Aplica-se uma barra vertical neon de `3px` (`#06B6D4`) ? esquerda do item selecionado para feedback instant?neo de localiza??o.
- **Indicador de Status da IA:** Exibe um indicador pulsante azul no rodap? da Sidebar representando a lat?ncia e o status dos agentes de IA em segundo plano.

### C. Header Superior Persistente (Sticky Header)
- **Design:** Fixado no topo (`sticky top-0 z-50`) com desfoque de fundo (`backdrop-blur-md`) e borda inferior transl?cida.
- **Elementos do Header:**
  - Seletor r?pido de Tenant / Empresa (para consultores gerenciarem m?ltiplos clientes).
  - Central de Notifica??es em tempo real (conclus?o de OCR, novos achados cr?ticos).
  - Perfil do Usu?rio com avatar e indica??o clara do seu papel (ex: `Consultant`).

---

## 3. Componentes Core Reutiliz?veis (Core Components)

### A. Tabela de Dados Densa com Filtros (Data Table)
- **Funcionalidades:** Ordena??o de colunas por clique, pagina??o embutida, sele??o de m?ltiplas linhas para a??es em lote.
- **Modo Destaque (Filtro IA):** Toggle r?pido para filtrar apenas "Itens sinalizados pela IA que necessitam de revis?o humana".

### B. Cart?o de M?tricas (KPI Metric Card)
- **Design:** Exibe o valor em destaque (ex: `R$ 145.230,00` de economia), uma varia??o percentual de alta ou baixa com ?cone de seta, e um mini-gr?fico (*sparkline*) em SVG para visualiza??o da tend?ncia temporal.

### C. Dropzone de Upload de Arquivos
- **Design:** Borda pontilhada com anima??o ao arrastar arquivos (`drag-over`). Exibe uma fila din?mica contendo barras de progresso lineares individuais e o status em tempo real do processamento (`Enviando` ? `Executando OCR` ? `Analisando IA` ? `Conclu?do`).

### D. Badge de Confian?a da IA (AI Confidence Badge)
- **L?gica de Cores Din?micas:**
  - Confian?a `กร 90%`: Borda e texto verdes (`text-emerald-500 bg-emerald-500/10`).
  - Confian?a `70% - 89%`: Borda e texto amarelos (`text-amber-500 bg-amber-500/10`).
  - Confian?a `< 70%` (Revis?o Obrigat?ria): Borda e texto vermelhos (`text-rose-500 bg-rose-500/10`).
