import ollama
import glob, os


image_path = "/Users/srinathmurali/Desktop/Screenshot 2025-06-01 at 11.25.34 PM.png"


if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}")
    exit(1)

if not os.path.isfile(image_path):
    print(f"Error: Path is not a file: {image_path}")
    exit(1)

print(f"Using image: {image_path}")


LEETCODE_ANALYSIS_PROMPT = (
    "You are an expert LeetCode interview coach analyzing a screenshot of someone solving a coding problem. "
    "Your goal is to help them solve the problem efficiently and learn from the process.\n\n"
    
    "ANALYSIS FRAMEWORK:\n"
    "1. **Problem Identification**: \n"
    "   - What is the exact problem title and number?\n"
    "   - What type of problem is this? (Array, String, Tree, Graph, DP, etc.)\n"
    "   - What is the difficulty level?\n"
    "   - What are the key constraints and requirements?\n\n"
    
    "2. **Current Progress Assessment**:\n"
    "   - What approach is the user currently taking?\n"
    "   - How much of the solution have they completed?\n"
    "   - Are there any syntax errors or logical issues visible?\n"
    "   - What test cases are they working with?\n\n"
    
    "3. **Solution Strategy & Hints**:\n"
    "   - What is the optimal approach for this problem?\n"
    "   - What data structures and algorithms should be used?\n"
    "   - What is the expected time and space complexity?\n"
    "   - Are there any edge cases they should consider?\n\n"
    
    "4. **Code Review & Next Steps**:\n"
    "   - If code is visible, review it for correctness and efficiency\n"
    "   - What should they implement next?\n"
    "   - Any debugging suggestions if there are errors?\n"
    "   - Alternative approaches they could consider?\n\n"
    
    "5. **Complete Solution** (IMPORTANT):\n"
    "   - Provide a complete, working solution in the same language they're using\n"
    "   - Include detailed comments explaining the logic\n"
    "   - Mention the time and space complexity\n"
    "   - Format the code properly with proper indentation\n\n"
    
    "RESPONSE FORMAT:\n"
    "Structure your response with clear sections:\n"
    "- **Problem Analysis**: Brief problem summary\n"
    "- **Current Status**: What they've done so far\n"
    "- **Approach**: Recommended strategy\n"
    "- **Complete Solution**: Full working code\n"
    "- **Complexity**: Time and space analysis\n"
    "- **Next Steps**: What to do next\n\n"
    
    "IMPORTANT GUIDELINES:\n"
    "- Focus on the LeetCode problem, not UI elements\n"
    "- Provide actionable coding advice\n"
    "- Always include a complete, working solution\n"
    "- Explain the reasoning behind the approach\n"
    "- Help them understand patterns for similar problems\n"
    "- Be encouraging and educational\n\n"
    
    "Analyze this LeetCode screenshot and provide comprehensive problem-solving assistance:"
)

try:
    client = ollama.Client()
    print("Sending request to Ollama...")
    
    response = client.chat(
        model="gemma3:4b-it-qat",  # or your chosen model
        messages=[
            {
                "role": "user",
                "content": LEETCODE_ANALYSIS_PROMPT,
                "images": [image_path],  # Fixed: images should be a list
            }
        ],
    )

    print("Response received!")
    print("=" * 50)
    print(response["message"]["content"])
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("Make sure:")
    print("1. Ollama is running (ollama serve)")
    print("2. The model 'gemma3:4b-it-qat' is available (ollama list)")
    print("3. The image path is correct and accessible")
