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
git clone https://github.com/dhvlog/dhv-audit-ai.git
cd dhv-audit-ai

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
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
- `src/domain/`: Entidades de negócio e regras puras.
- `src/application/`: Casos de uso e orquestração de auditorias.
- `src/interfaces/`: Adaptadores de entrada (Rotas FastAPI).
- `src/infrastructure/`: Repositórios, persistência e serviços externos.
- `docs/`: Documentação completa, planos mestre e ADRs.
- `tests/`: Suíte de testes automatizados.
