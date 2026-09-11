from PySide6.QtCore import QObject, Signal, QThread
import time
import subprocess
import os
import queue

from PySide6.QtCore import QObject, Signal, QThread
import time
import queue

class EmulatorWorker(QObject):
    
    update_acc_signal = Signal(str, bool, dict)  
    update_ld_signal = Signal(str, str)   
    account_started_signal = Signal(str)
    account_finished_signal = Signal(str) 

    def __init__(self, ld_name, account_queue, stop_events, ld_manager, account_cache, general_function, mode, active_tab, reg_tab):
        super().__init__()
        self.ld_name = ld_name
        self.account_queue = account_queue
        self.stop_events = stop_events
        self.ld_manager = ld_manager
        self.account_cache = account_cache
        self.general_function = general_function
        self.mode = mode
        self.active_tab = active_tab
        self.reg_tab = reg_tab
        self.is_aborted = False

    # 🟢 FIX: Added stop method to instantly kill boot sequences
    def stop(self):
        self.is_aborted = True
        print(f"🛑 Abort signal received for {self.ld_name}")

    def run(self):
        appium_name = None
        driver = None
        
        try:
            if self.is_aborted: return
            self.update_ld_signal.emit(self.ld_name, "⚡ Starting Emulator...")
            self.ld_manager.open_ld(self.ld_name)
            time.sleep(3)
            self.ld_manager.auto_arrange_by_setting()
            appium_name = self.ld_manager.GetAppiumName(self.ld_name)
            
            # Wait boot
            time.sleep(3)
            if self.is_aborted: return
            if not self.ld_manager.wait_for_emulator_ready(appium_name):
                self.update_ld_signal.emit(self.ld_name, "❌ Emulator boot failed")
                return

            if self.is_aborted: return

            # Root check
            if not self.ld_manager.check_and_force_root(appium_name):
                if not self.ld_manager.wait_for_emulator_ready(appium_name):
                    if not self.ld_manager.check_and_force_root(appium_name):
                        self.update_ld_signal.emit(self.ld_name, "❌ Root failed")
                        return
            
            if self.is_aborted: return

            # CONNECT APPIUM
            driver, bot = self.ld_manager.connect_to_ldplayer(self.ld_name, appium_name)
            if not driver or not bot:
                self.update_ld_signal.emit(self.ld_name, "⚠️ Appium connection failed")
                return

            # =======================================================
            # 🟢 ACCOUNT QUEUE LOOP
            # =======================================================
            while not self.account_queue.empty():
                if self.is_aborted: break
                
                acc_id = None
                try:
                    acc_id = self.account_queue.get_nowait()
                except queue.Empty:
                    break

                # 🟢 INNER TRY-CATCH
                try:
                    self.ld_manager.factory_reset_user_apps(appium_name)
                    if self.stop_events[acc_id].is_set():
                        continue 
                    self.account_started_signal.emit(str(acc_id))

                    self.update_ld_signal.emit(self.ld_name, f"[{acc_id}] ⚡ Processing...")
                    

                    data_acc = {}
                    if self.mode == "reg":
                        
                        lat, long = self.general_function.get_coordinates_from_ui(self.reg_tab.settings.get("fake_location", ""))
                        time_zone = self.reg_tab.settings.get("time_zone", "")
                        
                        phone_input1 = self.reg_tab.settings.get("phone_input1", "")
                        phone_input2 = self.reg_tab.settings.get("phone_input2", "")
                        phone_input3 = self.reg_tab.settings.get("phone_input3", "")
                        phone_number = self.general_function.generate_random_phone(phone_input1, phone_input2, phone_input3)
              
                        data_device = self.general_function.generate_full_professional_profile(lat, long, time_zone, phone_number)   

               
                        payload_content = "\n".join([f"{k}={v}" for k, v in data_device.items() if v])
                        self.ld_manager.push_farm_profile(appium_name, payload_content)
                        self.ld_manager.force_stop_app(appium_name, "com.facebook.lite")
                        self.ld_manager.force_stop_app(appium_name, "com.facebook.katana")

                        bot_success = self.reg_tab.Start_Reg(
                            driver=driver, bot=bot, acc_id=acc_id, ld_name=self.ld_name,
                            appium_name=appium_name, update_ld_signal=self.update_ld_signal,
                            stop_event=self.stop_events[acc_id], data_device=data_device, phone_number=phone_number
                        )

                    else:
                        self.update_acc_signal.emit(acc_id, False, {"status": f"🔄 Starting Account on {self.ld_name}"})
                        data_acc = self.account_cache.get_by_id(acc_id)

                        raw_phone = data_acc.get("phone_number", [])
                        if isinstance(raw_phone, list) and len(raw_phone) > 0:
                            mobile_no = str(raw_phone[0])
                        elif isinstance(raw_phone, str):
                            mobile_no = raw_phone
                        else:
                            mobile_no = ""
                        

                        data_device = {
                            "manufacturer": data_acc.get("manufacturer", ""),
                            "model": data_acc.get("model", ""),
                            "market_name": data_acc.get("market_name", ""),
                            "android_id": data_acc.get("android_id", ""),
                            "serial_number": data_acc.get("serial_number", ""),
                            "hardware": data_acc.get("hardware", ""),
                            "board": data_acc.get("board", ""),
                            "bootloader": data_acc.get("bootloader", ""),
                            "build_fingerprint": data_acc.get("build_fingerprint", ""),
                            "imei": data_acc.get("imei", ""),
                            "meid": data_acc.get("meid", ""),
                            "gsf_id": data_acc.get("gsf_id", ""),
                            "advertising_id": data_acc.get("advertising_id", ""),
                            "mac": data_acc.get("mac", ""),
                            "bluetooth_mac": data_acc.get("bluetooth_mac", ""),
                            "wifi_ssid": data_acc.get("wifi_ssid", ""),
                            "wifi_bssid": data_acc.get("wifi_bssid", ""),
                            "network_generation": data_acc.get("network_generation", "13"),
                            "imsi": data_acc.get("imsi", ""),
                            "simid": data_acc.get("simid", ""),
                            "mobile_no": mobile_no, 
                            "esim_eid": data_acc.get("esim_eid", ""),
                            "sim_operator": data_acc.get("sim_operator", ""),
                            "sim_operator_name": data_acc.get("sim_operator_name", ""),
                            "sim_country_iso": data_acc.get("sim_country_iso", ""),
                            "timezone": data_acc.get("time_zone", ""), 
                            "latitude": data_acc.get("gps", {}).get("lat", ""),
                            "longitude": data_acc.get("gps", {}).get("long", "")
                        }

                        # 5. Push Identity Payload
                        payload_content = "\n".join([f"{k}={v}" for k, v in data_device.items() if v])                            
                        self.ld_manager.push_farm_profile(appium_name, payload_content)
                        self.ld_manager.force_stop_app(appium_name, "com.facebook.katana")
                        self.ld_manager.force_stop_app(appium_name, "com.facebook.lite")
                        self.ld_manager.force_stop_app(appium_name, "com.example.spfarmchanger")

                        # Restore Device
                        raw_backup_path = data_acc.get("backup_file_name")
                        if raw_backup_path and os.path.exists(os.path.normpath(str(raw_backup_path).strip())):
                            backup_folder = os.path.normpath(str(raw_backup_path).strip())
                            self.update_ld_signal.emit(self.ld_name, "🔄 Restoring device data...")
                            
                            # 🟢 1. Try restoring Main Facebook (Katana)
                            katana_success = self.ld_manager.restore_full_device_with_identity(
                                appium_name, 
                                backup_folder, 
                                package_name="com.facebook.katana"
                            )
                            
                            # 🟢 2. Try restoring Facebook Lite
                            lite_success = self.ld_manager.restore_full_device_with_identity(
                                appium_name, 
                                backup_folder, 
                                package_name="com.facebook.lite"
                            )
                            
                            # 🟢 3. Check if AT LEAST ONE restore was successful
                            if not katana_success and not lite_success:
                                self.update_acc_signal.emit(acc_id, True, {"status": "❌ Restore Failed (Skipping)"})
                                continue # Skip to next account
                                
                        else:
                            self.update_acc_signal.emit(acc_id, True, {"status": "❌ Backup folder missing (Skipping)"})
                            continue # Skip to next account

                        if self.stop_events[acc_id].is_set():
                            continue

                        # Start Bot
                        bot_success = self.active_tab.Start_Active_Accounts(
                            driver=driver, bot=bot, acc_id=acc_id, ld_name=self.ld_name,
                            appium_name=appium_name, data_acc=data_acc,
                            update_acc_signal=self.update_acc_signal, 
                            update_ld_signal=self.update_ld_signal, stop_event=self.stop_events[acc_id]
                        )
                
                except Exception as acc_err:
                    error_msg = f"❌ Account Crash: {str(acc_err)[:40]}"
                    self.update_ld_signal.emit(self.ld_name, error_msg)
                    self.update_acc_signal.emit(acc_id, True, {"status": error_msg})
                    print(acc_err)

                finally:
                    # self.ld_manager.factory_reset_user_apps(appium_name)
                    if acc_id:
                        if self.stop_events[acc_id].is_set():
                            self.update_acc_signal.emit(acc_id, True, {"status": "🛑 Stopped"})
                        
                        self.account_queue.task_done()
                        self.account_finished_signal.emit(str(acc_id)) # Update the UI Counter!

        # Outer Try-Catch
        except Exception as e:
            self.update_ld_signal.emit(self.ld_name, f"❌ Emulator Crash: {str(e)[:40]}")
            print(str(e))
            
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            try:
                if self.ld_manager.is_ld_running(self.ld_name):
                    self.ld_manager.close_ld(self.ld_name)
            except Exception as e:
                print(f"❌ Failed to close {self.ld_name} during cleanup: {e}")

class EmulatorManualWorker(QThread):
    update_acc_signal = Signal(str, bool, dict)  # acc_id, save, ui_data
    update_ld_signal = Signal(str, str)         # ld_name, message
    close_ld_signal = Signal(list)              # list of acc_ids to close
    account_finished_signal = Signal(str)       # Signals UI counter
    account_started_signal = Signal(str)

    def __init__(self, stop_events, ld_name, shared_queue, actions, ld_manager, account_cache, general_function, active_tab_controller):
        super().__init__()
        self.ld_name = ld_name
        self.queue = shared_queue
        self.actions = actions
        
        self.ld_manager = ld_manager
        self.account_cache = account_cache
        self.general_function = general_function
        self.active_tab_controller = active_tab_controller
        self.stop_events = stop_events
        
        self.is_running = True
        self.current_acc_id = None
        self.manual_idle_ready = False # 🟢 FIX: Tracks if it's safe to enter idle loop

    def stop(self):
        self.is_running = False
        print(f"🛑 Stop flag set for {self.ld_name}")

    def run(self):
        appium_name = None
        driver = None
        
        try:
            self.update_ld_signal.emit(self.ld_name, "⚡ Starting Emulator...")
            self.ld_manager.open_ld(self.ld_name)
            time.sleep(2)
            self.ld_manager.auto_arrange_by_setting()
            appium_name = self.ld_manager.GetAppiumName(self.ld_name)
            
            # Wait boot
            time.sleep(3)
            if not self.ld_manager.wait_for_emulator_ready(appium_name):
                self.update_ld_signal.emit(self.ld_name, "❌ Boot failed")
                return # Jumps to finally block safely because manual_idle_ready is False

            # Root check
            if not self.ld_manager.check_and_force_root(appium_name):
                if not self.ld_manager.wait_for_emulator_ready(appium_name):
                    if not self.ld_manager.check_and_force_root(appium_name):
                        self.update_ld_signal.emit(self.ld_name, "❌ Root failed")
                        return

            # 🟢 CONNECT APPIUM
            driver, bot = self.ld_manager.connect_to_ldplayer(self.ld_name, appium_name)
            if not driver or not bot:
                self.update_ld_signal.emit(self.ld_name, "⚠️ Appium connection failed")
                return

            # 🟢 PROCESS ACCOUNTS ONE BY ONE
            while self.is_running and not self.queue.empty():
                acc_id = None
                try:
                    acc_id = self.queue.get_nowait()
                    self.current_acc_id = acc_id
                    self.account_started_signal.emit(str(acc_id))
                    self.update_acc_signal.emit(acc_id, False, {"status": "⚡ Starting..."})
                except queue.Empty:
                    break
                    
                # 🟢 INNER TRY-CATCH: Skips failing accounts safely
                try:
                    if self.stop_events[acc_id].is_set():
                        continue 

                    data_acc = self.account_cache.get_by_id(acc_id)

                    raw_phone = data_acc.get("phone_number", [])
                    mobile_no = str(raw_phone[0]) if isinstance(raw_phone, list) and len(raw_phone) > 0 else (raw_phone if isinstance(raw_phone, str) else "")
                    
                    data_device = {
                        "manufacturer": data_acc.get("manufacturer", ""),
                        "model": data_acc.get("model", ""),
                        "market_name": data_acc.get("market_name", ""),
                        "android_id": data_acc.get("android_id", ""),
                        "serial_number": data_acc.get("serial_number", ""),
                        "hardware": data_acc.get("hardware", ""),
                        "board": data_acc.get("board", ""),
                        "bootloader": data_acc.get("bootloader", ""),
                        "build_fingerprint": data_acc.get("build_fingerprint", ""),
                        "imei": data_acc.get("imei", ""),
                        "meid": data_acc.get("meid", ""),
                        "gsf_id": data_acc.get("gsf_id", ""),
                        "advertising_id": data_acc.get("advertising_id", ""),
                        "mac": data_acc.get("mac", ""),
                        "bluetooth_mac": data_acc.get("bluetooth_mac", ""),
                        "wifi_ssid": data_acc.get("wifi_ssid", ""),
                        "wifi_bssid": data_acc.get("wifi_bssid", ""),
                        "network_generation": data_acc.get("network_generation", "13"),
                        "imsi": data_acc.get("imsi", ""),
                        "simid": data_acc.get("simid", ""),
                        "mobile_no": mobile_no, 
                        "esim_eid": data_acc.get("esim_eid", ""),
                        "sim_operator": data_acc.get("sim_operator", ""),
                        "sim_operator_name": data_acc.get("sim_operator_name", ""),
                        "sim_country_iso": data_acc.get("sim_country_iso", ""),
                        "timezone": data_acc.get("time_zone", ""), 
                        "latitude": data_acc.get("gps", {}).get("lat", ""),
                        "longitude": data_acc.get("gps", {}).get("long", "")
                    }

                    # Push Identity Payload
                    payload_content = "\n".join([f"{k}={v}" for k, v in data_device.items() if v])                            
                    self.ld_manager.push_farm_profile(appium_name, payload_content)
                    self.ld_manager.force_stop_app(appium_name, "com.facebook.katana")
                    self.ld_manager.force_stop_app(appium_name, "com.example.spfarmchanger")

                    # Restore Device
                    raw_backup_path = data_acc.get("backup_file_name")
                    if raw_backup_path and os.path.exists(os.path.normpath(str(raw_backup_path).strip())):
                        backup_file_name = os.path.normpath(str(raw_backup_path).strip())
                        self.update_ld_signal.emit(self.ld_name, "🔄 Restoring device data...")
                        
                        if not self.ld_manager.restore_full_device_with_identity(appium_name, backup_file_name):
                            self.update_acc_signal.emit(acc_id, True, {"status": "❌ Restore Failed"})
                            continue
                    else:
                        self.update_acc_signal.emit(acc_id, True, {"status": "❌ Restore Error (File missing)"})
                        continue

                    if self.stop_events[acc_id].is_set():
                        continue

                    # Execute Requested Actions
                    if self.actions is None:
                        bot.open_app("com.facebook.katana")
                        self.update_ld_signal.emit(self.ld_name, "✅ Ready! Emulator left open for manual usage.")
                        self.update_acc_signal.emit(acc_id, True, {
                            "status": f"✅ Opened Manually ({self.ld_name})",
                            "last_date": self.general_function.current_date_time()
                        })
                        if driver:
                            driver.quit()
                            driver = None
                            
                        self.manual_idle_ready = True # 🟢 FIX: Safe to enter idle loop now!
                        break # Break loop immediately so LD stays open

                    elif self.actions == "get_user_ids":
                        uid = self.general_function.get_uid_in_background(appium_name)
                        status_msg = "✅ UID Success" if uid else "❌ UID Failed"
                        self.update_acc_signal.emit(acc_id, True, {
                            "uid": uid, "status": status_msg,
                            "last_date": self.general_function.current_date_time()
                        })

                    elif self.actions == "scrape_group":
                        bot.open_app("com.facebook.katana")
                        bot.wait(6)
                        dynamic_tabs, tab_bar_xpaths = self.active_tab_controller.get_dynamic_tab(bot, self.update_ld_signal, self.ld_name)
                        
                        if not dynamic_tabs:
                            self.update_acc_signal.emit(acc_id, True, {
                                "status": tab_bar_xpaths,
                                "last_date": self.general_function.current_date_time()
                            })
                            continue
                            
                        success, reason = self.active_tab_controller.extract_and_save_groups(acc_id, self.ld_name, appium_name, bot, self.update_acc_signal, self.update_ld_signal, dynamic_tabs, tab_bar_xpaths, self.stop_events[acc_id])
                        self.update_acc_signal.emit(acc_id, True, {
                            "status": reason,
                            "last_date": self.general_function.current_date_time()
                        })

                except Exception as e:
                    self.update_acc_signal.emit(acc_id, True, {"status": f"❌ Error: {str(e)[:40]}"})

                finally:
                    if acc_id:
                        if self.stop_events[acc_id].is_set():
                            self.update_acc_signal.emit(acc_id, True, {"status": "🛑 Stopped"})
                        
                        self.queue.task_done()
                        self.account_finished_signal.emit(str(acc_id)) # 🟢 Update the UI progress!

        except Exception as fatal_e:
            self.update_ld_signal.emit(self.ld_name, "❌ Fatal Thread Error")
            print(f"Fatal error in {self.ld_name}: {fatal_e}")

        finally:
            # 🟢 FIX: MANUAL IDLE LOOP (Only trigger if boot & load was successful)
            if self.actions is None and self.manual_idle_ready and self.is_running:
                while self.is_running:
                    time.sleep(1) # Uses 0% CPU, waits for user to click Stop
                self.update_ld_signal.emit(self.ld_name, "🛑 Closing Manual LD...")

            # 🟢 SAFE CLEANUP
            if driver:
                try:
                    driver.quit()
                except: pass
                
            if self.ld_manager.is_ld_running(self.ld_name):
                try:
                    self.ld_manager.close_ld(self.ld_name)
                    self.update_ld_signal.emit(self.ld_name, "✅ Closed")
                except Exception as e:
                    print(f"❌ Failed to close {self.ld_name}: {e}")

