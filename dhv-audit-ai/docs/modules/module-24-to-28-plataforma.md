# Módulos M24–M28 — Plataforma & Escala

---

## M24 — Portal do Cliente (Self-Service)

### Objetivo
Interface self-service para empresas clientes gerenciarem suas auditorias.

### Telas

| Tela | Funcionalidades |
|---|---|
| Dashboard | KPIs, economia, achados pendentes, progresso |
| Documentos | Upload drag-and-drop, status de processamento |
| Achados | Lista filtrada, detalhe com evidências, aprovar/rejeitar |
| Plano de Ação | Ações recomendadas, marcar como concluída |
| Relatórios | Download PDF/PPTX, histórico |
| Contas Bancárias | Conectar via Open Banking, upload OFX |
| Configurações | Usuários do cliente, notificações |

---

## M25 — Integration Hub (iPaaS)

### Objetivo
Conectores padronizados para importação automática de dados.

### Conectores

| Conector | Protocolo | Dados |
|---|---|---|
| SAP | RFC/OData | FI, MM, HR modules |
| TOTVS Protheus | REST API | Financeiro, compras, RH |
| Sankhya | REST API | ERP completo |
| Omie | REST API | Financeiro, NF-e |
| Bling | REST API | NF-e, estoque |
| SEFAZ | Web Service | NF-e, CT-e, eventos |
| eSocial | Web Service | Eventos trabalhistas |
| Open Banking | API OF | Extratos, transações |
| Email (IMAP) | IMAP | Documentos recebidos |
| SFTP | SFTP | Arquivos batch |
| Webhook | HTTP POST | Eventos customizados |

### Arquitetura do Conector

```python
class IntegrationConnector(Protocol):
    connector_id: str
    def authenticate(self, credentials: dict) -> bool: ...
    def fetch_documents(self, since: datetime) -> List[RawDocument]: ...
    def fetch_transactions(self, account: BankAccount, period: DateRange) -> List[Transaction]: ...
    def test_connection(self) -> ConnectionStatus: ...
```

Configuração de conectores via Admin Panel com credenciais criptografadas.

---

## M26 — Knowledge Base & Metodologia

### Objetivo
Central de conhecimento com playbooks, metodologias e onboarding.

### Conteúdo

| Tipo | Exemplo |
|---|---|
| Playbooks | "Auditoria de frete — passo a passo" |
| Checklists | Documentos necessários por domínio |
| Templates | Modelos de workpaper, relatório, contestação |
| Treinamento | Módulos e-learning para consultores |
| FAQ | Perguntas frequentes por domínio |
| Glossário | Termos técnicos logísticos/fiscais |

---

## M27 — Marketplace de Regras & Plugins

### Objetivo
Ecossistema extensível onde parceiros e a própria DHV publicam regras e plugins.

### Funcionalidades

- Publicar pacote de regras (ex: "Auditoria Farma ANVISA")
- Instalar/desinstalar por tenant
- Rating e reviews de pacotes
- Revenue share para criadores de plugins

---

## M28 — White-label & Multi-marca

### Objetivo
Permitir que outras consultorias usem a plataforma com sua própria marca.

### Funcionalidades

| Feature | Descrição |
|---|---|
| Branding customizado | Logo, cores, domínio próprio |
| Isolamento total | Dados, usuários, config separados |
| Admin próprio | Cada white-label tem seu super admin |
| Billing separado | Faturamento independente |
| Feature flags | Ativar/desativar módulos por marca |
