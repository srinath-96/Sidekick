"""
Configuration settings for the LeetCode AI Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # API Configuration
    GOOGLE_API_KEY = None
    
    # Directory settings
    SCREENSHOT_DIR = "crew_temp_screenshots"
    LOG_FILE = "leetcode_solutions.md"
    
    # Hotkey settings
    HOTKEY_COMBINATION = '<ctrl>+<shift>+a'
    HOTKEY_COMBINATION_MAC = '<cmd>+<shift>+a'
    
    # Model settings
    GEMINI_MODEL = "gemini/gemini-2.0-flash"
    GEMINI_VISION_MODEL = "gemini-2.0-flash"
    TEMPERATURE = 0.1
    
    # Crew settings
    VERBOSE = False
    
    @classmethod
    def initialize(cls):
        """Initialize configuration and validate environment variables"""
        # Check for API key
        cls.GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
        if not cls.GOOGLE_API_KEY:
            cls.GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
            if cls.GOOGLE_API_KEY:
                os.environ["GOOGLE_API_KEY"] = cls.GOOGLE_API_KEY
                print("Found GEMINI_API_KEY, using it for GOOGLE_API_KEY.")
            else:
                print("CRITICAL ERROR: Neither GOOGLE_API_KEY nor GEMINI_API_KEY environment variable is set.")
                exit(1)
        
        # Create screenshot directory if it doesn't exist
        if not os.path.exists(cls.SCREENSHOT_DIR):
            os.makedirs(cls.SCREENSHOT_DIR)
        
        return cls.GOOGLE_API_KEY

# Initialize configuration when module is imported
Config.initialize() 