# core/appium_manager.py
import subprocess
import time
import sys
import urllib.request
import urllib.error

class AppiumServerManager:
    _process = None

    @classmethod
    def is_running(cls) -> bool:
        """
        Pings the Appium server status endpoint. 
        Returns True if alive, False if dead.
        """
        try:
            # Appium 2.x uses this status endpoint
            response = urllib.request.urlopen("http://127.0.0.1:4723/status", timeout=2)
            return response.getcode() == 200
        except (urllib.error.URLError, ConnectionResetError):
            return False
        except Exception:
            return False

    @classmethod
    def reset_adb_on_startup():
        try:
            subprocess.run(["adb", "kill-server"], check=True, capture_output=True)
            subprocess.run(["adb", "start-server"], check=True, capture_output=True)
            time.sleep(2) 
            
        except FileNotFoundError:
            print("⚠️ ADB not found in system PATH. Skipping reset.")
    @classmethod
    def start_server(cls):
        try:
            # shell=True runs this exactly like typing it in CMD
            # stdout/stderr are sent to DEVNULL to stop Appium from spamming your Python console
            cls._process = subprocess.Popen(
                "appium --allow-cors",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅ Appium Server started.")
            time.sleep(1.5)  # Wait 3 seconds to let the server fully boot up
        except Exception as e:
            print(f"❌ Failed to start Appium Server: {e}")

    @classmethod
    def stop_server(cls):
        if cls._process:
            print("🛑 Shutting down Appium Server...")
            try:
                # Because we used shell=True on Windows, we have to kill the process tree
                if sys.platform == "win32":
                    subprocess.call(
                        ['taskkill', '/F', '/T', '/PID', str(cls._process.pid)], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL
                    )
                else:
                    cls._process.terminate()
                print("✅ Appium Server stopped.")
            except Exception as e:
                print(f"⚠️ Error stopping Appium: {e}")