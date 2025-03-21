import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

class APILogger:
    def __init__(self):
        self.logger = logging.getLogger("api_logger")
        self.logger.setLevel(logging.INFO)
        
        # Criar diretório de logs se não existir
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Handler para arquivo
        file_handler = logging.FileHandler(
            f"logs/api_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.INFO)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_request(
        self,
        api_key: str,
        request_data: Dict[str, Any],
        processing_time: float,
        response: Dict[str, Any]
    ) -> None:
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "api_key": api_key[-8:],  # Últimos 8 caracteres da chave
            "request_length": len(request_data.get("text", "")),
            "processing_time_ms": round(processing_time * 1000, 2),
            "response_type": {
                "classification": response.get("classification"),
                "entities_count": len(response.get("entities", [])),
                "summary_length": len(response.get("summary", ""))
            }
        }
        self.logger.info(f"API Request: {json.dumps(log_data)}")

    def log_error(self, api_key: str, error: Exception) -> None:
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "api_key": api_key[-8:],
            "error_type": type(error).__name__,
            "error_message": str(error)
        }
        self.logger.error(f"API Error: {json.dumps(log_data)}")

api_logger = APILogger() 