from datetime import datetime, date
import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database import Base
from src.infrastructure.models import (
    TenantModel,
    UserModel,
    CompanyModel,
    AuditCycleModel,
    DocumentModel,
    FindingModel
)

# Configura banco de dados em mem?ria SQLite dedicado para testes r?pidos
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_session():
    # Cria as tabelas do modelo f?sico
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_database_models_relational_integrity(db_session):
    # 1. Create Tenant
    tenant = TenantModel(
        id=uuid.uuid4(),
        name="Holding Alfa S/A",
        subdomain="alfa"
    )
    db_session.add(tenant)
    db_session.commit()
    
    assert tenant.status == "active"
    
    # 2. Create User linked to Tenant (RBAC)
    user = UserModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        email="consultant@dhvlog.com.br",
        password_hash="scrypted_hash_pass",
        name="Pedro Cabral",
        role="consultant"
    )
    db_session.add(user)
    
    # 3. Create Company under Tenant
    company = CompanyModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        cnpj="12345678000199",
        company_name="Alfa Transportes Rodovi?rios"
    )
    db_session.add(company)
    db_session.commit()
    
    # 4. Create Audit Cycle
    cycle = AuditCycleModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        company_id=company.id,
        title="Auditoria de Fretes Q2/2026",
        start_date=date(2026, 4, 1),
        end_date=date(2026, 6, 30)
    )
    db_session.add(cycle)
    db_session.commit()
    
    # 5. Create Document under Audit Cycle
    document = DocumentModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        audit_cycle_id=cycle.id,
        filename="cte-102.xml",
        file_path="s3://dhv-audit-storage/alfa/cte-102.xml",
        file_hash="a5f...62b",
        document_type="cte",
        ocr_confidence_score=98.50
    )
    db_session.add(document)
    db_session.commit()
    
    # 6. Create Finding validating materialidade zero (R$ 2.50)
    finding = FindingModel(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        audit_cycle_id=cycle.id,
        document_id=document.id,
        title="Arredondamento Fiscal Indevido",
        description="Fatura de transporte apresentou desvio de R$ 2.50 nas d?zimas de imposto.",
        severity="low",
        financial_impact=2.50,
        confidence_score=99.00
    )
    db_session.add(finding)
    db_session.commit()
    
    # Query validation
    db_finding = db_session.query(FindingModel).filter_by(id=finding.id).first()
    assert db_finding is not None
    assert float(db_finding.financial_impact) == 2.50
    assert db_finding.audit_cycle_id == cycle.id
    assert db_finding.document_id == document.id
