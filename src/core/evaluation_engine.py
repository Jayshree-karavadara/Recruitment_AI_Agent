from typing import List, Dict, Any
from fastapi import UploadFile
from src.core.document_processor import DocumentProcessor
from src.llm.base import LLMClient
from src.prompts.manager import PromptManager
from io import BytesIO

class EvaluationEngine:
    """Orchestrates the evaluation of candidates."""

    def __init__(
        self,
        llm_client: LLMClient,
        document_processor: DocumentProcessor,
        prompt_manager: PromptManager,
    ):
        """Initializes the EvaluationEngine."""
        self.llm_client = llm_client
        self.document_processor = document_processor
        self.prompt_manager = prompt_manager

    def _get_jd_text(
        self,
        jd_file: UploadFile,
        jd_text: str,
        jd_generation_details: Dict[str, Any],
    ) -> str:
        """Determines the source of the job description and returns its text."""
        if jd_file and jd_file.filename:
            return self.document_processor.process(jd_file)
        if jd_text:
            return jd_text
        if jd_generation_details and jd_generation_details.get("job_title"):
            return self.llm_client.generate_jd(jd_generation_details)
        raise ValueError("No valid job description source provided.")

    async def evaluate_candidates(
        self,
        resume_files: List[UploadFile],
        jd_file: UploadFile = None,
        jd_text: str = None,
        jd_generation_details: Dict[str, Any] = None,
    ) -> List[dict]:
        """Evaluates a list of resumes against a job description."""
        try:
            jd_text_content = self._get_jd_text(
                jd_file, jd_text, jd_generation_details
            )
        except ValueError as e:
            return [{"error": str(e)}]

        results = []
        for resume_file in resume_files:
            try:
                resume_text = self.document_processor.process(resume_file)
                
                evaluation = self.llm_client.evaluate_resume(jd_text_content, resume_text)
                evaluation["filename"] = resume_file.filename
                results.append(evaluation)
            except Exception as e:
                results.append({"filename": resume_file.filename, "error": str(e)})

        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        return results
