# DHV Audit AI Platform

Plataforma corporativa de auditoria inteligente assistida por Inteligência Artificial para operações logísticas e financeiras da DHV Log Consultoria.

## O que é
O **DHV Audit AI** automatiza a ingestão de documentos (faturas, XMLs de frete e notas fiscais, folhas de pagamento, contratos), extrai dados estruturados via OCR e IA multimodal, cruza informações com regras de negócio e benchmarks setoriais, detecta anomalias e gera planos de ação acionáveis com validação humana especializada (*human-in-the-loop*).

## Tech Stack
- **Linguagem:** Python 3.11+
- **Framework Web:** FastAPI (ASGI)
- **Validação de Dados:** Pydantic v2
- **Banco de Dados:** PostgreSQL com suporte a Multi-tenancy
- **IA & OCR:** Integração com LLMs multimodais e motores de OCR
- **Testes:** Pytest com cobertura estrita (>80%)

## Quick Start (Desenvolvimento Local)

### Pré-requisitos
- Python 3.11+ instalado
- Docker e Docker Compose (para banco de dados PostgreSQL)

### Instalação
```bash
# Clone o repositório
git clone https://github.com/vasquesinnexar-bit/dhv-audit-ai.git
cd dhv-audit-ai

# Setup automatizado (venv + dependências + .env)
bash scripts/setup-dev.sh
source venv/bin/activate

# Ou manualmente:
# python -m venv venv && source venv/bin/activate
# pip install -r requirements.txt
# cp .env.example .env
```

### Executando os Testes
```bash
pytest --cov=src --cov-report=term-missing
```

### Executando a API
```bash
uvicorn src.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000
```

## Variáveis de Ambiente
| Variável | Descrição | Obrigatória | Padrão |
|---|---|---|---|
| `DATABASE_URL` | String de conexão PostgreSQL | Sim | `postgresql://postgres:postgres@localhost:5432/dhv_audit` |
| `JWT_SECRET` | Chave secreta para autenticação JWT | Sim | `super-secret-key-change-in-production` |
| `LLM_API_KEY` | Chave de API para o motor de IA | Sim | `sk-placeholder` |

## Estrutura do Projeto
```
dhv-audit-ai/
├── src/
│   ├── domain/           # Entidades, enums e regras de negócio puras
│   ├── application/      # Casos de uso e orquestração
│   ├── infrastructure/   # Repositórios, DB, IA/OCR, storage
│   └── interfaces/       # Adaptadores HTTP (FastAPI)
├── tests/                # Testes automatizados (pytest)
├── docs/                 # Plano mestre, módulos e ADRs
├── scripts/              # Scripts de setup e automação
├── .github/workflows/    # CI (lint, typecheck, testes)
├── docker-compose.yml    # PostgreSQL + API
├── Dockerfile
├── Makefile              # Comandos de desenvolvimento
├── pyproject.toml        # Config pytest, ruff, mypy, coverage
├── requirements.txt
└── .env.example
```

## Comandos úteis
```bash
make install    # instala dependências
make dev        # sobe API em http://localhost:8000
make test       # executa testes
make lint       # ruff
make coverage   # pytest com cobertura
make docker-up  # sobe stack Docker
```
