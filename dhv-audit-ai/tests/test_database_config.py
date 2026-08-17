import os
import pytest
from src.infrastructure.database import get_db

def test_database_ssl_connection_arguments(monkeypatch):
    # Mock environment variables to force SSL mode requirement
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
    monkeypatch.setenv("DB_REQUIRE_SSL", "true")
    
    # Reload modules or test directly the database script flow
    import importlib
    import src.infrastructure.database
    importlib.reload(src.infrastructure.database)
    
    # Assert connect_args has sslmode required
    assert src.infrastructure.database.connect_args == {"sslmode": "require"}
    
    # Reset back to default
    monkeypatch.delenv("DB_REQUIRE_SSL")
    importlib.reload(src.infrastructure.database)

def test_get_db_generator_yield():
    db_gen = get_db()
    # It should return a session on next()
    session = next(db_gen)
    assert session is not None
    
    # Close it by raising StopIteration
    try:
        next(db_gen)
    except StopIteration:
        pass
