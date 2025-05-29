import mss
import time
import datetime
import os

# --- Configuration ---
SCREENSHOT_INTERVAL = 5  # Seconds between screenshots
OUTPUT_DIRECTORY = "periodic_screenshots"  # Folder to save screenshots
FILENAME_PREFIX = "screenshot_"

def take_periodic_screenshots():
    """
    Takes a screenshot at a regular interval and saves it.
    """
    print(f"--- Periodic Screenshot Script Started ---")
    print(f"Taking a screenshot every {SCREENSHOT_INTERVAL} seconds.")
    print(f"Screenshots will be saved in the '{OUTPUT_DIRECTORY}' directory.")
    print("Press Ctrl+C to stop the script.")

    # Create the output directory if it doesn't exist
    try:
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)
            print(f"Created directory: {OUTPUT_DIRECTORY}")
    except OSError as e:
        print(f"Error creating directory {OUTPUT_DIRECTORY}: {e}")
        print("Please ensure you have permissions to create this directory, or create it manually.")
        return

    try:
        with mss.mss() as sct:
            # Determine the monitor to capture.
            # sct.monitors[0] is the virtual screen including all monitors.
            # sct.monitors[1] is usually the primary monitor.
            if len(sct.monitors) > 1:
                monitor_to_capture = sct.monitors[1] # Primary monitor
                print(f"Capturing primary monitor: {monitor_to_capture}")
            elif sct.monitors:
                monitor_to_capture = sct.monitors[0] # The only available monitor (might be all screens)
                print(f"Capturing available monitor: {monitor_to_capture}")
            else:
                print("Error: No monitors found by mss.")
                return

            while True:
                try:
                    # Get current timestamp for a unique filename
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3] # YearMonthDay_HourMinuteSecond_Milliseconds
                    filename = f"{FILENAME_PREFIX}{timestamp}.png"
                    full_path = os.path.join(OUTPUT_DIRECTORY, filename)

                    # Capture the screen
                    sct_img = sct.grab(monitor_to_capture)

                    # Save the_image
                    mss.tools.to_png(sct_img.rgb, sct_img.size, output=full_path)
                    print(f"Screenshot saved: {full_path}")

                except mss.exception.ScreenShotError as e_mss:
                    print(f"MSS Error during capture: {e_mss}")
                    print("This might happen if the screen is locked or display changes.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

                # Wait for the next interval
                print(f"Waiting for {SCREENSHOT_INTERVAL} seconds...")
                time.sleep(SCREENSHOT_INTERVAL)

    except KeyboardInterrupt:
        print("\n--- Script Interrupted by User ---")
        print("Periodic screenshots stopped.")
    except Exception as e_outer:
        print(f"A critical error occurred: {e_outer}")

if __name__ == "__main__":
    # Before running, ensure your terminal/Python has screen recording permissions
    # if required by your OS (especially on macOS).
    # On macOS: System Settings > Privacy & Security > Screen Recording
    take_periodic_screenshots()