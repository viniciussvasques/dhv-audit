from typing import List, Optional
from src.domain.entities import AuditCycle, Finding, FindingSeverity, AuditStatus

class AuditRepositoryInterface:
    def save(self, cycle: AuditCycle) -> None:
        raise NotImplementedError
    def find_by_id(self, cycle_id: str) -> Optional[AuditCycle]:
        raise NotImplementedError

class CreateAuditCycleUseCase:
    def __init__(self, repository: AuditRepositoryInterface):
        self.repository = repository

    def execute(self, cycle_id: str, tenant_id: str, company_name: str) -> AuditCycle:
        cycle = AuditCycle(
            id=cycle_id,
            tenant_id=tenant_id,
            company_name=company_name,
            status=AuditStatus.PENDING
        )
        self.repository.save(cycle)
        return cycle

class AddFindingUseCase:
    def __init__(self, repository: AuditRepositoryInterface):
        self.repository = repository

    def execute(self, cycle_id: str, finding_id: str, title: str, description: str, severity: FindingSeverity, impact: float, confidence_score: float) -> AuditCycle:
        cycle = self.repository.find_by_id(cycle_id)
        if not cycle:
            raise ValueError(f"Audit cycle {cycle_id} not found")
        
        finding = Finding(
            id=finding_id,
            title=title,
            description=description,
            severity=severity,
            financial_impact=impact,
            confidence_score=confidence_score
        )
        cycle.add_finding(finding)
        self.repository.save(cycle)
        return cycle
