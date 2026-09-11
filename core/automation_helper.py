import subprocess
import time
import sys
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import threading
import random

# Import your server manager safely
from core.appium_manager import AppiumServerManager

class AppiumHelper:
    _repair_lock = threading.Lock()

    def __init__(self, driver, ld_name, reconnect_callback=None):
        self.driver = driver
        self.ld_name = ld_name
        self.automation_delay = 1
        self.reconnect_callback = reconnect_callback 
        self.size = self.driver.get_window_size() # Caching the size here!

    # ---------------------------------------------------------
    # Self-Healing & Crash Recovery Core
    # ---------------------------------------------------------
    def is_session_alive(self):
        try:
            self.driver.current_package
            return True
        except Exception:
            return False

    def handle_fatal_crash(self):
        print(f"🚨 [Fatal Connection Lost] on {self.ld_name}. Initiating self-repair...")
        try:
            self.driver.quit()
        except:
            pass

        with self._repair_lock:
            if not AppiumServerManager.is_running():
                print(f"☠️ [{self.ld_name}] Appium Server is dead. Restarting it globally...")
                AppiumServerManager.stop_server()
                time.sleep(2)
                AppiumServerManager.start_server()
                time.sleep(5) 
            else:
                print(f"⚡ [{self.ld_name}] Appium Server is alive. Isolated emulator crash detected.")

        time.sleep(random.uniform(2.0, 5.0)) 

        if self.reconnect_callback:
            print(f"🔄 [{self.ld_name}] Attempting to re-establish Appium session...")
            new_driver = self.reconnect_callback(self.ld_name)
            if new_driver:
                self.driver = new_driver
                # Refresh the cached size for the new driver session
                self.size = self.driver.get_window_size()
                print(f"✅ [{self.ld_name}] Driver successfully healed and reconnected!")
                return True
                
        return False

    def recover_system_environment(self):
        print("🛑 Force closing Appium Server...")
        AppiumServerManager.stop_server()
        
        print("🧹 Cleaning up old ADB connections...")
        try:
            subprocess.run(["adb", "kill-server"], check=True, capture_output=True)
            subprocess.run(["adb", "start-server"], check=True, capture_output=True)
            print("✅ ADB Server fresh and ready.")
            time.sleep(5) 
        except FileNotFoundError:
            print("⚠️ ADB not found in system PATH. Skipping ADB reset.")

        print("🚀 Restarting Appium Server...")
        AppiumServerManager.start_server()
        time.sleep(3)
    
    def is_fatal_error(self, e):
        err_str = str(e).lower()
        fatal_keywords = [
            "10054", "10061", "actively refused it", "connection aborted", 
            "max retries exceeded", "econnreset", "remote server", 
            "socket hang up", "invalid session", "invalidsessionidexception", 
            "terminated or not started", "instrumentation process", "httpconnectionpool"
        ]
        return any(err in err_str for err in fatal_keywords)

    # ---------------------------------------------------------
    # Internal Base Handlers
    # ---------------------------------------------------------
    def _find(self, by, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )
        except TimeoutException:
            raise  
        except WebDriverException as wde:
            err_str = str(wde).lower()
            if "econnreset" in err_str or "remote server" in err_str or "socket hang up" in err_str:
                if self.handle_fatal_crash():
                    return self._find(by, locator, timeout)
            raise wde

    def _click(self, by, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
            element.click()
            return True
        except TimeoutException:
            return False
        except WebDriverException as wde:
            err_str = str(wde).lower()
            if "econnreset" in err_str or "remote server" in err_str or "socket hang up" in err_str:
                print(f"🚨 Connection lost during click ({locator})! Repairing...")
                if self.handle_fatal_crash():
                    return self._click(by, locator, timeout)
                return False
            return False
        except Exception as e:
            print(f"❌ Click error ({locator}) : {e}")
            return False
        
    def exists_xpath(self, xpath, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False
        except Exception as e: 
            if self.is_fatal_error(e):
                print(f"🚨 Connection totally lost checking exists_xpath! Repairing...")
                if self.handle_fatal_crash():
                    return self.exists_xpath(xpath, timeout)
            return False

    def find_elements(self, xpath, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((AppiumBy.XPATH, xpath))
            )
        except TimeoutException:
            return []
        except Exception as e: 
            if self.is_fatal_error(e):
                print(f"🚨 Connection lost while finding elements ({xpath})! Repairing...")
                if self.handle_fatal_crash():
                    return self.find_elements(xpath, timeout)
            return []

    # 🟢 OPTIMIZED wait_any: Bypasses WebDriverWait to prevent Appium Server DDOS
    def wait_any(self, locators, timeout=60):
        end = time.time() + timeout
        # Temporarily disable implicit waits so find_elements returns instantly if not found
        self.driver.implicitly_wait(0) 
        
        while time.time() < end:
            try:
                for xpath in locators:
                    if len(self.driver.find_elements(AppiumBy.XPATH, xpath)) > 0:
                        return xpath
                # Crucial breathing delay to prevent emulator CPU spikes
                time.sleep(1.5) 
            except Exception as e:
                if self.is_fatal_error(e):
                    if self.handle_fatal_crash():
                        continue 
                return None
        return None

    # ---------------------------------------------------------
    # Specialized System Click (Bypasses Blocks)
    # ---------------------------------------------------------
    def safe_system_click(self, xpath, timeout=5):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            rect = element.rect
            center_x = rect['x'] + (rect['width'] // 2)
            center_y = rect['y'] + (rect['height'] // 2)
            
            print(f"🖱️ Bypassing Appium: ADB Tapping system button at {center_x}, {center_y}")
            
            udid = self.driver.capabilities.get('udid', self.driver.capabilities.get('appium:udid', self.ld_name))
            cmd = f"adb -s {udid} shell input tap {center_x} {center_y}"
            subprocess.run(cmd, shell=True)
            return True
            
        except WebDriverException as wde:
            print(f"❌ Safe system click hit a communication crash: {wde}")
            if "ECONNRESET" in str(wde) or "remote server" in str(wde).lower():
                if self.handle_fatal_crash():
                    return self.safe_system_click(xpath, timeout)
            return False
        except Exception as e:
            print(f"⚠️ Safe click structural exception for {xpath}: {e}")
            return False

    # ---------------------------------------------------------
    # Standard Click Targets
    # ---------------------------------------------------------
    def click_id(self, resource_id, timeout=10):
        return self._click(AppiumBy.ID, resource_id, timeout)

    # 🟢 OPTIMIZED: Native UIAutomator replaces crash-heavy wildcard XPath
    def click_text(self, text, timeout=10):
        ui_selector = f'new UiSelector().text("{text}")'
        return self._click(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector, timeout)

    def click_acc(self, content_desc, timeout=10):
        return self._click(AppiumBy.ACCESSIBILITY_ID, content_desc, timeout)

    def click_xpath(self, xpath, timeout=10):
        return self._click(AppiumBy.XPATH, xpath, timeout)

    def click_ui(self, ui_selector, timeout=10):
        return self._click(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector, timeout)
    
    def click_child(self, parent_xpath, child_xpath, timeout=10):
        try:
            parent = self._find(AppiumBy.XPATH, parent_xpath, timeout)
            parent.find_element(AppiumBy.XPATH, child_xpath).click()
            return True
        except Exception as e:
            print(f"❌ Click child failed: {e}")
            return False
        
    def exists_ui(self, ui_selector, timeout=2):
        """Native Android fast-check for element existence."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, ui_selector))
            )
            return True
        except TimeoutException:
            return False
        except WebDriverException as wde:
            err_str = str(wde).lower()
            if "econnreset" in err_str or "remote server" in err_str or "socket hang up" in err_str:
                self.handle_fatal_crash()
            return False
    

    # ---------------------------------------------------------
    # Standard Find Targets
    # ---------------------------------------------------------
    def find_id(self, resource_id, timeout=10):
        return self._find(AppiumBy.ID, resource_id, timeout)

    # 🟢 OPTIMIZED: Native UIAutomator search
    def find_text(self, text, timeout=10):
        ui_selector = f'new UiSelector().text("{text}")'
        return self._find(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector, timeout)

    def find_acc(self, content_desc, timeout=10):
        return self._find(AppiumBy.ACCESSIBILITY_ID, content_desc, timeout)

    def find_xpath(self, xpath, timeout=10):
        return self._find(AppiumBy.XPATH, xpath, timeout)
    
    # ---------------------------------------------------------
    # Text Input Target Handlers
    # ---------------------------------------------------------
    def _type(self, by, locator, value, timeout=10):
        try:
            element = self._find(by, locator, timeout)
            element.click()
            try:
                element.clear()
            except:
                pass
            element.send_keys(value)
            return True
        except Exception as e:
            print(f"❌ Typing interaction failed on ({locator}): {e}")
            return False
    def _type_not_clear(self, by, locator, value, timeout=10):
        try:
            element = self._find(by, locator, timeout)
            element.click()
            element.send_keys(value)
            return True
        except Exception as e:
            print(f"❌ Typing interaction failed on ({locator}): {e}")
            return False

    def type_id(self, resource_id, value, timeout=10):
        return self._type(AppiumBy.ID, resource_id, value, timeout)

    def type_xpath(self, xpath, value, timeout=10):
        return self._type(AppiumBy.XPATH, xpath, value, timeout)

    # 🟢 OPTIMIZED: Native UIAutomator input
    def type_text(self, text, value, timeout=10):
        ui_selector = f'new UiSelector().text("{text}")'
        return self._type(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector, value, timeout)

    def type_acc(self, content_desc, value, timeout=10):
        return self._type(AppiumBy.ACCESSIBILITY_ID, content_desc, value, timeout)

    def type_class(self, class_name, value, timeout=10):
        return self._type(AppiumBy.CLASS_NAME, class_name, value, timeout)

    def type_ui(self, ui_selector, value, timeout=10):
        return self._type(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector, value, timeout)
    
    def press_enter(self):
        self.driver.press_keycode(66)
        self.wait(1)


        


    
    def type_text_human_like(self, xpath, text, timeout=10):
        try:
            element = self._find(AppiumBy.XPATH, xpath, timeout)
            element.click()
     
            for char in text:
                element.send_keys(char) 
                time.sleep(random.uniform(0.1, 0.3))

            self.press_enter()
                
            return True
        except Exception as e:
            print(f"❌ Human-like({xpath}): {e}")
            return False
        
    def clear_text(self, xpath, timeout=10):
        try:
            element = self._find(AppiumBy.XPATH, xpath, timeout)
            element.click()
            element.clear()
            return True
        except Exception as e:
            return False

    def tap(self, x, y):
        try:
            self.driver.w3c_actions = None 
            actions = ActionChains(self.driver)
            touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
            actions.w3c_actions = ActionBuilder(self.driver, mouse=touch_input)
            
            actions.w3c_actions.pointer_action.move_to_location(int(x), int(y))
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1) 
            actions.w3c_actions.pointer_action.pointer_up()
            
            actions.perform()
            return True

        except WebDriverException as wde:
            print(f"❌ Action chain tap failed at ({x}, {y}) due to connection issue: {wde}")
            udid = self.driver.capabilities.get('udid', self.driver.capabilities.get('appium:udid', self.ld_name))
            try:
                subprocess.run(f"adb -s {udid} shell input tap {x} {y}", shell=True)
                return True
            except:
                if "ECONNRESET" in str(wde) or "remote server" in str(wde).lower():
                    if self.handle_fatal_crash():
                        return self.tap(x, y)
                return False
        except Exception as e:
            print(f"❌ General tap error: {e}")
            return False

    def tap_top_center(self, offset_y=50):
        try:
            x = self.size['width'] // 2
            return self.tap(x, offset_y)
        except Exception as e:
            print(f"❌ Top-center tap failed: {e}")
            return False
        
    def tap_top_right(self, offset_x=50, offset_y=50):
        try:
            x = self.size['width'] - offset_x 
            return self.tap(x, offset_y)
        except Exception as e:
            print(f"❌ Top-right tap failed: {e}")
            return False

    def click_bottom_center(self):
        self.tap(self.size['width'] // 2, int(self.size['height'] * 0.9))
        print("click bottom center tag")
        self.wait(1.5)

    def tap_percentage(self, x_percent, y_percent):
        try:
            x_pixel = int(self.size['width'] * (x_percent / 100.0))
            y_pixel = int(self.size['height'] * (y_percent / 100.0))
            return self.tap(x_pixel, y_pixel)
        except Exception as e:
            print(f"❌ tap_percentage: {e}")
            return False

    def dynamic_tap_tab_bar(self, target_tab_index, total_tabs=6):
        try:
            anchor_xpaths = [
                '//android.view.View[contains(@content-desc, "tab 1 of")]',
                '//android.view.View[contains(@content-desc, "tab 3 of")]',
                '//android.view.View[contains(@content-desc, "tab 2 of")]',
                '//android.view.View[contains(@content-desc, "tab 4 of")]',
                '//android.view.View[contains(@content-desc, "tab 5 of")]',
                '//android.view.View[contains(@content-desc, "tab 6 of")]' 
            ]
            
            target_y = None
            for xpath in anchor_xpaths:
                elements = self.driver.find_elements(AppiumBy.XPATH, xpath)
                if elements:
                    rect = elements[0].rect
                    target_y = int(rect['y'] + (rect['height'] / 2))
                    break
                    
            if not target_y:
                target_y = int(self.size['height'] * 0.12) 
                
            tab_width = self.size['width'] // total_tabs
            target_x = int((tab_width * (target_tab_index - 1)) + (tab_width / 2))
        
            return self.tap(target_x, target_y)
            
        except Exception as e:
            print(f"❌ Dynamic tab tap failed: {e}")
            return False

    def swipe(self, sx, sy, ex, ey, speed_ms=900):
        try:
            self.driver.w3c_actions = None
            actions = ActionChains(self.driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            
            actions.w3c_actions = ActionBuilder(self.driver, mouse=finger)
            
            actions.w3c_actions.pointer_action.move_to_location(int(sx), int(sy))
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.2)
            actions.w3c_actions.pointer_action.move_to_location(int(ex), int(ey))
            actions.w3c_actions.pointer_action.pointer_up() 

            actions.perform()
            return True

        except Exception as e:
            err_str = str(e).lower()
            if "10054" in err_str or "connection aborted" in err_str or "max retries exceeded" in err_str or "econnreset" in err_str or "remote server" in err_str or "socket hang up" in err_str or "invalid session" in err_str:
                print(f"🚨 Connection lost during swipe! Repairing...")
                if self.handle_fatal_crash():
                    return self.swipe(sx, sy, ex, ey, speed_ms)
                return False
                
            if not self.is_session_alive():
                print("🕵️ Ghost crash detected during swipe! Repairing...")
                if self.handle_fatal_crash():
                    return self.swipe(sx, sy, ex, ey, speed_ms)
                return False
                
            print(f"❌ Swipe failed: {e}")
            return False

    def pull_to_refresh(self):
        self.swipe(500, 300, 500, 1800, speed_ms=1800)
        self.wait(1) 
    
    def swipe_element(self, element, direction="up", times=1, delay=0.5, speed_ms=1000):
        rect = element.rect
        x = rect["x"] + rect["width"] / 2
        y_start = rect["y"] + (rect["height"] * 0.7) 
        y_end = rect["y"] + (rect["height"] * 0.3)   

        for _ in range(times):
            if direction == "up":
                self.swipe(x, y_start, x, y_end, speed_ms)
            else:
                self.swipe(x, y_end, x, y_start, speed_ms)
            time.sleep(delay)

    def scroll_down(self, speed_ms=1000):
        try:
            size = self.size
            center_x = size['width'] // 2
            start_y = int(size['height'] * 0.70)
            end_y = int(size['height'] * 0.30)
            
            return self.swipe(center_x, start_y, center_x, end_y, speed_ms)
        except Exception as e:
            print(f"❌ Scroll down failed: {e}")
            return False

    def scroll_up(self, speed_ms=1000):
        try:
            size = self.size
            center_x = size['width'] // 2
            start_y = int(size['height'] * 0.30)
            end_y = int(size['height'] * 0.65)
            
            return self.swipe(center_x, start_y, center_x, end_y, speed_ms)
        except Exception as e:
            print(f"❌ Scroll up failed: {e}")
            return False

    def press_back(self):
        self.driver.back()

    def press_home(self):
        self.driver.press_keycode(3)

    def open_app(self, package_name):
        try:
            # 1. Check if the app is even installed
            if not self.driver.is_app_installed(package_name):
                return False, f"No app {package_name} installed"

            # 2. Attempt to activate using standard Appium method
            try:
                self.driver.activate_app(package_name)
            except Exception:
                self.driver.execute_script('mobile: shell', {
                    'command': 'monkey',
                    'args': ['-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1']
                })
            
            return True, "Success"
        
        except Exception as e:
            error_msg = str(e)
            print(f"❌ App launch failed for {package_name}: {error_msg}")
            
            if "not installed" in error_msg.lower():
                return False, "No app installed"
            return False, "Launch failed"

    def wait(self, seconds):
        time.sleep(seconds * self.automation_delay)

    def get_text_xpath(self, xpath, timeout=10):
        element = self.find_xpath(xpath, timeout)
        return element.get_attribute("text")
    
    def hide_keyboard(self):
        try:
            self.driver.hide_keyboard()
            time.sleep(0.5) 
            return True
        except Exception as e:
            err_str = str(e).lower()
            if "not present" in err_str or "not shown" in err_str or "keyboard" in err_str:
                return True
            if "econnreset" in err_str or "remote server" in err_str or "socket hang up" in err_str or "invalid session" in err_str:
                print("🚨 Connection lost while trying to hide keyboard! Repairing...")
                if self.handle_fatal_crash():
                    return self.hide_keyboard()
                return False
            if not self.is_session_alive():
                print("🕵️ Ghost crash detected while hiding keyboard! Repairing...")
                if self.handle_fatal_crash():
                    return self.hide_keyboard()
                return False
            try:
                self.driver.press_keycode(4)
                time.sleep(0.5)
                return True
            except:
                return False

    def clear_xpath(self, xpath, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            element.click() 
            element.clear()
            return True
        except TimeoutException:
            if not self.is_session_alive():
                if self.handle_fatal_crash():
                    return self.clear_xpath(xpath, timeout)
            return False
        except Exception as e:
            err_str = str(e).lower()
            if "econnreset" in err_str or "remote server" in err_str or "socket hang up" in err_str or "invalid session" in err_str:
                print(f"🚨 Connection lost while trying to clear text ({xpath})! Repairing...")
                if self.handle_fatal_crash():
                    return self.clear_xpath(xpath, timeout)
                return False
            if not self.is_session_alive():
                print(f"🕵️ Ghost crash detected during text clear ({xpath})! Repairing...")
                if self.handle_fatal_crash():
                    return self.clear_xpath(xpath, timeout)
                return False
            print(f"❌ Failed to clear element ({xpath}): {e}")
            return False
        
    def press_backspace(self, count=1):

        try:
            for _ in range(count):
                self.driver.press_keycode(67) 
                time.sleep(random.uniform(0.05, 0.15)) # Fast human tapping speed
            return True
        except Exception as e:
            print(f"⚠️ Failed to press Backspace: {e}")
            return False
    # ---------------------------------------------------------
    # Facebook Specific Helpers
    # ---------------------------------------------------------
    def long_press(self, x, y, duration_ms=1500):
        """Simulates a long press. Falls back to ADB if Appium's W3C chain crashes."""
        try:
            # 1. Try standard W3C Action Chain
            self.driver.w3c_actions = None
            actions = ActionChains(self.driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            
            actions.w3c_actions = ActionBuilder(self.driver, mouse=finger)
            actions.w3c_actions.pointer_action.move_to_location(int(x), int(y))
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration_ms / 1000.0) 
            actions.w3c_actions.pointer_action.pointer_up() 

            actions.perform()
            return True

        except Exception as e:
            # 2. 🟢 THE FIX: If W3C crashes, bypass Appium and use native ADB!
            print(f"⚠️ W3C Long press failed. Using native ADB fallback at ({x}, {y})...")
            try:
                udid = self.driver.capabilities.get('udid', self.driver.capabilities.get('appium:udid', self.ld_name))
                # In ADB, a long press is a swipe that starts and ends at the exact same pixel, lasting 1.5 seconds.
                cmd = f"adb -s {udid} shell input swipe {int(x)} {int(y)} {int(x)} {int(y)} {duration_ms}"
                import subprocess
                subprocess.run(cmd, shell=True, check=True)
                return True
            except Exception as adb_e:
                print(f"❌ Both W3C and ADB long press failed: {adb_e}")
                return False

    def react_to_post(self, reaction_type="Like"):
        """Specialized lightning-fast reaction handler for Standard Feed Posts."""
        
        # 🟢 Universal XPath: Catches the button regardless of current emoji state
        universal_reaction_xpath = (
            '//*['
            'contains(@content-desc, "Like button") or '
            'contains(@content-desc, "Love button") or '
            'contains(@content-desc, "Care button") or '
            'contains(@content-desc, "Haha button") or '
            'contains(@content-desc, "Wow button") or '
            'contains(@content-desc, "Sad button") or '
            'contains(@content-desc, "Angry button") or '
            'contains(@text, "Like button")'
            ']'
        )
        
        try:
            # Search for the button once
            elements = self.find_elements(universal_reaction_xpath, timeout=2)
            
            if not elements:
                return False 

            btn_element = elements[0]

            # 🟢 If standard Like, just click the element we already found!
            if reaction_type == "Like":
                btn_element.click()
                return True

            # 🟢 For other reactions, calculate coordinates and Long Press
            rect = btn_element.rect
            btn_x = int(rect["x"] + rect["width"] / 2)
            btn_y = int(rect["y"] + rect["height"] / 2)
            
            self.long_press(btn_x, btn_y, duration_ms=1500)
            self.wait(1.5) 
            
            # 🟢 Look for the specific Emoji in the popup tray
            reaction_ui_selector = f'new UiSelector().descriptionContains("{reaction_type}")'
            
            if self.exists_ui(reaction_ui_selector, timeout=2):
                self.click_ui(reaction_ui_selector)
                return True
            else:
                # print(f"⚠️ Could not find '{reaction_type}' icon, falling back to normal like.")
                if self.exists_ui('new UiSelector().descriptionContains("Care")', timeout=2):
                    self.click_ui('new UiSelector().descriptionContains("Care")')
                    return True
                else:
                    # If the popup completely failed to appear, fallback to standard click
                    self.press_back()
                    btn_element.click()
                return True
                
        except Exception as e:
            print(f"❌ Reaction '{reaction_type}' failed: {e}")
            return False

    def safe_click_tab(self, tab_xpath, target_tab_index, total_tabs=6):
        if self.exists_xpath(tab_xpath, timeout=3):
            return self.click_xpath(tab_xpath)
        else:
            print(f"🔄 XPath failed for Tab {target_tab_index}. Using dynamic mathematical fallback...")
            return self.dynamic_tap_tab_bar(target_tab_index=target_tab_index, total_tabs=total_tabs)
        
    def react_to_reel(self, reaction_type="Like"):
        """Specialized reaction handler for Full-Screen Reels/Videos."""
        
        # 🟢 Universal XPath: Catches the button regardless of extra text or current emoji state
        universal_reaction_xpath = (
            '//android.view.ViewGroup['
            'contains(@content-desc, "Like button") or '
            'contains(@content-desc, "Love button") or '
            'contains(@content-desc, "Care button") or '
            'contains(@content-desc, "Haha button") or '
            'contains(@content-desc, "Wow button") or '
            'contains(@content-desc, "Sad button") or '
            'contains(@content-desc, "Angry button")'
            ']'
        )
        
        try:
            # Search for the button once
            elements = self.find_elements(universal_reaction_xpath, timeout=2)
            
            if not elements:
                print("⚠️ Reels Like/Reaction button not found.")
                return False 
                
            btn_element = elements[0]

            # 🟢 If standard Like, just click the element we already found!
            if reaction_type == "Like":
                btn_element.click()
                return True

            # 🟢 For other reactions, calculate coordinates and Long Press
            rect = btn_element.rect
            btn_x = int(rect["x"] + rect["width"] / 2)
            btn_y = int(rect["y"] + rect["height"] / 2)
            
            self.long_press(btn_x, btn_y, duration_ms=1500)
            self.wait(1.5) 
            
            # 🟢 Look for the specific Emoji in the popup tray
            reaction_ui_selector = f'new UiSelector().descriptionContains("{reaction_type}")'
            
            if self.exists_ui(reaction_ui_selector, timeout=2):
                self.click_ui(reaction_ui_selector)
                return True
            else:
                # print(f"⚠️ Could not find '{reaction_type}' popup. Tapping Care instead.")
                if self.exists_ui('new UiSelector().descriptionContains("Care")', timeout=2):
                    self.click_ui('new UiSelector().descriptionContains("Care")')
                    return True
                else:
                    # If the popup completely failed to appear, fallback to standard click
                    self.press_back()
                    btn_element.click()
                return True
                
        except Exception as e:
            print(f"❌ Reel Reaction '{reaction_type}' failed: {e}")
            return False 

    
    def react_to_story(self, target_index):
        love_reaction_xpath = '//android.view.ViewGroup[@content-desc="Love Reaction"]'

        index_to_xpath = {
            0: '//android.view.ViewGroup[@content-desc="Like Reaction"]',
            1: '//android.view.ViewGroup[@content-desc="Love Reaction"]',
            2: '//android.view.ViewGroup[@content-desc="Care Reaction"]',
            3: '//android.view.ViewGroup[@content-desc="Haha Reaction"]',
            4: '//android.view.ViewGroup[@content-desc="Wow Reaction"]',
            5: '//android.view.ViewGroup[@content-desc="Sad Reaction"]',
            6: '//android.view.ViewGroup[@content-desc="Angry Reaction"]'
        }
        
        target_xpath = index_to_xpath.get(target_index, index_to_xpath[0])

        try:
            # 3. VERIFY TRAY & AD-SAFETY
            love_btn = self.find_elements(love_reaction_xpath, timeout=0.5)
            if not love_btn:
                # self.press_back()
                return False

            # 4. SMART FALLBACK CHECK
            love_x = love_btn[0].rect['x']
            
            if love_x > (self.size['width'] * 0.50):
                if target_index == 0:
                    like_btn = self.find_elements(index_to_xpath[0], timeout=0.5)
                    if like_btn:
                        lx = like_btn[0].rect['x'] + (like_btn[0].rect['width'] // 2)
                        ly = like_btn[0].rect['y'] + (like_btn[0].rect['height'] // 2)
                        self.tap(lx, ly)
                        self.tap(lx, ly)
                        self.tap(lx, ly)
                else:
                    lx = love_btn[0].rect['x'] + (love_btn[0].rect['width'] // 2)
                    ly = love_btn[0].rect['y'] + (love_btn[0].rect['height'] // 2)
                    self.tap(lx, ly)
                    self.tap(lx, ly)
                    self.tap(lx, ly)
                    
            else:
                print(f"🖱️ Sniping Emoji Index {target_index} normally via XPath.")
                if self.exists_xpath(target_xpath, timeout=2):
                    self.click_xpath(target_xpath)
                else:
                    print(f"⚠️ Emoji XPath not found after swipe.")
                    return False
            return True
            
        except Exception as e:
            print(f"❌ Story reaction failed: {e}")
            return False


    # ---------------------------------------------------------
    # SMART NAVIGATION & SCREEN HELPERS
    # ---------------------------------------------------------
    def nudge_element_into_view(self, element, threshold_ratio=0.80):
        """
        Checks if an element is too far down the screen. If it is, it nudges the screen up slightly.
        Useful for buttons that are partially cut off by the bottom of the emulator.
        """
        try:
            h = self.size['height']
            w = self.size['width']
            rect = element.rect
            el_y = rect['y'] + (rect['height'] // 2)
            
            if el_y > (h * threshold_ratio):
                # Swipe up slightly
                self.swipe(w // 2, h * 0.60, w // 2, h * 0.40, speed_ms=800)
                self.wait(1.5)
                return True
        except Exception:
            pass 
        return False

    def menu_search_fallback(self, search_text, search_btn_xpath, search_input_xpath):
        """
        Universal fallback: Clicks search, calculates dropdown bounds safely before typing, 
        types the text, hides keyboard, and clicks the first dropdown result.
        """
        if self.exists_xpath(search_btn_xpath, timeout=3):
            self.click_xpath(search_btn_xpath)
            self.wait(2)

            if self.exists_xpath(search_input_xpath):
                # 1. FIND BOUNDS FIRST (Before typing changes the text!)
                elements = self.find_elements(search_input_xpath, timeout=2) 
                if not elements:
                    return False
                    
                bounds = elements[0].get_attribute("bounds")
                if not bounds:
                    return False
                    
                # Calculate the target coordinates for the first dropdown result
                coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                if len(coords) == 4:
                    center_x = (coords[0] + coords[2]) // 2
                    bar_height = coords[3] - coords[1]
                    target_y = coords[3] + int(bar_height * 0.8)
                else:
                    return False

                # 2. TYPE THE TEXT
                self.type_xpath(search_input_xpath, search_text)
                self.press_backspace(1)
                self.wait(2)
                
                # 3. HIDE KEYBOARD
                self.press_back()
                self.wait(4.5) 
                
                # 4. TAP THE PRE-CALCULATED COORDINATES
                self.tap(center_x, target_y)
                self.wait(5) # Wait for page to change
                return True
                
        return False
















