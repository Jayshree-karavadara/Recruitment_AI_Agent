from abc import ABC, abstractmethod
from typing import Dict

class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def evaluate_resume(self, jd_text: str, resume_text: str) -> dict:
        """Evaluates a resume against a job description."""
        pass

    @abstractmethod
    def generate_jd(self, details: Dict) -> str:
        """Generates a job description from a dictionary of details."""
        pass

    @abstractmethod
    def generate_interview_email(self, candidate_name: str, role: str) -> str:
        """Generates an interview email."""
        pass

    @abstractmethod
    def generate_rejection_email(self, candidate_name: str, role: str) -> str:
        """Generates a rejection email."""
        pass