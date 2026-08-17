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

def test_use_cases_gaps():
    from src.application.use_cases import AuditRepositoryInterface
    import pytest
    
    # Test abstract interface exceptions
    interface = AuditRepositoryInterface()
    with pytest.raises(NotImplementedError):
        interface.save(None)
    with pytest.raises(NotImplementedError):
        interface.find_by_id("1")
        
    # Test AddFindingUseCase cycle not found
    repo = InMemoryAuditRepository()
    use_case = AddFindingUseCase(repo)
    with pytest.raises(ValueError):
        use_case.execute("invalid-id", "f-1", "title", "desc", FindingSeverity.HIGH, 100.0, 0.95)

def test_api_error_branches():
    # 1. Get non-existing cycle_id -> 404
    response_get = client.get("/api/v1/audits/non-existent-id")
    assert response_get.status_code == 404
    assert "not found" in response_get.json()["detail"]
    
    # 2. Add finding to non-existing cycle -> 404
    response_find = client.post("/api/v1/audits/non-existent-id/findings", json={
        "id": "f-1",
        "title": "Title",
        "description": "Desc",
        "severity": "high",
        "financial_impact": 100.0,
        "confidence_score": 0.95
    })
    assert response_find.status_code == 404
    assert "not found" in response_find.json()["detail"]
    
    # 3. Create cycle with invalid body/conflict triggering Exception -> 400
    # Let's mock the use case execute method to raise an Exception
    from src.interfaces.api import main
    def mock_execute_fail(*args, **kwargs):
        raise Exception("Database insertion failed")
        
    original_uc = main.create_cycle_uc.execute
    main.create_cycle_uc.execute = mock_execute_fail
    try:
        response_err = client.post("/api/v1/audits", json={
            "id": "err-cycle",
            "tenant_id": "tenant-err",
            "company_name": "Err Corp"
        })
        assert response_err.status_code == 400
        assert "Database insertion failed" in response_err.json()["detail"]
    finally:
        main.create_cycle_uc.execute = original_uc


