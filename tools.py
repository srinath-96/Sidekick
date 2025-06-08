"""
Custom tools for screenshot capture and image analysis
"""
import os
import datetime
from PIL import Image
import mss
import google.generativeai as genai
from crewai.tools import BaseTool

from .config import Config
from .prompts import get_leetcode_analysis_prompt

# Configure Gemini
genai.configure(api_key=Config.GOOGLE_API_KEY)

class ScreenshotTool(BaseTool):
    """Tool for capturing screenshots of the current screen"""
    
    name: str = "Screen Capture Tool"
    description: str = (
        "Captures the current content of the primary screen, saves it as a PNG image file. "
        "Returns the absolute file path to the captured image."
    )

    def _run(self) -> str:
        print("[ScreenshotTool] _run called")
        try:
            with mss.mss() as sct:
                if len(sct.monitors) > 1:
                    monitor_definition = sct.monitors[1]
                elif sct.monitors:
                    monitor_definition = sct.monitors[0]
                else:
                    print("[ScreenshotTool] Error: No monitors found by mss.")
                    return "Error: No monitors found by mss."

                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                filename = f"cs_{timestamp}.png"
                full_path = os.path.abspath(os.path.join(Config.SCREENSHOT_DIR, filename))

                sct_img = sct.grab(monitor_definition)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=full_path)
                print(f"[ScreenshotTool] Screenshot saved to: {full_path}")
                if os.path.exists(full_path):
                    print(f"[ScreenshotTool] File exists after save: {full_path}")
                else:
                    print(f"[ScreenshotTool] File does NOT exist after save: {full_path}")
                return full_path
        except Exception as e:
            print(f"[ScreenshotTool] Error: {e}")
            return f"Error capturing screen: {str(e)}"

class GeminiImageAnalysisTool(BaseTool):
    """Tool for analyzing images using Google Gemini's vision capabilities"""
    
    name: str = "Gemini Image Analysis Tool"
    description: str = (
        "Analyzes an image using Google Gemini's vision capabilities. "
        "Input must be a string containing the absolute file path to the image."
    )

    def _run(self, file_path: str) -> str:
        try:
            print(f"[GeminiImageAnalysisTool] Analyzing screenshot: {file_path}")
            if not isinstance(file_path, str) or not file_path.strip():
                return "Error: File path must be a non-empty string."
            if not os.path.exists(file_path):
                return f"Error: Image file not found at path: {file_path}"
            
            # Load and prepare the image
            img = Image.open(file_path)
            img = img.convert("RGB")
            
            # Initialize Gemini model
            model = genai.GenerativeModel(Config.GEMINI_VISION_MODEL)
            
            # Get the LeetCode analysis prompt from file
            leetcode_prompt = get_leetcode_analysis_prompt()
            
            # Generate response using the LeetCode prompt
            response = model.generate_content([leetcode_prompt, img])
            
            print(f"[GeminiImageAnalysisTool] Successfully analyzed LeetCode problem: {file_path}")
            return response.text
            
        except Exception as e:
            print(f"[GeminiImageAnalysisTool] Error analyzing image {file_path}: {e}")
            return f"Error analyzing image: {str(e)}" 