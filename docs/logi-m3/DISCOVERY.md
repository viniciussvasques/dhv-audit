# DISCOVERY – Módulo 3 (TMS – Núcleo Operacional)

## Contexto
O módulo **TMS (Transport Management System)** será o núcleo operacional da plataforma SaaS de Gestão de Logística. Ele será responsável por orquestrar todo o fluxo de transporte: criação de ordens de carga, planejamento de rotas, alocação de recursos (veículos, motoristas), monitoramento em tempo real e integração com os módulos Financeiro (M2) e Operacional.

## Objetivos Principais
1. **Gestão de Ordens de Carga** – CRUD completo, ciclo de vida (draft, scheduled, in‑transit, delivered, cancelled).
2. **Planejamento de Rotas** – algoritmo de otimização (distância/tempo/custo) com suporte a múltiplas paradas.
3. **Alocação de Recursos** – matching de veículos e motoristas, regras de capacidade, disponibilidade.
4. **Monitoramento em Tempo Real** – ingestão de telemetria (GPS), eventos de status, visualização no dashboard.
5. **Integração** – eventos e APIs para Financeiro (faturamento automático) e Operacional (notificações, relatórios).

## Stakeholders
- **Operações** – equipe de planejamento de rotas e gestores de frota.
- **Financeiro** – precisa de dados de custos de transporte para faturamento.
- **Clientes** – rastreamento de entregas em tempo real via portal.
- **Diretoria** – métricas de eficiência (KPIs: custo por km, tempo médio de entrega).

## Restrições Técnicas
- **RLS** – isolamento por tenant em todas as tabelas (similar ao M2).
- **Escalabilidade** – suportar até 10 000 ordens simultâneas e 2 000 veículos.
- **Latência** – atualização de status em < 5 s para eventos críticos.
- **Compliance** – logs de auditoria, GDPR para dados de localização.

## Métricas de Sucesso
- **90 %** das rotas planejadas com otimização de custo ≥ 10 % vs baseline.
- **Tempo médio de entrega** ≤ 48 h para cargas domésticas.
- **Disponibilidade** da API ≥ 99,9 %.
- **Cobertura de testes** ≥ 85 %.

## Próximos Passos (Planejamento)
- Definir modelagem de dados (ordens, veículos, motoristas, eventos).
- Escolher algoritmo de roteamento (OSRM, GraphHopper ou solução própria).
- Mapear eventos de integração com M2 (faturamento ao fechar entrega).
- Estimar effort e prioridades (RICE) para backlog inicial.
