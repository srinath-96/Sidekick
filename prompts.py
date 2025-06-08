"""
LeetCode Analysis Prompts for AI Assistant
This module loads prompts from external text files for easier editing and maintenance.
"""
import os
from pathlib import Path

class PromptLoader:
    """Loads prompts from external text files"""
    
    def __init__(self):
        # Get the directory where this file is located
        self.prompts_dir = Path(__file__).parent / "prompts"
        self._ensure_prompts_directory()
        self._cache = {}
    
    def _ensure_prompts_directory(self):
        """Create prompts directory if it doesn't exist"""
        self.prompts_dir.mkdir(exist_ok=True)
    
    def load_prompt(self, prompt_name: str) -> str:
        """
        Load a prompt from a text file
        
        Args:
            prompt_name: Name of the prompt file (without .txt extension)
            
        Returns:
            The prompt text as a string
        """
        # Check cache first
        if prompt_name in self._cache:
            return self._cache[prompt_name]
        
        prompt_file = self.prompts_dir / f"{prompt_name}.txt"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                prompt_text = f.read().strip()
            
            # Cache the prompt
            self._cache[prompt_name] = prompt_text
            return prompt_text
            
        except Exception as e:
            raise RuntimeError(f"Error reading prompt file {prompt_file}: {e}")
    
    def get_available_prompts(self) -> list:
        """Get list of available prompt files"""
        if not self.prompts_dir.exists():
            return []
        
        return [f.stem for f in self.prompts_dir.glob("*.txt")]
    
    def reload_prompt(self, prompt_name: str) -> str:
        """Force reload a prompt from file (clears cache)"""
        if prompt_name in self._cache:
            del self._cache[prompt_name]
        return self.load_prompt(prompt_name)

# Global prompt loader instance
_prompt_loader = PromptLoader()

# Convenience functions for backward compatibility
def get_leetcode_analysis_prompt() -> str:
    """Get the LeetCode analysis prompt"""
    return _prompt_loader.load_prompt("leetcode_analysis")

def get_general_coding_prompt() -> str:
    """Get the general coding prompt"""
    return _prompt_loader.load_prompt("general_coding")

def get_debug_analysis_prompt() -> str:
    """Get the debug analysis prompt"""
    return _prompt_loader.load_prompt("debug_analysis")

# For backward compatibility - these will be loaded dynamically
@property
def LEETCODE_ANALYSIS_PROMPT():
    return get_leetcode_analysis_prompt()

@property
def GENERAL_CODING_PROMPT():
    return get_general_coding_prompt()

@property
def DEBUG_ANALYSIS_PROMPT():
    return get_debug_analysis_prompt()

# Make the prompt loader available for advanced usage
prompt_loader = _prompt_loader 