from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}

    def check_rate_limit(self, api_key: str) -> None:
        current_time = datetime.now()
        if api_key not in self.requests:
            self.requests[api_key] = []

        # Remove requests older than 1 minute
        self.requests[api_key] = [
            req_time for req_time in self.requests[api_key]
            if current_time - req_time < timedelta(minutes=1)
        ]

        if len(self.requests[api_key]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again in a minute."
            )

        self.requests[api_key].append(current_time)

rate_limiter = RateLimiter() 