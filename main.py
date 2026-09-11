# main.py
import sys
import subprocess
import time
from PySide6.QtWidgets import QApplication
from app.main_window import MainWindow

# Import the new manager you just created
from core.appium_manager import AppiumServerManager 

def reset_adb_on_startup():
    print("🧹 Cleaning up old ADB connections...")
    try:
        subprocess.run(["adb", "kill-server"], check=True, capture_output=True)
        subprocess.run(["adb", "start-server"], check=True, capture_output=True)
        time.sleep(5) 
        
    except FileNotFoundError:
        print("⚠️ ADB not found in system PATH. Skipping reset.")


if __name__ == "__main__":
    # 1. Clean up ADB first
    # reset_adb_on_startup()
    
    # 2. Start Appium automatically in the background
    # AppiumServerManager.start_server()

    # 3. Launch the UI
    app = QApplication(sys.argv)
    window = MainWindow()  
    window.show()

    # 4. Run the app until the user clicks the 'X' button
    exit_code = app.exec()
    
    # 5. This line will now ONLY run AFTER you close the UI window!
    # AppiumServerManager.stop_server()
    
    sys.exit(exit_code)