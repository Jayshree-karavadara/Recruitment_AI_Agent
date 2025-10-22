import json
import groq
from typing import Dict
from src.llm.base import LLMClient
from src.prompts.manager import PromptManager
from src.utils.logger import get_logger

logger = get_logger(__name__)

class GroqClient(LLMClient):
    """LLM client for Groq API."""

    def __init__(self, api_key: str, model: str, prompt_manager: PromptManager):
        """Initializes the GroqClient."""
        self.api_key = api_key
        self.model = model
        self.prompt_manager = prompt_manager
        self.client = groq.Groq(api_key=self.api_key)

    def _create_chat_completion(self, system_prompt: str, user_prompt: str, is_json: bool = False) -> str:
        """Helper to create a chat completion."""
        try:
            response_format = {"type": "json_object"} if is_json else {"type": "text"}
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                response_format=response_format,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return json.dumps({"error": "Failed to get response from Groq."}) if is_json else "Error: Could not get response."

    def evaluate_resume(self, jd_text: str, resume_text: str) -> dict:
        """Evaluates a resume against a job description using the Groq API."""
        prompt = self.prompt_manager.format_prompt(
            "resume_evaluation", jd_text=jd_text, resume_text=resume_text
        )
        if not prompt:
            return {"error": "Could not load prompt."}
        
        response_str = self._create_chat_completion(prompt["system_prompt"], prompt["user_prompt"], is_json=True)
        return json.loads(response_str)

    def generate_jd(self, details: Dict) -> str:
        """Generates a job description using the Groq API."""
        prompt = self.prompt_manager.format_prompt("jd_generation", **details)
        if not prompt:
            return "Error: Could not load prompt."
        return self._create_chat_completion(prompt["system_prompt"], prompt["user_prompt"])

    def generate_interview_email(self, candidate_name: str, role: str) -> str:
        """Generates an interview email using the Groq API."""
        prompt = self.prompt_manager.format_prompt(
            "interview_email", candidate_name=candidate_name, role=role
        )
        if not prompt:
            return "Error: Could not load prompt."
        return self._create_chat_completion(prompt["system_prompt"], prompt["user_prompt"])

    def generate_rejection_email(self, candidate_name: str, role: str) -> str:
        """Generates a rejection email using the Groq API."""
        prompt = self.prompt_manager.format_prompt(
            "rejection_email", candidate_name=candidate_name, role=role
        )
        if not prompt:
            return "Error: Could not load prompt."
        return self._create_chat_completion(prompt["system_prompt"], prompt["user_prompt"])
