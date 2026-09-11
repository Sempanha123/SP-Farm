from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions import interaction
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions.mouse_button import MouseButton

class AppiumHelper:

    def __init__(self, driver, ld_name):
        self.driver = driver
        self.ld_name = ld_name
        self.automation_delay = 1

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _find(self, by, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def _click(self, by, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, locator))
            )
            element.click()
            return True

        except Exception as e:
            print(f"❌ Click failed ({locator}) : {e}")
            return False
        
    def exists_xpath(self, xpath, timeout=2):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((AppiumBy.XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False

    def wait_any(self, locators, timeout=60):
        end = time.time() + timeout

        while time.time() < end:
            for xpath in locators:
                
                if self.exists_xpath(xpath, timeout=0.2):
                    
                    return xpath

            time.sleep(0.2)

        return None
    # ---------------------------------------------------------
    # Click
    # ---------------------------------------------------------

    def click_id(self, resource_id, timeout=10):
        """
        Example:
        helper.click_id("com.lexa.fakegps:id/menu_goto_location")
        """
        return self._click(AppiumBy.ID, resource_id, timeout)

    def click_text(self, text, timeout=10):
        """
        Example:
        helper.click_text("Go to")
        """
        xpath = f"//*[@text='{text}']"
        return self._click(AppiumBy.XPATH, xpath, timeout)

    def click_acc(self, content_desc, timeout=10):
        """
        Example:
        helper.click_acc("Open navigation drawer")
        """
        return self._click(AppiumBy.ACCESSIBILITY_ID, content_desc, timeout)

    def click_xpath(self, xpath, timeout=10):
        """
        Example:
        helper.click_xpath("//android.widget.CheckedTextView[@text='Go to']")
        """
        return self._click(AppiumBy.XPATH, xpath, timeout)

    def click_ui(self, ui_selector, timeout=10):
        """
        Example:
        helper.click_ui('new UiSelector().text("Go to")')
        """
        return self._click(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector, timeout)
    
    def click_child(self, parent_xpath, child_xpath, timeout=10):
        parent = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((AppiumBy.XPATH, parent_xpath))
        )
        parent.find_element(AppiumBy.XPATH, child_xpath).click()

    # ---------------------------------------------------------
    # Find
    # ---------------------------------------------------------

    def find_id(self, resource_id, timeout=10):
        return self._find(AppiumBy.ID, resource_id, timeout)

    def find_text(self, text, timeout=10):
        return self._find(
            AppiumBy.XPATH,
            f"//*[@text='{text}']",
            timeout
        )

    def find_acc(self, content_desc, timeout=10):
        return self._find(
            AppiumBy.ACCESSIBILITY_ID,
            content_desc,
            timeout
        )

    def find_xpath(self, xpath, timeout=10):
        return self._find(
            AppiumBy.XPATH,
            xpath,
            timeout
        )

    # ---------------------------------------------------------
    # Internal
    # ---------------------------------------------------------

    def _type(self, by, locator, value, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

        element.click()

        try:
            element.clear()
        except:
            pass

        element.send_keys(value)

        return True

    # ---------------------------------------------------------
    # Input
    # ---------------------------------------------------------

    def type_id(self, resource_id, value, timeout=60):
        return self._type(AppiumBy.ID, resource_id, value, timeout)

    def type_xpath(self, xpath, value, timeout=60):
        return self._type(AppiumBy.XPATH, xpath, value, timeout)

    def type_text(self, text, value, timeout=60):
        xpath = f"//*[@text='{text}']"
        return self._type(AppiumBy.XPATH, xpath, value, timeout)

    def type_acc(self, content_desc, value, timeout=60):
        return self._type(AppiumBy.ACCESSIBILITY_ID, content_desc, value, timeout)

    def type_class(self, class_name, value, timeout=60):
        return self._type(AppiumBy.CLASS_NAME, class_name, value, timeout)

    def type_ui(self, ui_selector, value, timeout=60):
        return self._type(
            AppiumBy.ANDROID_UIAUTOMATOR,
            ui_selector,
            value,
            timeout
        )

    # ---------------------------------------------------------
    # Coordinate Tap
    # ---------------------------------------------------------

    def tap(self, x, y):
        try:
            actions = ActionChains(self.driver)
            
            # Use standard "touch" pointer
            touch_input = PointerInput(interaction.POINTER_TOUCH, "touch")
            actions.w3c_actions = ActionBuilder(self.driver, mouse=touch_input)
            
            actions.w3c_actions.pointer_action.move_to_location(int(x), int(y))
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1) 
            actions.w3c_actions.pointer_action.pointer_up()
            
            actions.perform()
            return True

        except Exception as e:
            print(f"❌ Tap failed: {e}")
            return False

    def tap_top_center(self, offset_y=50):
        """
        Taps the top-center of the screen.
        offset_y: How many pixels down from the very top to tap.
        """
        try:
            # 1. Get screen dimensions
            size = self.driver.get_window_size()
            width = size['width']
            
            # 2. Calculate center X and custom Y
            x = width // 2
            y = offset_y 
            
            # 3. Reuse your existing tap logic
            return self.tap(x, y)
            
        except Exception as e:
            print(f"❌ Top-center tap failed: {e}")
            return False
        
    def tap_top_right(self, offset_x=20, offset_y=20):
        """
        Taps the top-right of the screen (Useful for closing Ads).
        offset_x: How many pixels inward from the right edge to tap.
        offset_y: How many pixels down from the very top to tap.
        """
        try:
            # 1. Get screen dimensions
            size = self.driver.get_window_size()
            width = size['width']
            
            # 2. Calculate top-right X and custom Y
            # Total width minus the offset keeps it safely inside the screen
            x = width - offset_x 
            y = offset_y 
            
            # 3. Reuse your existing tap logic
            return self.tap(x, y)
            
        except Exception as e:
            print(f"❌ Top-right tap failed: {e}")
            return False

    # ---------------------------------------------------------
    # Android Actions
    # ---------------------------------------------------------

    def press_back(self):
        self.driver.back()

    def press_home(self):
        self.driver.press_keycode(3)

    def open_app(self, package_name):
        try:
            self.driver.activate_app(package_name)
            return True
        except Exception as e:
            print(e)
            return False
        

    def wait(self, seconds):
        time.sleep(seconds * self.automation_delay)

    def get_text_xpath(self, xpath, timeout=10):
        element = self.find_xpath(xpath, timeout)
        return element.get_attribute("text")
    
    def swipe(self, sx, sy, ex, ey):
        try:
            actions = ActionChains(self.driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            
            # 🟢 PASS DURATION HERE: 3000ms makes it a very slow, smooth scroll
            actions.w3c_actions = ActionBuilder(self.driver, mouse=finger, duration=600)

            actions.w3c_actions.pointer_action.move_to_location(int(sx), int(sy))
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.2)
            actions.w3c_actions.pointer_action.move_to_location(int(ex), int(ey))
            actions.w3c_actions.pointer_action.pointer_up() 

            actions.perform()
        except Exception as e:
            print(f"❌ Swipe failed: {e}")

    def pull_to_refresh(self):
        self.swipe(500, 500, 500, 1500)
        self.wait(2) # Give it time to load
    
    def swipe_element(self, element, direction="up", times=1, delay=0.3):
        rect = element.rect

        x = rect["x"] + rect["width"] / 2
        center = rect["y"] + rect["height"] / 2

        move = rect["height"] * 0.3

        for _ in range(times):
            if direction == "up":
                self.swipe(x, center + move, x, center - move)
            else:
                self.swipe(x, center - move, x, center + move)

            time.sleep(delay)