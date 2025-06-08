"""
CrewAI agents for the LeetCode AI Assistant
"""
from crewai import Agent, LLM
from .tools import ScreenshotTool, GeminiImageAnalysisTool
from .config import Config

# Configure LLM for non-vision tasks
gemini_llm = LLM(
    model=Config.GEMINI_MODEL,
    temperature=Config.TEMPERATURE
)

def create_screen_scanner_agent():
    """Create the screen scanning agent"""
    return Agent(
        role="Screen Scanning Technician",
        goal="Capture a high-quality screenshot of the user's primary screen.",
        backstory=(
            "You are a diligent assistant responsible for capturing the screen accurately. "
            "You use a specialized tool to take a snapshot and provide its file location."
        ),
        tools=[ScreenshotTool()],
        verbose=Config.VERBOSE,
        allow_delegation=False,
        llm=gemini_llm
    )

def create_image_analysis_agent():
    """Create the image analysis agent"""
    return Agent(
        role="LeetCode Problem Analysis Specialist",
        goal="Analyze LeetCode problem screenshots using advanced vision capabilities to provide comprehensive coding assistance.",
        backstory=(
            "You are an expert LeetCode interview coach with advanced vision capabilities. "
            "You specialize in analyzing coding problems, understanding user progress, and providing "
            "complete solutions with detailed explanations. You help users learn patterns and "
            "improve their problem-solving skills."
        ),
        tools=[GeminiImageAnalysisTool()],
        verbose=Config.VERBOSE,
        allow_delegation=False,
        llm=gemini_llm
    ) 