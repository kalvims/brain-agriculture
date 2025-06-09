import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from main import app

# SQLite database URL for testing
SQLITE_DATABASE_URL = "sqlite:///./test_db.db"

# Create a SQLAlchemy engine
engine = create_engine(
    SQLITE_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a new database session with a rollback at the end of the test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


# Fixture to generate a user payload
@pytest.fixture()
def user_payload():
    """Generate a user payload."""
    return {
        "name": "John McDonald",
        "cpf_cnpj": "123.456.789-09",
        "birthdate": "1950-05-02",
    }


@pytest.fixture()
def user_payload_invalid_cpf():
    """Generate a user payload."""
    return {
        "name": "John McDonald",
        "cpf_cnpj": "123.456.789-89",
        "birthdate": "1950-05-02",
    }


@pytest.fixture()
def user_payload_updated():
    """Generate an updated user payload."""
    return {
        "name": "John McDonald da Silva",
        "cpf_cnpj": "123.456.789-09",
        "birthdate": "1980-05-22",
    }


@pytest.fixture()
def user_payload_updated_invalid_cpf():
    """Generate an updated user payload."""
    return {
        "name": "John McDonald da Silva",
        "cpf_cnpj": "123.456.789-19",
        "birthdate": "1980-05-22",
    }


@pytest.fixture()
def farm_payload():
    """Generate a farm payload."""
    return {
        "name": "Fazenda Tiao",
        "city": "São Paulo",
        "state": "SP",
        "total_area": 100.0,
        "arable_area": 50.0,
        "vegetation_area": 30.0,
    }


@pytest.fixture()
def farm_payload_invalid_area():
    """Generate a farm payload with invalid area."""
    return {
        "name": "Fazenda Jatobá",
        "city": "Umuarama",
        "state": "PR",
        "total_area": 50.0,
        "arable_area": 40.0,
        "vegetation_area": 30.0,
    }


@pytest.fixture()
def farm_payload_updated():
    """Generate an updated farm payload."""
    return {
        "name": "Fazenda Tiao Atualizada",
        "city": "São Paulo",
        "state": "SP",
        "total_area": 120.0,
        "arable_area": 60.0,
        "vegetation_area": 40.0,
    }


@pytest.fixture()
def plantation_data():
    return {"name": "Plantation Teste", "description": "Descrição Teste"}


@pytest.fixture()
def updated_plantation_data():
    return {"name": "Plantation Atualizada",
            "description": "Descrição Atualizada"}


@pytest.fixture()
def season_data():
    return {"year": 2023, "description": "Safra de Verão 2023"}


@pytest.fixture()
def updated_season_data():
    return {"year": 2024, "description": "Safra de Verão 2024"}


@pytest.fixture()
def farm_plantation_season_data():
    return {"plantation_id": 1, "season_id": 1}
