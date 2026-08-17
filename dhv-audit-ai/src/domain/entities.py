from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class FindingSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AuditStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    ANALYZED = "analyzed"
    VALIDATED = "validated"
    COMPLETED = "completed"

@dataclass
class Finding:
    id: str
    title: str
    description: str
    severity: FindingSeverity
    financial_impact: float
    confidence_score: float
    is_validated: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class AuditCycle:
    id: str
    tenant_id: str
    company_name: str
    status: AuditStatus = AuditStatus.PENDING
    findings: List[Finding] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def add_finding(self, finding: Finding) -> None:
        self.findings.append(finding)
        
    def total_financial_impact(self) -> float:
        return sum(f.financial_impact for f in self.findings)
