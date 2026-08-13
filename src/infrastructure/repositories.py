from typing import Optional, Dict
from src.domain.entities import AuditCycle
from src.application.use_cases import AuditRepositoryInterface

class InMemoryAuditRepository(AuditRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, AuditCycle] = {}

    def save(self, cycle: AuditCycle) -> None:
        self._storage[cycle.id] = cycle

    def find_by_id(self, cycle_id: str) -> Optional[AuditCycle]:
        return self._storage.get(cycle_id)
