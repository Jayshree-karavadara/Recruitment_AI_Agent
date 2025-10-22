from pydantic import BaseModel
from typing import List, Optional

class CandidateResult(BaseModel):
    """Pydantic model for a candidate evaluation result."""
    filename: str
    score: int
    missing_skills: List[str]
    remarks: str

class EvaluationResult(BaseModel):
    """Pydantic model for the overall evaluation result."""
    results: List[CandidateResult]
