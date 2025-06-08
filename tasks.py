"""
CrewAI tasks for the LeetCode AI Assistant
"""
from crewai import Task

def create_capture_task(screen_scanner_agent):
    """Create the screenshot capture task"""
    return Task(
        description=(
            "Take a screenshot of the current screen using the Screen Capture Tool. "
            "Your final answer must be only the absolute file path of the captured image."
        ),
        expected_output="The absolute file path to the screenshot image.",
        agent=screen_scanner_agent,
    )

def create_analyze_task(image_analysis_agent, capture_task):
    """Create the image analysis task"""
    return Task(
        description=(
            "You will receive a file path from the capture task. "
            "Use the Gemini Image Analysis Tool to analyze the LeetCode problem screenshot at that file path. "
            "Provide comprehensive problem-solving assistance including problem identification, "
            "solution strategy, complete working code, and learning insights. "
            "After the analysis, conclude your response with: "
            "'Analyzed image file: [the exact file path]'."
        ),
        expected_output=(
            "A comprehensive LeetCode problem analysis including problem identification, "
            "current progress assessment, solution strategy, complete working code with explanations, "
            "complexity analysis, and next steps, followed by 'Analyzed image file: /path/to/screenshot.png'."
        ),
        agent=image_analysis_agent,
        context=[capture_task]
    ) 