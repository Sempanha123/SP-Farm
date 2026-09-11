import subprocess
import time
import os
import datetime
import shutil
import string
import shlex
import random
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options


from core.automation_helper import AppiumHelper
from core.appium_manager import AppiumServerManager
class LDManager:
    def __init__(self, ui=None, general_function=None, data_manager=None):
        self.ui = ui
        self.general_function = general_function
        self.data_manager = data_manager
        self.settings = self.data_manager.get_ldplayer_settings()

        self.backup_dir = os.path.join(os.getcwd(), "backups")
        os.makedirs(self.backup_dir, exist_ok=True)

        self.LDList = []
        
        ldplayer_path = self.settings.get("ldplayer_path", "")
        if ldplayer_path.endswith("ldconsole.exe"):
            base_dir = os.path.dirname(ldplayer_path)
        else:
            base_dir = ldplayer_path

        self.ldconsole = os.path.join(base_dir, "ldconsole.exe")
        
        possible_adb = os.path.join(base_dir, "adb.exe")
        if os.path.exists(possible_adb):
            self.adb_path = possible_adb
        else:
            self.adb_path = "adb"
        
        if ldplayer_path.endswith("ldconsole.exe"):
            self.ldconsole = ldplayer_path
            
            # Automatically find adb.exe in the same folder as ldconsole.exe
            possible_adb = ldplayer_path.replace("ldconsole.exe", "adb.exe")
            if os.path.exists(possible_adb):
                self.adb_path = possible_adb
        else:
            possible_ld = os.path.join(ldplayer_path, "ldconsole.exe")
            if os.path.exists(possible_ld):
                self.ldconsole = possible_ld
            else:
                pass
            
            # Check for adb.exe in the provided directory
            possible_adb = os.path.join(ldplayer_path, "adb.exe")
            if os.path.exists(possible_adb):
                self.adb_path = possible_adb

    def run_command(self, args):
        if not os.path.exists(self.ldconsole):
            print(f"❌ CRITICAL ERROR: Cannot find ldconsole.exe at {self.ldconsole}")
            return None

        if isinstance(args, str):
            args = [args]
            
        cmd = [self.ldconsole] + args
        try:
            # We return the completed process object instead of just the output string
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if result.returncode != 0:
                print(f"⚠️ Command failed ({result.returncode}): {' '.join(cmd)}")
                return None
            
            return result 
        except Exception as e:
            print(f"❌ Error running command {cmd}: {e}")
            return None

    def open_ld(self, ld_name):
        print(f"🚀 Launching emulator: {ld_name}...")
        self.run_command(["launch", "--name", ld_name])

    def close_ld(self, ld_name):
        
        self.run_command(["quit", "--name", ld_name])

    def run_adb(self, cmd, device=None):
        full_cmd = [self.adb_path]
        if device:
            full_cmd.extend(["-s", device])
        full_cmd.extend(shlex.split(cmd))
        
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, check=False)
            return result.stdout.strip()
        except Exception as e:
            print(f"❌ ADB Error: {e}")
            return None
    
    def refresh_ld_path(self):
        self.settings = self.data_manager.get_ldplayer_settings()
        ldplayer_path = self.settings.get("ldplayer_path", "")
        
        if ldplayer_path.endswith("ldconsole.exe"):
            base_dir = os.path.dirname(ldplayer_path)
        else:
            base_dir = ldplayer_path

        possible_ld = os.path.join(base_dir, "ldconsole.exe")
        
        if os.path.exists(possible_ld):
            self.ldconsole = possible_ld
            
            # CRITICAL: Also update the ADB path so they stay synced!
            possible_adb = os.path.join(base_dir, "adb.exe")
            if os.path.exists(possible_adb):
                self.adb_path = possible_adb
            else:
                self.adb_path = "adb"
            return True
            
        return False

    def check_ld_path(self):
        return self.refresh_ld_path()

    def is_ld_running(self, ld_name):
        output = self.run_command(["runninglist"])

        if output is None: # If the command failed entirely
            return False
        stdout_text = getattr(output, 'stdout', output) or ""
        
        # If the output is in bytes (b''), decode it to a normal string
        if isinstance(stdout_text, bytes):
            stdout_text = stdout_text.decode('utf-8', errors='ignore')
            
        # Ensure it's actually a string before splitting
        stdout_text = str(stdout_text)

        running = [line.strip() for line in stdout_text.splitlines()]
        return ld_name.strip() in running




    def list_ld_instances(self):
        """List all LDPlayer instances."""
        result = self.run_command(["list2"])
        instances = []
        if result:
            for line in result.splitlines():
                parts = line.split(",")
                if len(parts) >= 5:
                    instances.append({
                        "index": parts[0].strip(),
                        "name": parts[1].strip(),
                        "status": parts[3].strip(),
                        "adb_port": parts[4].strip()
                    })
        return instances


    def stop_all(self):
        try:
            output = self.run_command(["list2"])
            if output:
                for line in output.splitlines():
                    parts = line.split(",")
                    if len(parts) >= 2:
                        ld_name = parts[1].strip()
                        self.run_command(["quit", "--name", ld_name])
                        self.kill_appium_session(ld_name, self.GetAppiumName(ld_name))
            else:
                print("⚠️ No open emulator sessions detected for dynamic shutdown.")
        except Exception as e:
            print(f"❌ Error during active shell execution kill phase: {e}")

    # -----------------------------------------------------
    # 🧩 Window Resizing Grid Arranger
    # -----------------------------------------------------
    def auto_arrange_by_setting(self):
        import win32gui
        import win32con
        import win32api

        ld_per_row = int(self.ui.ld_per_row.value())
        ld_per_column = int(self.ui.ld_per_column.value())
        
        running_hwnds = []

        def enum_windows_callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                class_name = win32gui.GetClassName(hwnd)
                window_title = win32gui.GetWindowText(hwnd)
                
                if "PlayerMainFrame" in class_name or "LDPlayer" in window_title:
                    if "Multi" not in window_title and "Manager" not in window_title:
                        running_hwnds.append(hwnd)
            return True

        win32gui.EnumWindows(enum_windows_callback, None)
        running_hwnds.sort(key=lambda h: win32gui.GetWindowText(h))

        if not running_hwnds:
            print("⚠️ No running or visible LDPlayer windows found to arrange.")
            return

        monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0, 0)))
        if isinstance(monitor_info, dict):
            usable_rect = monitor_info.get('WorkArea', monitor_info.get('Monitor', (0, 0, 1920, 1080)))
        else:
            usable_rect = monitor_info[1] if len(monitor_info) > 1 else (0, 0, 1920, 1080)
        
        start_x, start_y, end_x, end_y = usable_rect
        screen_width = end_x - start_x
        screen_height = end_y - start_y

        window_width = (screen_width // ld_per_row) - 2
        window_height = (screen_height // ld_per_column) - 2

        for layout_index, hwnd in enumerate(running_hwnds):
            column = layout_index % ld_per_row
            row = layout_index // ld_per_row

            pos_x = start_x + (column * (window_width + 2))
            pos_y = start_y + (row * (window_height + 2))

            win32gui.SetWindowPos(
                hwnd, win32con.HWND_TOP, 
                pos_x, pos_y, 
                window_width, window_height, 
                win32con.SWP_NOACTIVATE
            )


    # ==========================================================
    # REPAIR APP PERMISSIONS (DYNAMIC UID)
    # ==========================================================
    def repair_package_permissions(self, appium_name, package_name):
        import subprocess
        import re


        dumpsys = subprocess.run(
            ["adb", "-s", appium_name, "shell", "dumpsys", "package", package_name],
            capture_output=True, text=True
        )

        match = re.search(r"userId=(\d+)", dumpsys.stdout)
        if not match:
            print(f"⚠️ {package_name} not installed")
            return False

        uid = match.group(1)
        print(f"   UID = {uid}")

        commands = [
            f"chown -R {uid}:{uid} /data/data/{package_name}",
            f"chmod 700 /data/data/{package_name}",
            f"find /data/data/{package_name} -type d -exec chmod 700 {{}} \\;",
            f"find /data/data/{package_name} -type f -exec chmod 600 {{}} \\;",
            f"restorecon -R /data/data/{package_name}",
        ]

        for cmd in commands:
            subprocess.run(["adb", "-s", appium_name, "shell", "su", "0", cmd], capture_output=True)
        return True
    
    def repair_packages(self, appium_name, packages):
        for package in packages:
            try:
                self.repair_package_permissions(appium_name, package)
            except Exception as e:
                print(f"❌ {package}: {e}")

    def factory_reset_user_apps(self, appium_name):
        print(f"🗑️ Deep Factory Resetting identity & apps on {appium_name}...")

        try:
            # 1. Kill background processes
            subprocess.run(["adb", "-s", appium_name, "shell", "am", "kill-all"], capture_output=True)
            time.sleep(1)

            # 2. Clear 3rd party apps (This automatically wipes /data/data/ for Katana and Lite)
            SKIP_PACKAGES = {
                "io.appium.uiautomator2.server",
                "io.appium.uiautomator2.server.test",
                "com.vpn.fast.proxy.securecactus",
            }

            result = subprocess.check_output(
                ["adb", "-s", appium_name, "shell", "pm", "list", "packages", "-3"],
                text=True
            )
            packages = [x.replace("package:", "").strip() for x in result.splitlines() if x.strip()]

            for package in packages:
                if package in SKIP_PACKAGES:
                    continue
                subprocess.run(["adb", "-s", appium_name, "shell", "pm", "clear", package], capture_output=True)

            # 3. Wipe System XML Configs and Meta Tracking Footprints (Added FB Lite paths)
            identity_and_system_files = [
                "/data/system/users/0/settings_ssaid.xml",
                "/sdcard/Android/data/com.facebook.katana",
                "/sdcard/Android/media/com.facebook.katana",
                "/sdcard/Android/data/com.facebook.lite",  # 🟢 Added Lite
                "/sdcard/Android/media/com.facebook.lite", # 🟢 Added Lite
                "/sdcard/.facebook_cache",
            ]

            for path in identity_and_system_files:
                subprocess.run(["adb", "-s", appium_name, "shell", "su", "0", "rm", "-rf", path], capture_output=True)

            # 4. Safely wipe shared app caches
            subprocess.run(["adb", "-s", appium_name, "shell", "su", "0", "rm", "-rf", "/sdcard/Android/data/*/cache/*"], capture_output=True)
            
            # Recreate base folders
            subprocess.run(["adb", "-s", appium_name, "shell", "mkdir", "-p", "/sdcard/Android/data"], capture_output=True)
            subprocess.run(["adb", "-s", appium_name, "shell", "mkdir", "-p", "/sdcard/Android/media"], capture_output=True)

            time.sleep(2)
            print("✅ Emulator user data & system identity reset complete")
            return True

        except Exception as e:
            print(f"❌ Reset failed: {e}")
            return False
    # def backup_full_device_with_identity(self, acc_id, update_ld_signal, ld_name, appium_name, backup_name=None, output_dir="backups"):
    #     if not backup_name:
    #         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    #         backup_name = f"{ld_name}_backup_{timestamp}"
            
    #     backup_root = os.path.join(output_dir, backup_name)
        
    #     if os.path.exists(backup_root):
    #         shutil.rmtree(backup_root) 
    #     os.makedirs(backup_root, exist_ok=True)
        
    #     remote_archive = "/sdcard/fb_data.tar"

    #     try:
    #         print(f"💾 Starting Facebook-only backup for {ld_name}")

    #         IMPORTANT_PATHS = ["/data/data/com.facebook.katana"]
            
    #         # 1. Check if FB data exists using su -c (with single quotes around the command)
    #         check_cmd = f"shell su -c 'ls {IMPORTANT_PATHS[0]}'"
    #         check_out = self.run_adb(check_cmd, device=appium_name)
            
    #         if check_out is None or "No such file" in check_out:
    #             print("❌ No Facebook data found to backup.")
    #             update_ld_signal.emit(ld_name, "❌ No FB Data Found")
    #             return None

    #         # 2. Force stop FB using run_adb (Doesn't need root, but good practice to clear memory)
    #         self.run_adb("shell am force-stop com.facebook.katana", device=appium_name)

    #         # 3. Create tar archive using su -c
    #         paths_joined = " ".join(IMPORTANT_PATHS)
    #         # Add --warning=no-file-changed to prevent tar from crashing on cache files
    #         tar_cmd = f"shell su -c 'tar -cf {remote_archive} {paths_joined}'"
    #         print("🗜️ Zipping Facebook data on emulator...")
    #         self.run_adb(tar_cmd, device=appium_name)

    #         # 4. Pull backup to PC (Direct subprocess with a TIMEOUT added so it never freezes again)
    #         local_archive = os.path.join(backup_root, "fb_data.tar")
    #         print("📥 Pulling Facebook archive to PC...")
            
    #         # 🟢 PRO-TIP: Always add a timeout to subprocess calls to prevent permanent freezing
    #         subprocess.run(
    #             [self.adb_path, "-s", appium_name, "pull", remote_archive, local_archive], 
    #             capture_output=True, 
    #             timeout=60 # Will abort if it takes longer than 60 seconds
    #         )

    #         print("✅ FB Backup complete")
    #         update_ld_signal.emit(ld_name, "✅ Backup complete")
    #         return backup_root

    #     except subprocess.TimeoutExpired:
    #         print("❌ Backup timed out! ADB got stuck pulling the file.")
    #         update_ld_signal.emit(ld_name, "❌ Backup Timeout")
    #         return None
    #     except Exception as e:
    #         print(f"❌ Backup Exception: {e}")
    #         update_ld_signal.emit(ld_name, "❌ Script Error")
    #         return None
    #     finally:
    #         # Clean up using su -c
    #         self.run_adb(f"shell su -c 'rm -f {remote_archive}'", device=appium_name)

    # def restore_full_device_with_identity(self, appium_name, backup_folder):
    #     local_archive = os.path.join(backup_folder, "fb_data.tar")
        
    #     if not os.path.exists(local_archive):
    #         # local_archive = os.path.join(backup_folder, "full_app_data.tar")
    #     # if not os.path.exists(local_archive):
    #         print("❌ Cannot find fb_data.tar or full_app_data.tar in backup folder.")
    #         return False

    #     remote_archive = "/sdcard/restore_fb_data.tar"
    #     IMPORTANT_PACKAGES = ["com.facebook.katana"]

    #     try:
    #         print(f"🔄 Starting restore process for {appium_name}...")
    #         # 1. Force stop FB using run_adb
    #         self.run_adb("shell am force-stop com.facebook.katana", device=appium_name)

    #         # 2. Upload Backup (Direct subprocess to protect Windows paths!)
    #         print("📤 Pushing backup to emulator...")
    #         try:
    #             push_result = subprocess.run(
    #                 [self.adb_path, "-s", appium_name, "push", local_archive, remote_archive],
    #                 capture_output=True, text=True,
    #                 timeout=60 # 🟢 Added timeout to prevent freeze during transfer
    #             )
    #             if push_result.returncode != 0:
    #                 print(f"❌ Failed to push: {push_result.stderr}")
    #                 return False
    #         except subprocess.TimeoutExpired:
    #             print("❌ Push timed out! Emulator might be frozen.")
    #             return False

    #         # 3. Extract Files using run_adb (🟢 FIXED: Added -c and single quotes)
    #         print("📦 Extracting data on emulator...")
    #         self.run_adb(f"shell su -c 'tar -xf {remote_archive} -C /'", device=appium_name)

    #         # 4. Repair Facebook Permissions ONLY
    #         # (Note: Extracting as root sets the owner to root, so repair_packages MUST run chown!)
    #         # print("🔧 Repairing app permissions...")
    #         # self.repair_packages(appium_name, IMPORTANT_PACKAGES)

    #         # 5. Clean FB Cache safely using run_adb (🟢 FIXED: Wrapped in su -c for wildcards)
    #         print("🧹 Clearing old cache...")
    #         self.run_adb("shell su -c 'rm -rf /sdcard/Android/data/com.facebook.katana/cache/*'", device=appium_name)

    #         print("✅ Restore complete!")
    #         return True

    #     except Exception as e:
    #         print(f"❌ Restore Exception: {e}")
    #         return False
    #     finally:
    #         # 🟢 FIXED: Wrapped cleanup in su -c to ensure it deletes properly
    #         self.run_adb(f"shell su -c 'rm -f {remote_archive}'", device=appium_name)
    #         print("🧹 Temporary files removed")

    def backup_full_device_with_identity(self, acc_id, update_ld_signal, ld_name, appium_name, backup_name=None, output_dir="backups", package_name="com.facebook.katana"):
        # 1. Create Folder Structure
        if not backup_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{ld_name}_backup_{timestamp}"
            
        backup_root = os.path.join(output_dir, backup_name)
        
        # 🟢 Safely create the folder (Will NOT delete existing files, so we can store multiple apps here)
        os.makedirs(backup_root, exist_ok=True)
        
        # 🟢 DYNAMIC FILE NAMES: Uses the package name so they don't overwrite each other!
        remote_archive = f"/sdcard/{package_name}_data.tar"
        local_archive = os.path.join(backup_root, f"{package_name}.tar")

        try:
            print(f"💾 Starting Mini-Backup for {ld_name} ({package_name})")
            FB_DIR = f"/data/data/{package_name}"
            
            # Check if app data exists
            check_cmd = f"shell su -c 'ls {FB_DIR}/shared_prefs'"
            check_out = self.run_adb(check_cmd, device=appium_name)
            
            if check_out is None or "No such file" in check_out:
                print(f"❌ No session data found for {package_name}.")
                update_ld_signal.emit(ld_name, f"❌ No Data: {package_name}")
                return None

            # Force stop the app
            self.run_adb(f"shell am force-stop {package_name}", device=appium_name)

            # Create archive
            ESSENTIAL_FOLDERS = "shared_prefs databases app_light_prefs"
            tar_cmd = f"shell su -c 'tar -cf {remote_archive} -C {FB_DIR} {ESSENTIAL_FOLDERS}'"
            
            print(f"🗜️ Zipping essential data for {package_name}...")
            self.run_adb(tar_cmd, device=appium_name)

            # Pull backup to PC
            print(f"📥 Pulling {package_name}.tar to PC...")
            subprocess.run(
                [self.adb_path, "-s", appium_name, "pull", remote_archive, local_archive], 
                capture_output=True, 
                timeout=60
            )

            print(f"✅ Backup complete for {package_name}")
            update_ld_signal.emit(ld_name, f"✅ Saved {package_name}")
            return backup_root

        except subprocess.TimeoutExpired:
            print(f"❌ Backup timed out for {package_name}.")
            return None
        except Exception as e:
            print(f"❌ Backup Exception: {e}")
            return None
        finally:
            self.run_adb(f"shell su -c 'rm -f {remote_archive}'", device=appium_name)

    def restore_full_device_with_identity(self, appium_name, backup_folder, package_name="com.facebook.katana"):
        # 🟢 DYNAMIC FILE NAMES: Looks for the specific app's .tar file
        local_archive = os.path.join(backup_folder, f"{package_name}.tar")
        
        if not os.path.exists(local_archive):
            print(f"❌ Cannot find {package_name}.tar in backup folder.")
            return False

        remote_archive = f"/sdcard/restore_{package_name}.tar"
        FB_DIR = f"/data/data/{package_name}"

        try:
            print(f"🔄 Starting restore process for {appium_name} ({package_name})...")
            
            # Force stop the app
            self.run_adb(f"shell am force-stop {package_name}", device=appium_name)

            # Upload Backup
            print(f"📤 Pushing {package_name} backup to emulator...")
            try:
                push_result = subprocess.run(
                    [self.adb_path, "-s", appium_name, "push", local_archive, remote_archive],
                    capture_output=True, text=True,
                    timeout=60
                )
                if push_result.returncode != 0:
                    print(f"❌ Failed to push: {push_result.stderr}")
                    return False
            except subprocess.TimeoutExpired:
                print("❌ Push timed out! Emulator might be frozen.")
                return False

            # Extract Files
            print("📦 Extracting data on emulator...")
            self.run_adb(f"shell su -c 'tar -xf {remote_archive} -C {FB_DIR}/'", device=appium_name)

            # Repair App Permissions
            print("🔧 Repairing app permissions...")
            fix_owner_cmd = f"shell su -c 'chown -R $(stat -c %U {FB_DIR}):$(stat -c %g {FB_DIR}) {FB_DIR}'"
            self.run_adb(fix_owner_cmd, device=appium_name)

            fix_selinux_cmd = f"shell su -c 'restorecon -R {FB_DIR}'"
            self.run_adb(fix_selinux_cmd, device=appium_name)

            # Clean Cache
            print("🧹 Clearing old cache...")
            self.run_adb(f"shell su -c 'rm -rf /sdcard/Android/data/{package_name}/cache/*'", device=appium_name)

            print(f"✅ Restore complete for {package_name}!")
            return True

        except Exception as e:
            print(f"❌ Restore Exception: {e}")
            return False
        finally:
            self.run_adb(f"shell su -c 'rm -f {remote_archive}'", device=appium_name)




    def wait_until_closed(self, ld_name, timeout=30):
        # Reset apps FIRST
        # self.factory_reset_user_apps(self.GetAppiumName(ld_name))
        self.close_ld(ld_name)
        start = time.time()
        while self.is_ld_running(ld_name):
            if time.time() - start > timeout:
                print(f"⚠️ Timeout waiting for {ld_name}")
                return False
            time.sleep(1)

        # self.kill_appium_session(ld_name, appnium)
        # print(f"✅ {ld_name} fully closed")
        return True

    def wait_for_emulator_ready(self, appium_name, timeout=200):
        if not appium_name:
            print("❌ Error: appium_name is None! The emulator hasn't assigned a port yet.")
            return False

        start_time = time.time()
        while time.time() - start_time < timeout:
            
            try:
                result = subprocess.check_output([self.adb_path, 'devices'], stderr=subprocess.STDOUT, text=True)
                lines = result.strip().split('\n')
                print(lines)
                for line in lines[1:]:
                    print(line) # You can comment this out to reduce console spam
                    if appium_name in line and "device" in line:
                        return True
            except Exception as e:
                print(f"❌ Error checking ADB devices: {e}")
            
            time.sleep(2.5)

        print(f"❌ Timeout! {appium_name} not ready within {timeout} seconds.")
        return False

    def GetAppiumName(self, instance_name):
        if not self.LDList:
            self.get_ldplayer_instances()
        instance_info = next((inst for inst in self.LDList if inst["name"] == instance_name), None)
        if instance_info:
            return instance_info["appium_name"]
        print(f"No instance found with name: {instance_name}")

        return None

    def get_ldplayer_instances(self):
        try:
            # Call with a list
            result = self.run_command(["list2"]) 
            
            # Now we check if result exists before trying to access .stdout
            if result is None: 
                return []

            output = result.stdout.strip()
            instances = []
            
            for line in output.splitlines():
                row = line.split(',')
                if len(row) >= 2:
                    try:
                        index = int(row[0].strip())
                        name = row[1].strip()
                        appium_port = 5554 + (index * 2)
                        
                        instances.append({
                            "index": index,
                            "name": name,
                            "appium_name": f"emulator-{appium_port}",
                            "leidian": f"leidian{index}"
                        })
                    except ValueError:
                        continue 

            self.LDList = instances
            return instances
        except Exception as e:
            print(f"❌ Unexpected error parsing devices: {e}")
            return []
    
    def check_and_force_root(self, appium_name):
        
        try:
            # 1. Check current user status via adb shell
            check_cmd = [self.adb_path, '-s', appium_name, 'shell', 'whoami']
            current_user = subprocess.check_output(check_cmd, stderr=subprocess.DEVNULL, text=True).strip()
            
            if current_user == "root":
                print(f"🎯 [Root Guard] {appium_name} is ALREADY running as root user.")
                return True
            root_cmd = ['adb', '-s', appium_name, 'root']
            root_output = subprocess.check_output(root_cmd, stderr=subprocess.STDOUT, text=True).strip()
            
            time.sleep(3)
            
            # 4. Re-verify the status layout
            current_user_retry = subprocess.check_output(check_cmd, stderr=subprocess.DEVNULL, text=True).strip()
            if current_user_retry == "root":
                return True
            else:
                print(f"❌ [Root Guard] Failed to elevate {appium_name}. Make sure 'Root Permission' is checked in LDPlayer settings.")
                return False
                
        except Exception as e:
            # # print(f"❌ [Root Guard] Exception occurred while configuring permissions on {appium_name}: {e}")
            # result = subprocess.check_output(['adb', 'devices'], stderr=subprocess.STDOUT, text=True)
            # print(f"❌ adb devices ❌ {result}")
            return False
        
    def connect_to_ldplayer(self, ld_name: str, appium_name: str):
        max_retries = 3
        try:
            port_digits = "".join(filter(str.isdigit, appium_name))
            base_port = int(port_digits) if port_digits else 5554
            
            # Your math: 8254, 8256, 8258
            unique_system_port = 8200 + (base_port % 100)
            
            # 🟢 THE FIX 1: Generate a unique MJPEG port to stop silent collisions
            unique_mjpeg_port = 9100 + (base_port % 100) 
        except Exception:
            unique_system_port = 8200
            unique_mjpeg_port = 9100
        # 2. Configure the automated driver options framework
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        
        options.device_name = str(appium_name)  
        options.set_capability("appium:udid", str(appium_name)) 
        options.set_capability("appium:systemPort", unique_system_port)
        options.set_capability("appium:mjpegServerPort", unique_mjpeg_port) # 🟢 ADDED

        options.set_capability("appium:noReset", True)
        options.set_capability("appium:dontStopAppOnReset", True)
        options.set_capability("appium:skipDeviceInitialization", True)
        options.set_capability("appium:skipServerInstallation", False)

        # 🟢 THE FIX 2: Uncomment and maximize timeouts to survive CPU lag spikes
        # newCommandTimeout: How long Appium waits for your Python script to send the next command before killing the session.
        options.set_capability("appium:newCommandTimeout", 180) 
        # adbExecTimeout: How long Appium waits for the ADB bridge to respond (CRITICAL for multiple emulators).
        options.set_capability("appium:adbExecTimeout", 120000) 
        # uiautomator2ServerLaunchTimeout: Gives heavy emulators plenty of time to boot the UI2 server.
        options.set_capability("appium:uiautomator2ServerLaunchTimeout", 120000)

        # 3. Connect to the running background Appium Server bridge
        server_url = "http://127.0.0.1:4723"
        for attempt in range(max_retries):
            try:
                driver = webdriver.Remote(server_url, options=options)
                
                # Initialize your automation tool macro helper
                reconnect_hook = lambda broken_ld_name: self.connect_to_ldplayer(broken_ld_name, appium_name)[0]
                bot = AppiumHelper(driver, ld_name, reconnect_callback=reconnect_hook)
                
                # print(f"🚀🚀🚀🚀🚀 {ld_name} is successfully connected to Appium Server")
                return driver, bot

            except Exception as e:
                print(f"⚠️ Connection attempt {attempt + 1} to {ld_name} failed. Error: {e}")
                
                if not AppiumServerManager.is_running():
                    AppiumServerManager.start_server()
                    time.sleep(4) 
                else:
                    time.sleep(3)
                    
        print(f"❌ Critical connection failure to {ld_name} after {max_retries} attempts.")
        return None, None

    def kill_appium_session(self, ld_name, appium_name):
        """
        Kills the Appium node process running on the specific system port 
        assigned to the given ld_name/appium_name.
        """
        try:
            # 1. Replicate your port calculation logic
            port_digits = "".join(filter(str.isdigit, appium_name))
            base_port = int(port_digits) if port_digits else 5554
            target_port = 8200 + (base_port % 100)
            
            print(f"🧹 Attempting to clean up Appium on port {appium_name} {target_port} for {ld_name}...")

            # 2. Use netstat to find the PID of the process using this port, then kill it
            # This command finds the PID (last column) and passes it to taskkill
            command = f'for /f "tokens=5" %a in (\'netstat -aon ^| findstr ":{target_port}"\') do taskkill /f /pid %a'
            
            # We use shell=True because of the piping ('|') in the command
            subprocess.run(command, shell=True, capture_output=True, text=True)
            
   
            
        except Exception as e:
            print(f"⚠️ Error cleaning up Appium process: {e}")


    def push_farm_profile(self, device_name, payload_content):
        temp_filename = f"temp_farm_{device_name}.prop"
        try:
            # 1. Write the payload to a local temporary file
            with open(temp_filename, "w", encoding="utf-8") as f:
                f.write(payload_content)
            
            # 2. Push the file directly to the device
            # This avoids shell/quote escaping issues entirely
            self.run_adb(f"push {temp_filename} /data/local/tmp/farm.prop", device=device_name)
            
            # 3. Set permissions
            self.run_adb("shell chmod 777 /data/local/tmp/farm.prop", device=device_name)
            
            # 4. Clean up local temp file
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
            return True
        except Exception as e:
            print(f"❌ Failed to push farm profile: {e}")
            return False

    def force_stop_app(self, device_name, package_name):
        self.run_adb(f"shell am force-stop {package_name}", device=device_name)

    def launch_app(self, device_name, package_name):
        self.run_adb(f"shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1", device=device_name)











    