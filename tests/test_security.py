import pytest
from fastapi import HTTPException
from app.core.security import get_api_key
from app.core.rate_limiter import rate_limiter
from app.core.config import settings

@pytest.mark.asyncio
async def test_get_api_key_success():
    api_key = settings.API_KEY
    result = await get_api_key(api_key)
    assert result == api_key

@pytest.mark.asyncio
async def test_get_api_key_missing():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key(None)
    assert exc_info.value.status_code == 401
    assert "API key is missing" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_get_api_key_empty():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key("")
    assert exc_info.value.status_code == 401
    assert "API key is missing" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_get_api_key_invalid():
    with pytest.raises(HTTPException) as exc_info:
        await get_api_key("invalid_key")
    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value.detail)

def test_rate_limiter():
    api_key = "test_key"
    
    # Deve permitir requisições até o limite
    for _ in range(settings.RATE_LIMIT_PER_MINUTE):
        rate_limiter.check_rate_limit(api_key)
    
    # A próxima requisição deve falhar
    with pytest.raises(HTTPException) as exc_info:
        rate_limiter.check_rate_limit(api_key)
    assert exc_info.value.status_code == 429
    assert "Rate limit exceeded" in str(exc_info.value.detail)

def test_rate_limiter_different_keys():
    api_key1 = "test_key1"
    api_key2 = "test_key2"
    
    # Deve permitir requisições até o limite para cada chave separadamente
    for _ in range(settings.RATE_LIMIT_PER_MINUTE):
        rate_limiter.check_rate_limit(api_key1)
        rate_limiter.check_rate_limit(api_key2)
    
    # A próxima requisição deve falhar para ambas as chaves
    with pytest.raises(HTTPException):
        rate_limiter.check_rate_limit(api_key1)
    with pytest.raises(HTTPException):
        rate_limiter.check_rate_limit(api_key2) 