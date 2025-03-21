from pydantic import BaseModel
from typing import List

class TextRequest(BaseModel):
    text: str

class TextAnalysisResponse(BaseModel):
    classification: str
    entities: List[str]
    summary: str 