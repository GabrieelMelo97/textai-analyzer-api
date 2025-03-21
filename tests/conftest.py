import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app
from app.services.text_analysis_service import TextAnalysisService
from app.core.config import settings

@pytest.fixture
def test_client():
    with patch('app.api.endpoints.text_analysis_service') as mock_service:
        mock_service.analyze_text.return_value = {
            "classification": "Notícias",
            "entities": ["Pessoa1", "Organização1", "Local1"],
            "summary": "Resumo do texto"
        }
        yield TestClient(app)

@pytest.fixture
def mock_text_analysis_service():
    mock_service = Mock(spec=TextAnalysisService)
    mock_service.analyze_text.return_value = {
        "classification": "Notícias",
        "entities": ["Pessoa1", "Organização1", "Local1"],
        "summary": "Resumo do texto"
    }
    return mock_service

@pytest.fixture
def valid_api_key():
    return settings.API_KEY

@pytest.fixture
def sample_text():
    return "Este é um texto de exemplo para teste que deve ter um tamanho adequado para passar na validação." 