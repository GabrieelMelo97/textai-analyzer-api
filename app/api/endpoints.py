import time
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.text_analysis import TextRequest, TextAnalysisResponse
from app.services.text_analysis_service import TextAnalysisService
from app.core.config import settings
from app.core.security import get_api_key
from app.core.rate_limiter import rate_limiter
from app.core.logging import api_logger

router = APIRouter()
text_analysis_service = TextAnalysisService(settings.DEEPSEEK_API_KEY)

# Cache simples em memória
response_cache = {}

@router.post("/analyze", response_model=TextAnalysisResponse)
async def analyze_text(
    request: TextRequest,
    api_key: str = Depends(get_api_key)
):
    try:
        # Validação do tamanho do texto
        if len(request.text) < settings.MIN_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text must be at least {settings.MIN_TEXT_LENGTH} characters long"
            )
        if len(request.text) > settings.MAX_TEXT_LENGTH:
            raise HTTPException(
                status_code=400,
                detail=f"Text must not exceed {settings.MAX_TEXT_LENGTH} characters"
            )

        # Rate limiting
        rate_limiter.check_rate_limit(api_key)

        # Verificar cache
        cache_key = f"{api_key}:{request.text}"
        if cache_key in response_cache:
            return response_cache[cache_key]

        # Processar requisição e medir tempo
        start_time = time.time()
        result = text_analysis_service.analyze_text(request.text)
        processing_time = time.time() - start_time

        # Criar resposta
        response = TextAnalysisResponse(
            classification=result["classification"],
            entities=result["entities"],
            summary=result["summary"]
        )

        # Armazenar no cache
        response_cache[cache_key] = response
        
        # Limpar cache se necessário
        if len(response_cache) > settings.MAX_CACHE_ITEMS:
            response_cache.clear()

        # Logging
        api_logger.log_request(
            api_key=api_key,
            request_data=request.dict(),
            processing_time=processing_time,
            response=result
        )

        return response

    except Exception as e:
        api_logger.log_error(api_key, e)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e)) 