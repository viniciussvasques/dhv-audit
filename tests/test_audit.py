from fastapi.testclient import TestClient
from src.domain.entities import AuditCycle, Finding, FindingSeverity, AuditStatus
from src.application.use_cases import CreateAuditCycleUseCase, AddFindingUseCase
from src.infrastructure.repositories import InMemoryAuditRepository
from src.interfaces.api.main import app, repository

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "dhv-audit-ai"}

def test_audit_cycle_domain():
    cycle = AuditCycle(id="audit-1", tenant_id="tenant-10", company_name="Logística Alfa")
    assert cycle.status == AuditStatus.PENDING
    assert cycle.total_financial_impact() == 0.0

    finding = Finding(
        id="f-1",
        title="Cobrança Duplicada de Frete",
        description="Fatura 1234 cobrada em duplicidade.",
        severity=FindingSeverity.HIGH,
        financial_impact=5000.0,
        confidence_score=0.98
    )
    cycle.add_finding(finding)
    assert len(cycle.findings) == 1
    assert cycle.total_financial_impact() == 5000.0

def test_create_and_fetch_audit_flow_via_api():
    # Clear repo for test
    repository._storage.clear()

    # 1. Create audit cycle via API
    res_create = client.post("/api/v1/audits", json={
        "id": "cycle-99",
        "tenant_id": "tenant-alpha",
        "company_name": "Beta Transportes"
    })
    assert res_create.status_code == 200
    assert res_create.json()["id"] == "cycle-99"

    # 2. Add finding via API
    res_finding = client.post("/api/v1/audits/cycle-99/findings", json={
        "id": "find-1",
        "title": "Divergência de Peso Cubado",
        "description": "Peso faturado acima do aferido.",
        "severity": "medium",
        "financial_impact": 1200.50,
        "confidence_score": 0.92
    })
    assert res_finding.status_code == 200
    assert res_finding.json()["total_findings"] == 1
    assert res_finding.json()["total_impact"] == 1200.50

    # 3. Fetch audit cycle via API
    res_get = client.get("/api/v1/audits/cycle-99")
    assert res_get.status_code == 200
    data = res_get.json()
    assert data["company_name"] == "Beta Transportes"
    assert len(data["findings"]) == 1
    assert data["total_financial_impact"] == 1200.50
