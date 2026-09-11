import os
import subprocess
import cv2
from PIL import Image
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QImage, QPixmap, QImageReader
from PySide6.QtWidgets import QWidget, QTableWidgetItem, QTableWidget, QComboBox, QLabel,QTableView, QStackedWidget
from PySide6.QtCore import QSortFilterProxyModel
from datetime import datetime
import subprocess
import re
import imaplib
import random
import re
import time
import requests
import random
import string

class GeneralFunction:

    def __init__(self):
        # ==========================================
        # 1. DETAILED DEVICE MODELS (Flagships + Mid-Range)
        # ==========================================
        self.device_models = [
            # --- Samsung Galaxy Series ---
            {"manufacturer": "samsung", "model": "SM-S928B", "product": "e3q", "market_name": "Galaxy S24 Ultra", "hardware": "qcom", "board": "kalama", "android_ver": "14", "build_tag": "UP1A.231005.007"},
            {"manufacturer": "samsung", "model": "SM-S918B", "product": "dm3q", "market_name": "Galaxy S23 Ultra", "hardware": "qcom", "board": "kalama", "android_ver": "13", "build_tag": "TP1A.220624.014"},
            {"manufacturer": "samsung", "model": "SM-S908B", "product": "b0q", "market_name": "Galaxy S22 Ultra", "hardware": "qcom", "board": "taro", "android_ver": "12", "build_tag": "SP1A.210812.016"},
            {"manufacturer": "samsung", "model": "SM-G998B", "product": "p3s", "market_name": "Galaxy S21 Ultra", "hardware": "exynos2100", "board": "exynos2100", "android_ver": "12", "build_tag": "SP1A.210812.016"},
            {"manufacturer": "samsung", "model": "SM-F946B", "product": "q5q", "market_name": "Galaxy Z Fold 5", "hardware": "qcom", "board": "kalama", "android_ver": "13", "build_tag": "TP1A.220624.014"},
            {"manufacturer": "samsung", "model": "SM-A546B", "product": "a54x", "market_name": "Galaxy A54 5G", "hardware": "exynos1380", "board": "s5e8835", "android_ver": "13", "build_tag": "TP1A.220624.014"},
            {"manufacturer": "samsung", "model": "SM-A146U", "product": "a14x", "market_name": "Galaxy A14 5G", "hardware": "mt6833", "board": "mt6833", "android_ver": "13", "build_tag": "TP1A.220624.014"},
            
            # --- Google Pixel Series ---
            {"manufacturer": "google", "model": "Pixel 8 Pro", "product": "husky", "market_name": "Pixel 8 Pro", "hardware": "gs301", "board": "husky", "android_ver": "14", "build_tag": "UD1A.230803.041"},
            {"manufacturer": "google", "model": "Pixel 8", "product": "shiba", "market_name": "Pixel 8", "hardware": "gs301", "board": "shiba", "android_ver": "14", "build_tag": "UD1A.230803.041"},
            {"manufacturer": "google", "model": "Pixel 7 Pro", "product": "cheetah", "market_name": "Pixel 7 Pro", "hardware": "gs201", "board": "cheetah", "android_ver": "13", "build_tag": "TQ3A.230605.012"},
            {"manufacturer": "google", "model": "Pixel 7a", "product": "lynx", "market_name": "Pixel 7a", "hardware": "gs201", "board": "lynx", "android_ver": "13", "build_tag": "TQ3A.230605.012"},
            {"manufacturer": "google", "model": "Pixel 6", "product": "oriole", "market_name": "Pixel 6", "hardware": "gs101", "board": "oriole", "android_ver": "12", "build_tag": "SQ3A.220705.004"},
            {"manufacturer": "google", "model": "Pixel 6a", "product": "bluejay", "market_name": "Pixel 6a", "hardware": "gs101", "board": "bluejay", "android_ver": "12", "build_tag": "SQ3A.220705.004"},

            # --- Xiaomi / Redmi / Poco ---
            {"manufacturer": "xiaomi", "model": "23127PN0CC", "product": "houji", "market_name": "Xiaomi 14", "hardware": "qcom", "board": "shennong", "android_ver": "14", "build_tag": "UKQ1.230804.001"},
            {"manufacturer": "xiaomi", "model": "2210132G", "product": "nuwa", "market_name": "Xiaomi 13 Pro", "hardware": "qcom", "board": "kalama", "android_ver": "13", "build_tag": "TKQ1.221114.001"},
            {"manufacturer": "xiaomi", "model": "2201122G", "product": "cupid", "market_name": "Xiaomi 12 Pro", "hardware": "qcom", "board": "taro", "android_ver": "12", "build_tag": "SKQ1.211006.001"},
            {"manufacturer": "xiaomi", "model": "23021RAAEG", "product": "tapas", "market_name": "Redmi Note 12", "hardware": "qcom", "board": "bengal", "android_ver": "13", "build_tag": "TKQ1.221114.001"},
            {"manufacturer": "xiaomi", "model": "2201117TG", "product": "spes", "market_name": "Redmi Note 11", "hardware": "qcom", "board": "bengal", "android_ver": "11", "build_tag": "RKQ1.211001.001"},
            {"manufacturer": "POCO", "model": "23049PCD8G", "product": "marble", "market_name": "Poco F5", "hardware": "qcom", "board": "marble", "android_ver": "13", "build_tag": "TKQ1.221114.001"},

            # --- OnePlus / Oppo / Vivo / Realme ---
            {"manufacturer": "OnePlus", "model": "CPH2449", "product": "salami", "market_name": "OnePlus 11 5G", "hardware": "qcom", "board": "kalama", "android_ver": "13", "build_tag": "SKQ1.221119.001"},
            {"manufacturer": "OnePlus", "model": "NE2215", "product": "taro", "market_name": "OnePlus 10 Pro", "hardware": "qcom", "board": "taro", "android_ver": "12", "build_tag": "SKQ1.211019.001"},
            {"manufacturer": "OPPO", "model": "CPH2305", "product": "Find X5 Pro", "market_name": "Oppo Find X5 Pro", "hardware": "qcom", "board": "taro", "android_ver": "12", "build_tag": "SKQ1.211230.001"},
            {"manufacturer": "vivo", "model": "V2218", "product": "PD2241", "market_name": "Vivo X90 Pro", "hardware": "mt6985", "board": "k6985v1_64", "android_ver": "13", "build_tag": "TP1A.220624.014"},
            {"manufacturer": "realme", "model": "RMX3301", "product": "RMX3301", "market_name": "Realme GT 2 Pro", "hardware": "qcom", "board": "taro", "android_ver": "12", "build_tag": "SKQ1.211019.001"},

            # --- Motorola / Asus ---
            {"manufacturer": "motorola", "model": "XT2303-2", "product": "rtwo", "market_name": "Motorola Edge 40", "hardware": "mt6891", "board": "mt6891", "android_ver": "13", "build_tag": "T1TL33.3-39-3"},
            {"manufacturer": "motorola", "model": "XT2201-1", "product": "frontier", "market_name": "Motorola Edge 30 Pro", "hardware": "qcom", "board": "taro", "android_ver": "12", "build_tag": "S3SH32.12-41-4"},
            {"manufacturer": "asus", "model": "ASUS_AI2205_C", "product": "AI2205", "market_name": "ROG Phone 7", "hardware": "qcom", "board": "kalama", "android_ver": "13", "build_tag": "TKQ1.220829.002"}
        ]

        # ==========================================
        # 2. MASSIVE TIMEZONE -> CARRIER MAPPING
        # ==========================================
        self.tz_to_carrier = {
            # --- North America ---
            "America/New_York": {"op": "310410", "name": "AT&T", "iso": "us"},
            "America/Chicago": {"op": "310260", "name": "T-Mobile", "iso": "us"},
            "America/Los_Angeles": {"op": "310012", "name": "Verizon", "iso": "us"},
            "America/Denver": {"op": "311580", "name": "US Cellular", "iso": "us"},
            "America/Phoenix": {"op": "310260", "name": "T-Mobile", "iso": "us"},
            "America/Toronto": {"op": "302610", "name": "Bell", "iso": "ca"},
            "America/Vancouver": {"op": "302720", "name": "Rogers", "iso": "ca"},
            "America/Montreal": {"op": "302220", "name": "Telus", "iso": "ca"},
            "America/Mexico_City": {"op": "334020", "name": "Telcel", "iso": "mx"},

            # --- Latin & South America ---
            "America/Sao_Paulo": {"op": "72406", "name": "Vivo", "iso": "br"},
            "America/Argentina/Buenos_Aires": {"op": "722310", "name": "Claro", "iso": "ar"},
            "America/Bogota": {"op": "732103", "name": "Tigo", "iso": "co"},
            "America/Santiago": {"op": "73001", "name": "Entel", "iso": "cl"},
            "America/Lima": {"op": "71610", "name": "Claro", "iso": "pe"},

            # --- Europe ---
            "Europe/London": {"op": "23430", "name": "EE", "iso": "gb"},
            "Europe/Belfast": {"op": "23410", "name": "O2", "iso": "gb"},
            "Europe/Berlin": {"op": "26201", "name": "Telekom", "iso": "de"},
            "Europe/Paris": {"op": "20801", "name": "Orange", "iso": "fr"},
            "Europe/Madrid": {"op": "21407", "name": "Movistar", "iso": "es"},
            "Europe/Rome": {"op": "22201", "name": "TIM", "iso": "it"},
            "Europe/Amsterdam": {"op": "20404", "name": "Vodafone", "iso": "nl"},
            "Europe/Stockholm": {"op": "24001", "name": "Telia", "iso": "se"},
            "Europe/Warsaw": {"op": "26006", "name": "Play", "iso": "pl"},
            "Europe/Istanbul": {"op": "28601", "name": "Turkcell", "iso": "tr"},
            "Europe/Kyiv": {"op": "25501", "name": "Vodafone", "iso": "ua"},

            # --- Southeast Asia ---
            "Asia/Bangkok": {"op": "52001", "name": "AIS", "iso": "th"},
            "Asia/Phnom_Penh": {"op": "45601", "name": "Cellcard", "iso": "kh"},
            "Asia/Ho_Chi_Minh": {"op": "45204", "name": "Viettel", "iso": "vn"},
            "Asia/Manila": {"op": "51502", "name": "Globe", "iso": "ph"},
            "Asia/Jakarta": {"op": "51010", "name": "Telkomsel", "iso": "id"},
            "Asia/Kuala_Lumpur": {"op": "50212", "name": "Maxis", "iso": "my"},
            "Asia/Singapore": {"op": "52501", "name": "Singtel", "iso": "sg"},

            # --- East Asia & Oceania ---
            "Asia/Tokyo": {"op": "44010", "name": "NTT Docomo", "iso": "jp"},
            "Asia/Seoul": {"op": "45005", "name": "SK Telecom", "iso": "kr"},
            "Asia/Taipei": {"op": "46692", "name": "Chunghwa", "iso": "tw"},
            "Asia/Hong_Kong": {"op": "45400", "name": "CSL", "iso": "hk"},
            "Australia/Sydney": {"op": "50501", "name": "Telstra", "iso": "au"},
            "Australia/Melbourne": {"op": "50502", "name": "Optus", "iso": "au"},
            "Pacific/Auckland": {"op": "53005", "name": "Spark", "iso": "nz"},

            # --- South Asia, Middle East, & Africa ---
            "Asia/Kolkata": {"op": "40410", "name": "Airtel", "iso": "in"},
            "Asia/Dhaka": {"op": "47001", "name": "Grameenphone", "iso": "bd"},
            "Asia/Karachi": {"op": "41001", "name": "Mobilink", "iso": "pk"},
            "Asia/Dubai": {"op": "42402", "name": "Etisalat", "iso": "ae"},
            "Asia/Riyadh": {"op": "42001", "name": "STC", "iso": "sa"},
            "Africa/Johannesburg": {"op": "65501", "name": "Vodacom", "iso": "za"},
            "Africa/Cairo": {"op": "60202", "name": "Vodafone", "iso": "eg"},
            "Africa/Lagos": {"op": "62130", "name": "MTN", "iso": "ng"},
            "Africa/Nairobi": {"op": "63902", "name": "Safaricom", "iso": "ke"}
        }

   
    @staticmethod
    def generate_random_phone(input1, input2, input3):
        """
        Combines Country Code + Prefix + Random Digits (matching input3 length)
        Supports multiple prefixes separated by commas (e.g. "96, 98, 78")
        """
        code = str(input1).strip()
        
        # If user puts "96, 98, 78" in input 2, it picks one randomly. If just "96", it uses "96".
        prefixes = [p.strip() for p in str(input2).split(",") if p.strip()]
        prefix = random.choice(prefixes) if prefixes else ""
        
        # Count how many digits are in input3 (e.g., "76536" = 5 digits)
        tail_length = len(str(input3).strip())
        if tail_length == 0:
            tail_length = 6 # Fallback if empty
            
        # Generate random numbers to fill that length
        random_tail = "".join(random.choices(string.digits, k=tail_length))
        
        return f"{code}{prefix}{random_tail}"

    @staticmethod
    def get_selected_account_ids(table_view):
        ids = []

        selection = table_view.selectionModel()

        if not selection:
            return ids

        model = table_view.model()

        for index in selection.selectedRows():

            # Handle proxy models safely
            if isinstance(model, QSortFilterProxyModel):
                source_index = model.mapToSource(index)
                source_model = model.sourceModel()
            else:
                source_index = index
                source_model = model

            # Your AccountModel stores ID in UserRole
            account_id = source_model.data(
                source_index,
                Qt.UserRole
            )

            if account_id is not None:
                ids.append(str(account_id))

        return ids


    @staticmethod
    def get_random_items_from_string(raw_string, min_items=1, max_items=1, prefix="", separator=" "):
        """
        General utility to parse a comma-separated string, clean it, 
        and return a randomized selection of items.
        
        - prefix: Add a symbol automatically (e.g., "#" for hashtags, "@" for mentions).
        - separator: How to join them together (e.g., " " for spaces, ", " for commas).
        """
        if not raw_string or not isinstance(raw_string, str):
            return ""

        # 1. Clean and split the string by comma
        raw_items = raw_string.split(',')
        clean_items = []

        for item in raw_items:
            item = item.strip()
            if not item:
                continue
                
            # Add prefix if requested and it doesn't already have it
            if prefix and not item.startswith(prefix):
                item = f"{prefix}{item}"
                
            # Prevent duplicates in the pool
            if item not in clean_items:
                clean_items.append(item)

        # 2. Pick a random amount of items
        if not clean_items:
            return ""

        # Ensure max_items doesn't exceed the total amount of available items
        actual_max = min(max_items, len(clean_items))
        actual_min = min(min_items, actual_max)

        num_to_pick = random.randint(actual_min, actual_max)
        
        # Pick random unique items from the list
        selected_items = random.sample(clean_items, num_to_pick)

        # 3. Join them into a single string
        return separator.join(selected_items) + separator


    @staticmethod
    def check_uid_live_status(uid, proxy=None):
        # UPDATE 1: Use m.facebook.com. It serves lighter HTML and triggers fewer login walls.
        url = f"https://m.facebook.com/profile.php?id={uid}"
        
        # Slightly randomized/updated modern User-Agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }
        
        proxies = {"http": proxy, "https": proxy} if proxy else None

        try:
            # Added a slightly longer timeout; proxies can be slow
            response = requests.get(url, headers=headers, proxies=proxies, timeout=15, allow_redirects=True)
            
            # 1. Standard HTTP Status Checks
            if response.status_code == 404:
                return "DEAD_404"
            
            # UPDATE 2: Explicitly catch HTTP rate limiting
            if response.status_code == 429:
                return "ERROR_RATE_LIMIT"

            # 2. Redirect Check
            current_url = response.url.strip("/").lower()
            
            # Redirected to generic home/feed
            if current_url.endswith(".mbasic.facebook.com") or "home.php" in current_url:
                return "DIE"
                
            # UPDATE 3: The Login Wall. 
            # If FB pushes you to login with a 'next' parameter pointing to the profile, 
            # the profile almost certainly exists (Live), but FB is protecting it from scrapers.
            if "/login/" in current_url:
                return "LIVE_LOGIN_WALL"

            page_text = response.text.lower()


            save_path = r"C:\Users\Rg Gear\Desktop\facebook_debug.html"
            
            with open(save_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            
           

            # 4. Explicit Dead Markers (Expanded list)
            dead_markers = {
                "this content isn't available right now": "DIE",
                "this page isn't available": "DIE",
                "content not found": "DIE",
                "link may be broken": "DIE",
                "the link you followed may be broken": "DIE",
                "page you requested was not found": "DIE"
            }
            
            for marker, status_code in dead_markers.items():
                if marker in page_text:
                    return status_code 
                
             # 3. Rate-Limit / Checkpoint via DOM
            if response.status_code == 429 or "security check" in page_text or "rate limited" in page_text:
                return f"⚠️ Warning but UID {uid} is likely Live."

            # Survived all checks -> Account is Live!
            return "LIVE"

        except requests.exceptions.Timeout:
            return "ERROR_TIMEOUT"
        except Exception as e:
            print(f"❌ Network Error checking UID {uid}: {e}")
            return "ERROR_NETWORK"
   

    @staticmethod
    def check_status_via_adb(ld_name):
        try:
            # 1. Dump the current UI hierarchy to a local XML file inside the emulator
            # This is almost instant
            dump_cmd = f"ldconsole.exe adb -n {ld_name} --command 'shell uiautomator dump /sdcard/view.xml'"
            subprocess.run(dump_cmd, shell=True, capture_output=True)

            # 2. Pull that file to your local computer
            pull_cmd = f"ldconsole.exe adb -n {ld_name} --command 'pull /sdcard/view.xml view.xml'"
            subprocess.run(pull_cmd, shell=True, capture_output=True)

            # 3. Read the XML file locally (Pure Python string searching, super fast)
            if os.path.exists("view.xml"):
                with open("view.xml", "r", encoding="utf-8") as f:
                    content = f.read()

                # Now just look for "Live" or "Dead" keywords in the raw text
                if "Checkpoint" in content or "Login" in content or "Log In" in content:
                    return "DIE"
                elif "Feed" in content or "Menu" in content:
                    return "LIVE"
                else:
                    return "LOADING"
                    
        except Exception as e:
            print(f"Error: {e}")
            return "ERROR"

    @staticmethod
    def get_yandex_code(email_address, app_password):
        """
        High-performance fetcher: Handles Character encodings, HTML fallbacks, 
        safely ignores CSS/HTML tags, and extracts Facebook 6-digit codes.
        """
        import email
        import imaplib
        import re
        from email.header import decode_header

        # Prevent crashes if the variables are empty
        if not email_address or not app_password:
            print("❌ Yandex Fetch Error: Email or App Password is missing/empty.")
            return None
            
        clean_email = str(email_address).strip()
        clean_password = str(app_password).replace(" ", "").strip()

        try:
            mail = imaplib.IMAP4_SSL("imap.yandex.com", 993)
            mail.login(clean_email, clean_password)
            
            status, _ = mail.select("FB_Codes") 
            if status != "OK":
                print("❌ Folder 'FB_Codes' not found!")
                mail.logout()
                return None

            status, messages = mail.search(None, 'UNSEEN')
            
            if status == "OK" and messages[0]:
                latest_email_id = messages[0].split()[-1]
                _, msg_data = mail.fetch(latest_email_id, "(RFC822)")
                
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # =========================================================
                # 1. CHECK THE SUBJECT LINE FIRST (Safest Method)
                # =========================================================
                subject, encoding = decode_header(msg.get("Subject", ""))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")
                
                # Check if the 6-digit code is right in the subject
                subject_match = re.search(r'\b\d{6}\b', subject)
                if subject_match:
                    code = subject_match.group(0)
                    mail.store(latest_email_id, '+FLAGS', '\\Seen')
                    mail.logout()
                    return code

                # =========================================================
                # 2. IF NOT IN SUBJECT, CAREFULLY PARSE THE BODY
                # =========================================================
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type in ["text/plain", "text/html"]:
                            charset = part.get_content_charset() or 'utf-8'
                            try:
                                body += part.get_payload(decode=True).decode(charset, errors='ignore') + " "
                            except Exception:
                                pass
                else:
                    charset = msg.get_content_charset() or 'utf-8'
                    body = msg.get_payload(decode=True).decode(charset, errors='ignore')

                # 🟢 CRITICAL FIX: Strip HTML tags and CSS so we don't catch hex colors or widths!
                clean_text = re.sub(r'<style.*?</style>', ' ', body, flags=re.IGNORECASE | re.DOTALL) # Remove CSS
                clean_text = re.sub(r'<[^>]+>', ' ', clean_text) # Remove HTML tags
                
                # Regex to find exactly 6 digits isolated, ensuring it doesn't have a '#' in front of it
                code_match = re.search(r'(?<!#)\b\d{6}\b', clean_text)
                
                if code_match:
                    code = code_match.group(0)
                    mail.store(latest_email_id, '+FLAGS', '\\Seen')
                    mail.logout()
                    return code
                else:
                    print("⚠️ Found email, but visible 6-digit code could not be parsed.")
            
            mail.logout()
            return None

        except Exception as e:
            print(f"❌ Yandex Fetch Error: {e}")
            return None


    @staticmethod
    def get_uid_in_background(adb_device_id):
        try:
            # 1. Safer command: Added '2>/dev/null' to silently ignore "file not found" errors
            cmd = f'adb -s {adb_device_id} shell "su -c \'cat /data/data/com.facebook.katana/shared_prefs/* 2>/dev/null\'"'
            
            # 🟢 Use subprocess.run instead of check_output so it doesn't crash on errors
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            raw_xml_data = result.stdout
            
            # If the files were empty or deleted, just return None peacefully
            if not raw_xml_data.strip():
                return None

            # 2. Use Regex to find the UID
            matches = re.findall(r'(1000\d{11,12}|615\d{11,13})', raw_xml_data)
            
            if matches:
                true_uid = max(set(matches), key=matches.count)
                return true_uid
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error checking Facebook UID: {e}")
            return None


    @staticmethod
    def set_location(acc_id, ld_name, lat_long, bot, status_signal):
        try:
            status_signal.emit(acc_id, ld_name, "🚀 Launching FakeGPS App...")
            bot.open_app("com.lexa.fakegps")
            bot.wait(3)
            
            bot.tap_top_center()
            bot.click_acc("Open navigation drawer")
            bot.click_id("com.lexa.fakegps:id/menu_goto_location")
            
            # Type the coordinates
            bot.type_xpath("//android.widget.EditText[@text='latitude, longitude']", lat_long)
            
            # 🟢 FIX 1: Use safe_system_click for the Android 'OK' button!
            ok_button_xpath = '//android.widget.Button[@resource-id="android:id/button1"]'
            bot.safe_system_click(ok_button_xpath)
            bot.wait(1)
            
            # 🟢 FIX 2: Use exists_xpath to prevent TimeoutException crashes
            if bot.exists_xpath(ok_button_xpath, timeout=2):
                cancel_button_xpath = '//android.widget.Button[@resource-id="android:id/button2"]'
                bot.safe_system_click(cancel_button_xpath)
            
            # Click the Play/Start button
            bot.click_xpath('//android.widget.ImageButton[@resource-id="com.lexa.fakegps:id/action_start"]')
            bot.wait(2)
            
            status_signal.emit(acc_id, ld_name, "✅ GPS Location Spoofed Successfully.")
            return True

        except Exception as e:
            status_signal.emit(acc_id, ld_name, f"❌ GPS Setup Failed: {e}")
            return False

    @staticmethod
    def set_ravo_vpn(acc_id, ld_name, target_city, bot, update_ld_status, stop_event):
        message = ""

        try:
            update_ld_status.emit( ld_name, "🚀 Launching Ravo VPN App")
            success, msg = bot.open_app("com.vpn.fast.proxy.securecactus")
            if not success:
                update_ld_status.emit(ld_name, msg)
                return False, msg
            
            bot.wait(3) 

            # --- 1. HANDLE ONBOARDING POP-UPS ---
            onboarding_elements = {
                # This union matches the modern permissioncontroller ID OR legacy packageinstaller ID
                'Allow': (
                    '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_button"] | '
                    '//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_allow_button"] | '
                    '//android.widget.Button[contains(@text, "ALLOW") or contains(@text, "Allow")]'
                ),
                'Deny': (
                    '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_deny_button"] | '
                    '//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_deny_button"] | '
                    '//android.widget.Button[contains(@text, "DENY") or contains(@text, "Don")]'
                ),
                'Not Now': '//android.widget.TextView[@resource-id="android:id/button2"]',
                'Skip': '//android.widget.Button[@content-desc="Skip"]',
                'Accept and Continue': '//android.widget.Button[@content-desc="Accept and Continue"]',
            }

            power_btn_xpath = '//android.view.View[@content-desc="Ravo VPN"]/android.view.View/android.view.View[3]'
            location_card_xpath = "//*[@content-desc='Current Location']/following-sibling::android.widget.ImageView[1]"
            not_connected_xpath = "//*[@content-desc='NOT CONNECTED']"
            connected_xpath = "//*[@content-desc='CONNECTED']"
            connecting_auth_xpath = '//*[@content-desc="CONNECTING" or @content-desc="AUTHENTICATION"]'
            target_server_xpath = f"//*[contains(@content-desc, '{target_city}')]" 
 

            screen_reached = False
            
            for _ in range(8): 
                if bot.exists_xpath(power_btn_xpath, timeout=3) or bot.exists_xpath(location_card_xpath, timeout=3):
                    screen_reached = True
                    break 
                
                # Check for random popups
                found_xpath = bot.wait_any(list(onboarding_elements.values()), timeout=2)
                if found_xpath:
                    element_name = next((name for name, xpath in onboarding_elements.items() if xpath == found_xpath), "Popup")
                    update_ld_status.emit(ld_name, f"[{acc_id}] 🛡️ Privacy screen detected: {element_name}")
                    bot.click_xpath(found_xpath)
                    bot.wait(0.5)

            if not screen_reached:
                return False, "❌ Failed to reach Name screen.", 

           # --- 2. MAIN VPN LOGIC ---
            max_selection_attempts = 2
            
            for attempt in range(max_selection_attempts):
                found_target_city = False 
                found_server_menu = False
                if stop_event.is_set(): return False
                # 1. Check Initial Connection Status
                is_not_connected = bot.exists_xpath(not_connected_xpath, timeout=10)
                current_location_desc = ""
                try:
                    loc_element = bot.find_xpath(location_card_xpath, timeout=5)
                    current_location_desc = loc_element.get_attribute("content-desc") or ""
                except:
                    pass

                # Already connected to right city?
                if not is_not_connected and target_city in current_location_desc:
                    update_ld_status.emit( ld_name, f"✅ Already connected to {target_city}. Proceeding...")
                    return True, "Already connected"

                # If disconnected, is city already selected?
                if is_not_connected and target_city in current_location_desc:
                    update_ld_status.emit( ld_name, f"✅ Target city already selected. Clicking Connect...")
                    found_target_city = True
                
                if not found_target_city:
                    # 2. Open Server Menu
                    update_ld_status.emit( ld_name, f"🔄 Opening server menu (Attempt {attempt + 1}/2)...")
                    bot.click_xpath(location_card_xpath)
                    bot.wait(1)
                    
                    # 3. SMART CHECK: Ensure Menu Loads
                    for ref_attempt in range(3):
                        if bot.exists_xpath("//*[@content-desc='Select Server']", timeout=3):
                            found_server_menu = True
                            break
                        update_ld_status.emit( ld_name, f"⚠️ Server list not loaded. Refreshing ({ref_attempt + 1}/3)...")
                        bot.pull_to_refresh()
                        bot.wait(3)
                    if stop_event.is_set(): return False
                    if not found_server_menu:
                        if attempt < max_selection_attempts - 1: continue 
                        message = "❌ Internet/VPN Menu failed to load (Max retries)"
                        update_ld_status.emit( ld_name, message)
                        return False, message

                    # 4. Search for City
                    bot.click_xpath("//*[@content-desc='Free']")
                    bot.wait(1)
                    for i in range(3): 
                        if bot.exists_xpath(target_server_xpath, timeout=2):
                            bot.click_xpath(target_server_xpath)
                            found_target_city = True
                            bot.wait(2)
                            break
                        bot.scroll_down(speed_ms=700)
                        bot.wait(1)

                    if not found_target_city:
                        update_ld_status.emit( ld_name, f"⏳ Checking 'Pro' tab...")
                        bot.click_xpath("//*[@content-desc='Pro']")
                        bot.wait(2)
                        for i in range(9):
                            if bot.exists_xpath(target_server_xpath, timeout=2):
                                bot.click_xpath(target_server_xpath)
                                found_target_city = True
                                bot.wait(1)
                                break
                            bot.scroll_down(speed_ms=700)
                            bot.wait(1)

                    
                # 5. Connect and Verify
                if found_target_city:
                    update_ld_status.emit( ld_name, f"⚡ Selected {target_city}. Connecting...")
                    bot.click_xpath(power_btn_xpath)
                    
                    # Handle Android System Consent
                    alert_title = '//android.widget.TextView[@resource-id="android:id/alertTitle"]'
                    if bot.exists_xpath(alert_title, timeout=3):
                        update_ld_status.emit( ld_name, "🔑 System VPN consent requested. Clicking 'OK'...")
                        bot.safe_system_click('//android.widget.Button[@resource-id="android:id/button1"]')
                        bot.wait(2) 
                    
                    # 📺 SMART AD WATCHER (Optimized)
                    update_ld_status.emit( ld_name, "📺 Checking for Ads")
                    
                    # Wait for connection to attempt, then check if we are on an Ad screen
                    bot.wait(2)
                    
                    # Define Ad Escape Elements
                    continue_ad_xpath = '//*[@text="Continue"]'
                    skip_video = '//*[@text="Skip"]'
                    close_candidates = [
                        '//android.widget.Image[contains(@content-desc, "Close")]',
                        '//android.widget.Button[contains(@text, "Close")]',
                        '//android.widget.ImageView[contains(@resource-id, "close")]',
                        '//android.view.View[@clickable="true" and ./android.widget.Image]', 
                        '//android.widget.Button[@clickable="true" and count(*)=0]' 
                    ]
                    
                    # Loop to clear Ads if they appear
                    for ad_wait in range(25):
                        if stop_event.is_set(): return False
                        # Exit loop if connected
                        if not bot.exists_xpath(not_connected_xpath, timeout=1) and \
                           not bot.exists_xpath(connecting_auth_xpath, timeout=1) and \
                           bot.exists_xpath(connected_xpath, timeout=1):
                            update_ld_status.emit( ld_name, "✅ Connected!")
                            break

                        # Attempt to close/skip
                        if bot.exists_xpath(continue_ad_xpath, timeout=1):
                            bot.click_xpath(continue_ad_xpath)
                        elif bot.exists_xpath(skip_video, timeout=1):
                            bot.click_xpath(skip_video)
                        else:
                            for xpath in close_candidates:
                                if bot.exists_xpath(xpath, timeout=1):
                                    bot.click_xpath(xpath)
                                    break
                            else:
                                bot.tap_percentage(98.7, 0.27) 
                        
                        bot.wait(1)
                    if stop_event.is_set(): return False
                    # Final connection verification
                    bot.wait(5)
                    try:
                        final_loc_element = bot.find_xpath(location_card_xpath, timeout=5)
                        final_location_desc = final_loc_element.get_attribute("content-desc") or ""
                        is_connected_now = not bot.exists_xpath(not_connected_xpath, timeout=3)
                        
                        if is_connected_now and target_city in final_location_desc:
                            update_ld_status.emit( ld_name, f"✅ Verified! Connected to {target_city}.")
                            return True, "Connected successfully"
                    except Exception:
                        pass
                
                else:
                    # Target city not found in list
                    message = f"❌ Could not find {target_city} in VPN list"
                    update_ld_status.emit( ld_name, message)
                    if bot.exists_xpath("//*[@content-desc='Select Server']", timeout=2):
                        bot.press_back()
                    if attempt == max_selection_attempts - 1:
                        return False, message

            # If loop finishes without returning True
            return False, "❌ Max retries reached, could not connect"

        except Exception as e:
            return False, f"VPN Crash: {str(e)[:30]}"

    @staticmethod
    def get_coordinates_from_ui(raw_text):
        raw_text = raw_text.strip()
        
        # Default safety fallback variables as numbers
        fallback_lat, fallback_long = 0.0, 0.0

        if not raw_text:
            print("⚠️ GPS Input field is empty. Defaulting to 0.0, 0.0")
            return fallback_lat, fallback_long

        try:
            if "," in raw_text:
                # Split the text at the comma
                lat_str, long_str = raw_text.split(",", 1)
                
                # 🟢 THE CONVERSION: Force strings to floating-point numbers!
                sort_lat = float(lat_str.strip())
                sort_long = float(long_str.strip())
                
                return sort_lat, sort_long
            else:
                print("❌ Invalid layout format! Missing a comma separating lat and long.")
                return fallback_lat, fallback_long
                
        except ValueError as e:
            print(f"❌ Could not convert coordinate text strings to numbers: {e}")
            return fallback_lat, fallback_long


    @staticmethod
    def get_latlong_format(data_gps: dict):
        # 2. Extract lat and long (defaulting to empty strings if they are missing)
        lat = data_gps.get("lat", "")
        lon = data_gps.get("long", "")

        # 3. Format it exactly how you want it
        if lat and lon:
            lat_long = f"{lat}, {lon}"
        else:
            lat_long = "" # Or whatever fallback you want if GPS data is missing

        return lat_long
        # Output: 11.562108, 104.888535


    @staticmethod
    def current_date_time():
        return datetime.now().strftime("%d/%m/%Y %I:%M:%S %p")
    
    @staticmethod
    def get_time_ago(date_string):
        if not date_string:
            return "Never"
            
        try:
            # 1. Convert your formatted string back into a datetime object
            past_date = datetime.strptime(date_string, "%d/%m/%Y %I:%M:%S %p")
            now = datetime.now()
            
            # 2. Calculate the difference in total seconds
            diff = now - past_date
            seconds = int(diff.total_seconds())
            
            # 3. Figure out the human-readable format
            if seconds < 60:
                return "Just now"
            elif seconds < 3600:
                minutes = seconds // 60
                return f"{minutes}mn ago"
            elif seconds < 86400:
                hours = seconds // 3600
                return f"{hours}h ago"
            elif seconds < 2592000:  # Roughly 30 days
                days = seconds // 86400
                return f"{days} days ago"
            elif seconds < 31536000: # Roughly 365 days
                months = seconds // 2592000
                return f"{months} month ago" if months == 1 else f"{months} months ago"
            else:
                years = seconds // 31536000
                return f"{years} year ago" if years == 1 else f"{years} years ago"
                
        except ValueError:
            # Fallback if the date format doesn't match or the string is broken
            return date_string

    @staticmethod
    def get_ldplayer_list(ldplayer_path):
        ldconsole_path = os.path.join(ldplayer_path, "ldconsole.exe")

        if not os.path.exists(ldconsole_path):
            print("⚠️ ldconsole.exe not found at:", ldconsole_path)
            return []
        try:
            import subprocess
            result = subprocess.run(
                [ldconsole_path, "list2"],
                capture_output=True, text=True, check=True
            )
            lines = result.stdout.strip().splitlines()
            ld_list = []
            for line in lines:
                parts = line.split(",")
                if len(parts) > 1:
                    ld_list.append({"name": parts[1].strip()})
            return ld_list
        except Exception as e:
            print("❌ Error fetching LDPlayer list:", e)
            return []
        


    @staticmethod
    def get_current_page_name(stacked_widget: QStackedWidget):
        if not stacked_widget:
            return None
        current_widget = stacked_widget.currentWidget()
        if current_widget:
            return current_widget.objectName()
        return None
    

    @staticmethod
    def update_selection_label(table: QTableView, label: QLabel):
        if not table or not label:
            return

        model = table.model()

        if model is None:
            label.setText("0/0")
            return

        selection_model = table.selectionModel()

        selected_count = (
            len(selection_model.selectedRows())
            if selection_model else 0
        )

        # Visible rows (after category/search filter)
        visible_count = model.rowCount()

        # Total rows (all accounts)
        if isinstance(model, QSortFilterProxyModel):
            total_count = model.sourceModel().rowCount()
        else:
            total_count = visible_count

        # Same count when no filter is active
        if visible_count == total_count:
            label.setText(f"{selected_count}/{total_count}")
        else:
            label.setText(
                f"{selected_count}/{visible_count} (All: {total_count})"
            )



    @staticmethod
    def show_custom_dialog(dialog_class, parent=None, **kwargs):
        dialog = dialog_class(parent)

        # Optional: pass extra data to dialog
        if hasattr(dialog, "set_data"):
            dialog.set_data(**kwargs)

        result = dialog.exec()  # Show as modal dialog
        return result, dialog



    @staticmethod
    def populate_combobox(
        combobox,
        data,
        default_item=None,
        clear_first=True
    ):
        combobox.blockSignals(True)
        try:
            if clear_first:
                combobox.clear()

            if default_item is not None:
                combobox.addItem(str(default_item))

            if data:
                combobox.addItems([str(x) for x in data])

        finally:
            combobox.blockSignals(False)

    @staticmethod
    def get_media_folder_info(folder_path, extensions):
        if not folder_path or not os.path.isdir(folder_path):
            return {
                "source_count": 0,
                "post_already_count": 0,
                "total": 0,
                "post_already_folder": ""
            }
        post_already_folder = os.path.join(folder_path, "posted")
        os.makedirs(post_already_folder, exist_ok=True)
        def count(path):
            total = 0
            try:
                for file in os.scandir(path):
                    if file.is_file() and file.name.lower().endswith(extensions):
                        total += 1
            except Exception as e:
                print(e)
            return total
        source = count(folder_path)
        posted = count(post_already_folder)
        return {
            "source_count": source,
            "post_already_count": posted,
            "total": source + posted,
            "post_already_folder": post_already_folder
        }

    @staticmethod
    def go_to_location(path):
        if not os.path.exists(path):
            return False
        try:
            if os.path.isfile(path):
                subprocess.Popen(
                    ["explorer", "/select,", os.path.normpath(path)]
                )
            else:
                os.startfile(path)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_video_duration(video_path):

        try:

            cap = cv2.VideoCapture(video_path)

            fps = cap.get(cv2.CAP_PROP_FPS)

            frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

            cap.release()

            if fps <= 0:
                return "--:--"

            seconds = int(frames / fps)

            minutes = seconds // 60
            seconds = seconds % 60

            return f"{minutes:02d}:{seconds:02d}"

        except Exception:

            return "--:--"

    @staticmethod
    def get_video_thumbnail(video_path, width=50, height=70):
        try:
            cap = cv2.VideoCapture(video_path)
            success, frame = cap.read()
            cap.release()
            
            if not success:
                return None
                
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            
            # 🟢 FIX 1 & 2: Use QImage, and MUST use .copy() so the memory survives 
            # after the CV2 numpy array gets garbage collected!
            image = QImage(
                frame.data,
                w,
                h,
                ch * w,
                QImage.Format_RGB888
            ).copy() 

            return image.scaled(
                width,
                height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

        except Exception as e:
            print(f"Video thumbnail error: {e}")
            return None

    @staticmethod
    def get_image_thumbnail(image_path, width=50, height=70):
        MAX_PIXELS = 80_000_000
        try:
            with Image.open(image_path) as img:
                # Skip huge images
                if img.width * img.height > MAX_PIXELS:
                    return None
                    
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
                
                cache_dir = os.path.join(
                    os.path.dirname(image_path),
                    ".thumb_cache"
                )
                os.makedirs(cache_dir, exist_ok=True)

                cache_path = os.path.join(
                    cache_dir,
                    os.path.splitext(os.path.basename(image_path))[0] + ".webp"
                )

                img.save(cache_path, "WEBP", quality=30)

                # 🟢 FIX 3: Return QImage instead of QPixmap so it is thread-safe!
                return QImage(cache_path)

        except Exception as e:
            print(f"Image thumbnail error: {e}")
            return None
    # ==========================================
    # 🧬 HARDWARE & PHONE GENERATOR HELPERS
    # ==========================================

    # def random_digits(self, length):
    #     return "".join(random.choices(string.digits, k=length))

    # def random_hex(self, length):
    #     return "".join(random.choices("0123456789abcdef", k=length))

    # def random_mac(self):
    #     hex_digits = "0123456789ABCDEF"
    #     mac_pairs = []
        
    #     for _ in range(6):
    #         # Pick two random hex characters and join them (e.g., 'A' + '7' = 'A7')
    #         pair = random.choice(hex_digits) + random.choice(hex_digits)
    #         mac_pairs.append(pair)
            
    #     # Join all 6 pairs with a colon
    #     return ":".join(mac_pairs)

    # def generate_full_professional_profile(self, lat=None, long=None, time_zone=None, phone_number=None):
    #     """Generates a unique profile. Carrier is strictly determined by Time Zone."""
        
    #     device = random.choice(self.device_models)
        
    #     # 3. 🛑 NO RANDOM CARRIERS: Strictly get the exact carrier for the Time Zone!
    #     carrier = self.tz_to_carrier.get(time_zone)
    #     if not carrier:
    #         # Fallback if Time Zone is empty or missing from the list
    #         carrier = {"op": "310410", "name": "AT&T", "iso": "us"} 
        
    #     imei_base = self.random_digits(15)
    #     mac_address = self.random_mac()
    #     bluetooth_mac = self.random_mac()
    #     android_id_str = self.random_hex(16)
        
    #     # Generate realistic platform system variables
    #     if device["manufacturer"] == "samsung":
    #         hardware_chip = "exynos990"
    #         board_type = "universal990"
    #         bootloader_ver = f"{device['model']}XXU1ATCT"
    #         fingerprint_str = f"samsung/{device['product']}/{device['model']}:10/QP1A.190711.020/{bootloader_ver}:user/release-keys"
    #     elif device["manufacturer"] == "google":
    #         hardware_chip = "gs201"
    #         board_type = "pantheon"
    #         bootloader_ver = f"cloudripper-{self.random_digits(4)}"
    #         fingerprint_str = f"google/{device['product']}/{device['model']}:13/TQ3A.230605.012/{self.random_digits(7)}:user/release-keys"
    #     else:
    #         hardware_chip = "qcom"
    #         board_type = "tarot"
    #         bootloader_ver = f"BL_{self.random_hex(6).upper()}"
    #         fingerprint_str = f"{device['manufacturer']}/{device['model']}/{device['model']}:12/SKQ1.211019.001/{self.random_digits(6)}:user/release-keys"

    #     # Apply the phone number if passed, otherwise generate a fake US one
    #     final_phone = phone_number if phone_number else f"+1555{imei_base[-7:]}"


        
            

    #     # profile = {
    #     #     "manufacturer": "google",
    #     #     "model": "Pixel 8 Pro",
    #     #     "market_name": "Pixel 8 Pro",
    #     #     "android_id": "70e78ce964fc16ae",
    #     #     "serial_number": "SP7901341918",
    #     #     "hardware": "gs201",
    #     #     "board": "pantheon",
    #     #     "bootloader": bootloader_ver,
    #     #     "build_fingerprint": "google/husky/Pixel 8 Pro:13/TQ3A.230605.012/0936071:user/release-keys",
    #     #     "imei": imei_base,
    #     #     "meid": "990000" + imei_base[:8],
    #     #     "gsf_id": self.random_hex(16),
    #     #     "advertising_id": "def51d9d-39da-ed60-c538-57a220675f1b",
    #     #     "mac": mac_address,
    #     #     "bluetooth_mac": bluetooth_mac,
    #     #     "wifi_ssid": f"{carrier['name']}_SPHighSpeed_{self.random_hex(4).upper()}",
    #     #     "wifi_bssid": mac_address,
    #     #     "network_generation": "13", 
    #     #     "imsi": carrier["op"] + self.random_digits(9),
    #     #     "simid": "8901" + carrier["op"] + self.random_digits(11),
    #     #     "mobile_no": "+15559195168",
    #     #     "esim_eid": "89049032" + self.random_digits(24),
    #     #     "sim_operator": carrier["op"],
    #     #     "sim_operator_name": carrier["name"],
    #     #     "sim_country_iso": carrier["iso"],
    #     # }

    #     profile = {
    #         "manufacturer": device["manufacturer"],
    #         "model": device["model"],
    #         "market_name": device["market_name"],
    #         "android_id": android_id_str,
    #         "serial_number": "SP" + imei_base[:10],
    #         "hardware": hardware_chip,
    #         "board": board_type,
    #         "bootloader": bootloader_ver,
    #         "build_fingerprint": fingerprint_str,
    #         "imei": imei_base,
    #         "meid": "990000" + imei_base[:8],
    #         "gsf_id": self.random_hex(16),
    #         "advertising_id": f"{self.random_hex(8)}-{self.random_hex(4)}-{self.random_hex(4)}-{self.random_hex(4)}-{self.random_hex(12)}",
    #         "mac": mac_address,
    #         "bluetooth_mac": bluetooth_mac,
    #         "wifi_ssid": f"{carrier['name']}_SPHighSpeed_{self.random_hex(4).upper()}",
    #         "wifi_bssid": mac_address,
    #         "network_generation": "13", 
    #         "imsi": carrier["op"] + self.random_digits(9),
    #         "simid": "8901" + carrier["op"] + self.random_digits(11),
    #         "mobile_no": final_phone,  # 📱 INJECTED HERE
    #         "esim_eid": "89049032" + self.random_digits(24),
    #         "sim_operator": carrier["op"],
    #         "sim_operator_name": carrier["name"],
    #         "sim_country_iso": carrier["iso"],
    #     }
        
    #     if time_zone:
    #         profile["timezone"] = time_zone
            
    #     if lat and long: 
    #         profile["latitude"] = str(lat)
    #         profile["longitude"] = str(long)
            
    #     return profile
   
    # Helper Utilities
    def random_digits(self, length):
        return "".join(random.choices(string.digits, k=length))

    def random_hex(self, length):
        return "".join(random.choices("0123456789abcdef", k=length))

    def random_mac(self):
        hex_digits = "0123456789ABCDEF"
        return ":".join(
            random.choice(hex_digits) + random.choice(hex_digits) 
            for _ in range(6)
        )

    def generate_valid_imei(self):
        """Generates a 15-digit IMEI compliant with the Luhn checksum algorithm."""
        # TAC (Type Allocation Code) prefix for mobile devices
        tac_prefix = random.choice(["35208411", "35482110", "86420504", "35924710"])
        body = tac_prefix + self.random_digits(6)  # 14 digits total
        
        # Calculate Luhn Checksum for the 15th digit
        total = 0
        for i, digit in enumerate(body):
            d = int(digit)
            if i % 2 != 0:  # Double every second digit (0-indexed position 1, 3, 5...)
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        check_digit = (10 - (total % 10)) % 10
        return body + str(check_digit)

    def generate_full_professional_profile(self, lat=None, long=None, time_zone=None, phone_number=None):
        """Generates a hardware profile matching selected device specifications."""
        device = random.choice(self.device_models)
        
        # Select carrier based on time zone, defaulting to US AT&T if missing
        carrier = self.tz_to_carrier.get(time_zone, {"op": "310410", "name": "AT&T", "iso": "us"})
        
        imei_val = self.generate_valid_imei()
        device_mac = self.random_mac()
        bluetooth_mac = self.random_mac()
        router_bssid = self.random_mac()  # Distinct MAC for Wi-Fi Access Point
        android_id_str = self.random_hex(16)
        
        # Build Fingerprint dynamically using device metadata
        bootloader_ver = f"{device['model']}XXU1{self.random_hex(4).upper()}"
        fingerprint_str = (
            f"{device['manufacturer']}/{device['product']}/{device['model']}:"
            f"{device['android_ver']}/{device['build_tag']}/"
            f"{self.random_digits(7)}:user/release-keys"
        )

        final_phone = phone_number if phone_number else f"+1555{imei_val[-7:]}"

        # Construct profile
        profile = {
            "manufacturer": device["manufacturer"],
            "model": device["model"],
            "market_name": device["market_name"],
            "product": device["product"],
            "android_id": android_id_str,
            "serial_number": "SP" + imei_val[:10],
            "hardware": device["hardware"],
            "board": device["board"],
            "bootloader": bootloader_ver,
            "build_fingerprint": fingerprint_str,
            "imei": imei_val,
            "meid": "990000" + imei_val[:8],
            "gsf_id": self.random_hex(16),
            "advertising_id": f"{self.random_hex(8)}-{self.random_hex(4)}-{self.random_hex(4)}-{self.random_hex(4)}-{self.random_hex(12)}",
            "mac": device_mac,
            "bluetooth_mac": bluetooth_mac,
            "wifi_ssid": f"{carrier['name']}_Home_{self.random_hex(4).upper()}",
            "wifi_bssid": router_bssid,
            "network_generation": "13",
            "imsi": carrier["op"] + self.random_digits(9),
            "simid": "8901" + carrier["op"] + self.random_digits(11),
            "mobile_no": final_phone,
            "esim_eid": "89049032" + self.random_digits(24),
            "sim_operator": carrier["op"],
            "sim_operator_name": carrier["name"],
            "sim_country_iso": carrier["iso"],
        }
        
        if time_zone:
            profile["timezone"] = time_zone
            
        if lat and long:
            profile["latitude"] = str(lat)
            profile["longitude"] = str(long)
            
        return profile












