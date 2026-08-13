from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.domain.entities import FindingSeverity, AuditStatus
from src.application.use_cases import CreateAuditCycleUseCase, AddFindingUseCase
from src.infrastructure.repositories import InMemoryAuditRepository

app = FastAPI(
    title="DHV Audit AI API",
    description="API corporativa de auditoria inteligente com IA — DHV Log Consultoria",
    version="1.0.0"
)

repository = InMemoryAuditRepository()
create_cycle_uc = CreateAuditCycleUseCase(repository)
add_finding_uc = AddFindingUseCase(repository)

class CreateCycleRequest(BaseModel):
    id: str
    tenant_id: str
    company_name: str

class AddFindingRequest(BaseModel):
    id: str
    title: str
    description: str
    severity: FindingSeverity
    financial_impact: float
    confidence_score: float

@app.get("/health", tags=["System"])
def health_check():
    return {"status": "healthy", "service": "dhv-audit-ai"}

@app.post("/api/v1/audits", tags=["Audit Cycles"])
def create_audit_cycle(req: CreateCycleRequest):
    try:
        cycle = create_cycle_uc.execute(req.id, req.tenant_id, req.company_name)
        return {"id": cycle.id, "tenant_id": cycle.tenant_id, "company_name": cycle.company_name, "status": cycle.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/audits/{cycle_id}/findings", tags=["Findings"])
def add_finding(cycle_id: str, req: AddFindingRequest):
    try:
        cycle = add_finding_uc.execute(
            cycle_id=cycle_id,
            finding_id=req.id,
            title=req.title,
            description=req.description,
            severity=req.severity,
            impact=req.financial_impact,
            confidence_score=req.confidence_score
        )
        return {
            "audit_id": cycle.id,
            "total_findings": len(cycle.findings),
            "total_impact": cycle.total_financial_impact()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/audits/{cycle_id}", tags=["Audit Cycles"])
def get_audit_cycle(cycle_id: str):
    cycle = repository.find_by_id(cycle_id)
    if not cycle:
        raise HTTPException(status_code=404, detail="Audit cycle not found")
    return {
        "id": cycle.id,
        "tenant_id": cycle.tenant_id,
        "company_name": cycle.company_name,
        "status": cycle.status,
        "findings": [
            {
                "id": f.id,
                "title": f.title,
                "description": f.description,
                "severity": f.severity,
                "financial_impact": f.financial_impact,
                "confidence_score": f.confidence_score,
                "is_validated": f.is_validated
            } for f in cycle.findings
        ],
        "total_financial_impact": cycle.total_financial_impact()
    }
