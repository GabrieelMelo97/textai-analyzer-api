import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, Mock
from app.core.config import settings
from app.main import app
from app.api.endpoints import text_analysis_service, response_cache

@pytest.fixture(autouse=True)
def clear_cache():
    response_cache.clear()
    yield
    response_cache.clear()

@pytest.mark.asyncio
async def test_analyze_text_endpoint_success(test_client, valid_api_key, sample_text):
    with patch('app.api.endpoints.get_api_key', new_callable=AsyncMock) as mock_get_api_key, \
         patch('app.api.endpoints.rate_limiter.check_rate_limit') as mock_rate_limiter, \
         patch.object(text_analysis_service, 'analyze_text') as mock_analyze_text:
        mock_get_api_key.return_value = valid_api_key
        mock_analyze_text.return_value = {
            "classification": "Notícias",
            "entities": ["Pessoa1", "Organização1", "Local1"],
            "summary": "Resumo do texto"
        }

        response = test_client.post(
            "/api/v1/analyze",
            headers={"X-API-Key": valid_api_key},
            json={"text": sample_text}
        )

        assert response.status_code == 200
        assert response.json() == {
            "classification": "Notícias",
            "entities": ["Pessoa1", "Organização1", "Local1"],
            "summary": "Resumo do texto"
        }

@pytest.mark.asyncio
async def test_analyze_text_missing_api_key(test_client, sample_text):
    response = test_client.post(
        "/api/v1/analyze",
        json={"text": sample_text}
    )
    
    assert response.status_code == 401
    assert "API key is missing" in response.json()["detail"]

@pytest.mark.asyncio
async def test_analyze_text_invalid_api_key(test_client, sample_text):
    response = test_client.post(
        "/api/v1/analyze",
        headers={"X-API-Key": "invalid_key"},
        json={"text": sample_text}
    )
    
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]

@pytest.mark.asyncio
async def test_analyze_text_too_short(test_client, valid_api_key):
    with patch('app.api.endpoints.get_api_key', new_callable=AsyncMock) as mock_get_api_key:
        mock_get_api_key.return_value = valid_api_key
        
        short_text = "a" * (settings.MIN_TEXT_LENGTH - 1)
        response = test_client.post(
            "/api/v1/analyze",
            headers={"X-API-Key": valid_api_key},
            json={"text": short_text}
        )
        
        assert response.status_code == 400
        assert f"Text must be at least {settings.MIN_TEXT_LENGTH} characters long" in response.json()["detail"]

@pytest.mark.asyncio
async def test_analyze_text_too_long(test_client, valid_api_key):
    with patch('app.api.endpoints.get_api_key', new_callable=AsyncMock) as mock_get_api_key:
        mock_get_api_key.return_value = valid_api_key
        
        long_text = "a" * (settings.MAX_TEXT_LENGTH + 1)
        response = test_client.post(
            "/api/v1/analyze",
            headers={"X-API-Key": valid_api_key},
            json={"text": long_text}
        )
        
        assert response.status_code == 400
        assert f"Text must not exceed {settings.MAX_TEXT_LENGTH} characters" in response.json()["detail"]

@pytest.mark.asyncio
async def test_analyze_text_rate_limit(test_client, valid_api_key, sample_text):
    with patch('app.api.endpoints.get_api_key', new_callable=AsyncMock) as mock_get_api_key:
        mock_get_api_key.return_value = valid_api_key
        
        # Fazer várias requisições para atingir o limite
        for _ in range(settings.RATE_LIMIT_PER_MINUTE + 1):
            response = test_client.post(
                "/api/v1/analyze",
                headers={"X-API-Key": valid_api_key},
                json={"text": sample_text}
            )
        
        # A última requisição deve falhar por limite de taxa
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["detail"] 