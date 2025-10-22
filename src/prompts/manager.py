import yaml
from pathlib import Path
from typing import Dict, Any, Union

from src.utils.logger import get_logger

logger = get_logger(__name__)

class PromptManager:
    """Manages loading, parsing, and formatting of prompts from a YAML file."""

    def __init__(self, prompts_file: Path):
        """
        Initializes the PromptManager with the path to the prompts file.
        
        Args:
            prompts_file: Path to the YAML file containing prompt templates
        """
        self.prompts_file = prompts_file
        self.prompts = self._load_prompts()

    def _load_prompts(self) -> Dict[str, Any]:
        """
        Loads prompts from the YAML file.
        
        Returns:
            Dictionary of prompt templates
            
        Raises:
            FileNotFoundError: If the prompts file doesn't exist
            ValueError: If there's an error parsing the YAML
        """
        try:
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                prompts = yaml.safe_load(f) or {}
                logger.info(f"Successfully loaded {len(prompts)} prompts from {self.prompts_file}")
                return prompts
        except FileNotFoundError as e:
            logger.error(f"Prompts file not found at: {self.prompts_file}")
            raise FileNotFoundError(f"Prompts file not found: {self.prompts_file}") from e
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML in prompts file: {e}")
            raise ValueError(f"Invalid YAML in prompts file: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error loading prompts: {e}")
            raise

    def get_prompt(self, prompt_name: str, **kwargs) -> Union[str, Dict[str, Any]]:
        """
        Gets a specific prompt by name and formats it with the given kwargs.
        
        Args:
            prompt_name: Name of the prompt template to retrieve
            **kwargs: Variables to format into the prompt
            
        Returns:
            Formatted prompt as a string or dictionary
            
        Raises:
            ValueError: If no prompts are loaded or required variables are missing
            KeyError: If the requested prompt doesn't exist
        """
        if not self.prompts:
            raise ValueError("No prompts loaded. Check the prompts file path and format.")
        
        if prompt_name not in self.prompts:
            available = ", ".join(self.prompts.keys())
            raise KeyError(f"Prompt '{prompt_name}' not found. Available prompts: {available}")
        
        prompt = self.prompts[prompt_name]
        
        # Handle both string and dictionary prompts
        if isinstance(prompt, str):
            try:
                return prompt.format(**kwargs)
            except KeyError as e:
                raise ValueError(f"Missing required variable in prompt '{prompt_name}': {e}") from e
        elif isinstance(prompt, dict):
            # For system/user prompt format
            formatted = {}
            for key, value in prompt.items():
                if isinstance(value, str):
                    try:
                        formatted[key] = value.format(**kwargs)
                    except KeyError as e:
                        raise ValueError(f"Missing required variable in prompt '{prompt_name}.{key}': {e}") from e
                else:
                    formatted[key] = value
            return formatted
        else:
            raise ValueError(f"Invalid prompt format for '{prompt_name}'. Expected string or dict, got {type(prompt)}")
    
    # Alias for backward compatibility
    format_prompt = get_prompt
