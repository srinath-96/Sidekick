"""
CrewAI workflow manager for the LeetCode AI Assistant
"""
import threading
from crewai import Crew, Process
from .agents import create_screen_scanner_agent, create_image_analysis_agent
from .tasks import create_capture_task, create_analyze_task
from .logger import LeetCodeLogger
from .config import Config

class LeetCodeCrewManager:
    """Manages the CrewAI workflow for LeetCode analysis"""
    
    def __init__(self):
        self.analysis_in_progress = False
        self.logger = LeetCodeLogger()
        self._setup_crew()
    
    def _setup_crew(self):
        """Initialize the CrewAI agents, tasks, and crew"""
        # Create agents
        self.screen_scanner_agent = create_screen_scanner_agent()
        self.image_analysis_agent = create_image_analysis_agent()
        
        # Create tasks
        self.capture_task = create_capture_task(self.screen_scanner_agent)
        self.analyze_task = create_analyze_task(self.image_analysis_agent, self.capture_task)
        
        # Create crew
        self.crew = Crew(
            agents=[self.screen_scanner_agent, self.image_analysis_agent],
            tasks=[self.capture_task, self.analyze_task],
            process=Process.sequential,
            verbose=Config.VERBOSE
        )
    
    def run_analysis(self):
        """Run the screen analysis in a separate thread"""
        if self.analysis_in_progress:
            print("⚠️  Analysis already in progress, skipping...")
            return
        
        self.analysis_in_progress = True
        print("[DEBUG] run_analysis: started, analysis_in_progress set to True")
        
        try:
            print("🔍 Analyzing LeetCode problem...")
            self._setup_crew()  # Recreate agents, tasks, and crew for every analysis
            print("[DEBUG] Before self.crew.kickoff()")
            crew_output = self.crew.kickoff()
            print("[DEBUG] After self.crew.kickoff()")
            
            # Process the output
            raw_output = self._extract_raw_output(crew_output)
            
            # Log the results
            if raw_output:
                self.logger.log_analysis(raw_output, "")
                print("✅ LeetCode analysis complete! Solution saved to leetcode_solutions.md")
                
                # Show preview
                preview = self.logger.get_analysis_preview(raw_output)
                print(preview)
            else:
                print("❌ No analysis output received")
                
        except Exception as e:
            print(f"❌ Error during LeetCode analysis: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.analysis_in_progress = False
            print("[DEBUG] run_analysis: finished, analysis_in_progress set to False")
            # Cleanup screenshots
            self.logger.cleanup_screenshots()
    
    def _extract_raw_output(self, crew_output):
        """Extract raw text output from crew result"""
        if not crew_output:
            return "Error: Crew kickoff returned no output."
        
        if hasattr(crew_output, 'raw') and isinstance(crew_output.raw, str):
            return crew_output.raw
        else:
            return str(crew_output)
    
    def run_analysis_async(self):
        """Run analysis in a separate thread to avoid blocking the hotkey listener"""
        print("🔥 Hotkey triggered! Starting analysis...")
        threading.Thread(target=self.run_analysis, daemon=True).start() 