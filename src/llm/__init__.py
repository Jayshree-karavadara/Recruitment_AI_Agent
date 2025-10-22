import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from src.llm.base import LLMClient
from src.llm.openai_client import OpenAIClient
from src.llm.groq_client import GroqClient
from src.prompts.manager import PromptManager

load_dotenv()

# Build a robust path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def get_llm_client() -> LLMClient:
    """Factory function to get the configured LLM client."""
    config_path = BASE_DIR / "config/settings.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    provider = config["ai"]["default_provider"]
    model = config["ai"]["models"][provider]

    prompts_path = BASE_DIR / "config/prompts.yaml"
    prompt_manager = PromptManager(prompts_path)

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        return OpenAIClient(api_key=api_key, model=model, prompt_manager=prompt_manager)
    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")

        print(f"Using Groq API key: {api_key}")
        
        return GroqClient(api_key=api_key, model=model, prompt_manager=prompt_manager)
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")
