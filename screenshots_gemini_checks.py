import google.generativeai as genai
import os
from PIL import Image
import time
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# The script will try to read this from your environment variables.
# For testing ONLY, if you haven't set the environment variable,
# you could temporarily uncomment and set it here (NOT recommended for production):
# os.environ['GOOGLE_API_KEY'] = "YOUR_ACTUAL_GOOGLE_API_KEY"

SCREENSHOT_FOLDER = "periodic_screenshots"  # Folder containing your screenshots
GEMINI_MODEL_NAME = "gemini-2.0-flash"  # Good balance of speed and capability.
                                            # Or use "gemini-1.5-pro-latest" for highest quality.
PROMPT_FOR_GEMINI = (
    "Analyze this screenshot carefully. Describe the main application or window in focus. "
    "What are the key visual elements or text present? "
    "Are there any notable alerts, dialog boxes, or calls to action? "
    "Provide a concise summary of what is happening on the screen."
)
# Supported image extensions (Pillow can open many, but these are common for screenshots)
SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp')

def process_screenshots_with_gemini():
    """
    Iterates through screenshots in a folder, sends them to Gemini for analysis,
    and prints the responses.
    """
    print("--- Gemini Screenshot Analyzer ---")
    print(f"Attempting to process images from folder: '{SCREENSHOT_FOLDER}'")
    print(f"Using Gemini model: {GEMINI_MODEL_NAME}")

    # 1. Configure API Key
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("\nError: The GOOGLE_API_KEY environment variable is not set.")
            print("Please set it before running the script. You can get a key from https://aistudio.google.com/app/apikey")
            return
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"Error configuring the Google Generative AI SDK: {e}")
        return

    # 2. Initialize the Gemini Model
    # You can customize generation_config for things like temperature, top_p, etc.
    # You can also set safety_settings to adjust content filtering.
    model = genai.GenerativeModel(
        GEMINI_MODEL_NAME,
        generation_config={"temperature": 0.3} # Lower temperature for more factual/less creative descriptions
    )

    # 3. Check if the screenshot folder exists
    if not os.path.isdir(SCREENSHOT_FOLDER):
        print(f"\nError: The screenshot folder '{SCREENSHOT_FOLDER}' was not found in the current directory.")
        print("Please make sure it exists and contains your screenshot images.")
        return

    # 4. Get list of image files, sorted by name (often chronological if timestamped)
    try:
        image_files = sorted([
            f for f in os.listdir(SCREENSHOT_FOLDER)
            if f.lower().endswith(SUPPORTED_EXTENSIONS)
        ])
    except FileNotFoundError: # Should be caught by os.path.isdir, but as a safeguard
        print(f"\nError: Screenshot folder '{SCREENSHOT_FOLDER}' not found when listing files.")
        return


    if not image_files:
        print(f"\nNo supported image files ({', '.join(SUPPORTED_EXTENSIONS)}) found in '{SCREENSHOT_FOLDER}'.")
        return

    print(f"\nFound {len(image_files)} image(s) to process.\n")

    # 5. Loop through each image, send to Gemini, and print response
    for image_filename in image_files:
        image_path = os.path.join(SCREENSHOT_FOLDER, image_filename)
        print(f"--- Processing: {image_filename} ---")

        try:
            # Load the image using Pillow
            img = Image.open(image_path)

            # Send the image and prompt to Gemini.
            # The SDK can handle PIL Image objects directly.
            print("Sending to Gemini for analysis...")
            response = model.generate_content([PROMPT_FOR_GEMINI, img])

            # Print the response text
            if response.parts:
                print("\nGemini's Response:")
                print(response.text) # .text combines text from all parts
            else:
                # This might happen if the response was blocked due to safety settings
                # or if there was no text content generated.
                print("\nGemini's response was empty or potentially blocked.")
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                    print(f"Prompt Feedback (e.g., block reason): {response.prompt_feedback}")
                if hasattr(response, 'candidates') and response.candidates:
                     for candidate in response.candidates:
                        if candidate.finish_reason != 'STOP':
                             print(f"Candidate Finish Reason: {candidate.finish_reason}")
                             if hasattr(candidate, 'safety_ratings'):
                                 print(f"Candidate Safety Ratings: {candidate.safety_ratings}")


        except FileNotFoundError:
            print(f"Error: Image file not found at '{image_path}'. Skipping.")
        except Exception as e:
            # This will catch errors during the API call or other unexpected issues
            print(f"An error occurred while processing {image_filename}:")
            print(e)
            if "API key not valid" in str(e): # Specific check for common API key issue
                print("Please ensure your GOOGLE_API_KEY is correct and valid.")
                break # Stop processing if API key is bad


        print("-" * 50 + "\n")
        time.sleep(2)  # Add a small delay between API calls to be respectful of rate limits,
                       # especially if you have many images or are on a free tier.

    print("--- All screenshots have been processed. ---")

if __name__ == "__main__":
    process_screenshots_with_gemini()