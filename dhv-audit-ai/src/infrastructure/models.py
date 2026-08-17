import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Date, Numeric, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
from src.infrastructure.database import Base

class TenantModel(Base):
    """
    Representa o Grupo Econ?mico/Holding atendido pelo modelo Boutique.
    """
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    subdomain = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default="active") # active, suspended, canceled
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    users = relationship("UserModel", back_populates="tenant", cascade="all, delete-orphan")
    companies = relationship("CompanyModel", back_populates="tenant", cascade="all, delete-orphan")

class UserModel(Base):
    """
    Controle de Usu?rios com RBAC (SuperAdmin, Consultant, TenantAdmin, etc.).
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    role = Column(String(50), default="viewer", nullable=False) # super_admin, consultant, tenant_admin, viewer
    status = Column(String(50), default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tenant = relationship("TenantModel", back_populates="users")

class CompanyModel(Base):
    """
    Representa os CNPJs constituintes do Grupo Econ?mico.
    """
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    company_name = Column(String(255), nullable=False)
    trade_name = Column(String(255))
    state_registration = Column(String(20))
    city_registration = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    tenant = relationship("TenantModel", back_populates="companies")
    audit_cycles = relationship("AuditCycleModel", back_populates="company")

class AuditCycleModel(Base):
    """
    Mapeia os ciclos de auditoria peri?dicos das holdings.
    """
    __tablename__ = "audit_cycles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="RESTRICT"), nullable=False)
    title = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String(50), default="pending", nullable=False) # pending, processing, analyzed, validated, completed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    company = relationship("CompanyModel", back_populates="audit_cycles")
    documents = relationship("DocumentModel", back_populates="audit_cycle", cascade="all, delete-orphan")
    findings = relationship("FindingModel", back_populates="audit_cycle", cascade="all, delete-orphan")

class DocumentModel(Base):
    """
    Documentos ingeridos e vinculados ao storage AWS S3.
    """
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    audit_cycle_id = Column(UUID(as_uuid=True), ForeignKey("audit_cycles.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_hash = Column(String(64), nullable=False) # SHA-256
    document_type = Column(String(50), nullable=False) # cte, nfe, nfse, ofx, e_social, manual
    status = Column(String(50), default="queued", nullable=False) # queued, parsing, processed, failed
    ocr_confidence_score = Column(Numeric(5, 2))
    raw_extracted_json = Column(JSON().with_variant(JSONB, "postgresql"))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    audit_cycle = relationship("AuditCycleModel", back_populates="documents")

class FindingModel(Base):
    """
    Achados de auditoria gerados por IA / regras com materialidade zero.
    """
    __tablename__ = "findings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False)
    audit_cycle_id = Column(UUID(as_uuid=True), ForeignKey("audit_cycles.id", ondelete="CASCADE"), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    severity = Column(String(50), nullable=False) # low, medium, high, critical
    financial_impact = Column(Numeric(15, 2), default=0.00, nullable=False)
    confidence_score = Column(Numeric(5, 2), nullable=False)
    is_validated = Column(Boolean, default=False, nullable=False)
    validated_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    validated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    audit_cycle = relationship("AuditCycleModel", back_populates="findings")
