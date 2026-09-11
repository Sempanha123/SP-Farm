from PySide6.QtWidgets import (
    QWidget,
    QCheckBox,
    QSpinBox,
    QDoubleSpinBox,
    QTextEdit,
    QPlainTextEdit,
    QComboBox
)
# from appium.webdriver.common.appiumby import AppiumBy
import random
import os
import random
import glob
import re
import time
import pyotp
from core.app_signals import signals
import shutil
class ActiveTab(QWidget):
    def __init__(self, ui=None, parent=None, data_manager=None, ld_manager=None, general_function=None, account_cache=None):
        super().__init__()
        self.ui = ui
        self.parent = parent
        self.data_manager = data_manager
        self.ld_manager = ld_manager 
        self.general_function = general_function
        self.account_cache = account_cache


        self.actives_settings = self.data_manager.get_active_settings()

        self._loading_settings = False

        # 1. First, load existing settings into the UI
        self.load_active_settings()
        self._connect_signals()

        


        self.send_button_xpath = '//android.view.ViewGroup[@content-desc="Send"]'
        self.vid_heading_xpath = '//android.widget.TextView[@content-desc="Video, Heading"]'
        self.foryou_btn_xpath = '//android.view.ViewGroup[@content-desc="For you Button"]'
        self.live_btn_xpath = '//android.view.ViewGroup[@content-desc="Live Button"]'
        self.sound_icon_xpath = '//android.widget.ImageView[@content-desc="Toggle video sound"] | //android.widget.RelativeLayout[contents(@content-desc, "Mute video")]'
        self.fs_back_xpath = '//android.view.ViewGroup[@content-desc="Back"] | //android.widget.Button[@content-desc="Back"]'

        self.fs_comment_xpath = '//android.view.ViewGroup[@content-desc="Comment"]'
        self.fs_share_xpath = '//android.view.ViewGroup[@content-desc="Share"]'

        self.reaction_xpath = (
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

        self.fs_search_xpath = '//android.view.ViewGroup[@content-desc="Search"]'
        self.fs_reels_prof_xpath = '//android.view.ViewGroup[@content-desc="Navigate to your Reels profile"]'
        self.fs_create_reels_xpath = '//android.view.ViewGroup[@content-desc="Create reel"]'
        self.fs_follow_xpath = '//android.view.ViewGroup[contains(@content-desc, "this person")]'

        self.close_btn = (
            '//android.widget.Button[@content-desc="Close"] | '
            '//android.view.ViewGroup[@content-desc="Close"] | ' 
            '//*[contains(@content-desc, "Close")] |'
            '//android.widget.Button[contains(@text, "Close") or contains(@text, "Close")] |'
        )
        self.personal_details = (
            '//android.widget.Button[contains(@content-desc, "Profiles, Your accounts and profiles")] | '
            '//android.widget.Button[contains(@content-desc, "Profiles and personal details")] | '
            '//android.view.View[@content-desc="Profiles and personal details"]/parent::*'
        )  
        
        self.wrong_pass_error = (
            '//android.view.View[@content-desc="The password you entered is incorrect. Try again."] |'
            '//android.view.View[contains(@content-desc, "is incorrect")] | '
            '//*[contains(@content-desc, "incorrect") or contains(@content-desc, "wrong") or contains(@content-desc, "match")]'
        )
        self.continue_btn = (
            '//android.view.ViewGroup[@content-desc="Continue"] |'
            '//android.widget.Button[@content-desc="Continue"] | '
        )
        self.ok_btn = (
                '//android.view.View[@content-desc="OK"] |'
                '//android.widget.Button[contains(@text, "OK") or contains(@text, "OK")] |'
            ),
        self.skip_btn = (
                '//android.view.View[@content-desc="Skip"] |'
                '//android.widget.Button[contains(@text, "Skip") or contains(@text, "Skip") or contains(@text, "SKIP")] |'
            ),
        self.allow_btn = (
            '//android.view.ViewGroup[@content-desc="Allow"] |'
            '//android.view.ViewGroup[@content-desc="Allow access"] | '
            '//*[@text="ALLOW" or @text="Allow"] | '
            '//android.widget.Button[@resource-id="com.android.packageinstaller:id/permission_allow_button"] | '
            '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_all_button"] |'
            '//android.widget.Button[@resource-id="com.android.permissioncontroller:id/permission_allow_foreground_only_button"]'
        )
        self.popup_xpaths = (
            '//android.widget.Button['
                '@content-desc="Save" or @content-desc="Skip" or @content-desc="Close" or '
                '@content-desc="Not Now" or @content-desc="Not now" or '
                '@text="Skip" or @text="Not Now" or @text="Not now" or @resource-id="android:id/button2"'
            '] | '
            '//android.view.ViewGroup['
                '@content-desc="Save" or @content-desc="Skip" or @content-desc="Close" or '
                '@content-desc="Not Now" or @content-desc="Not now" or @resource-id="android:id/button2"'
            '] | '
            '//android.widget.TextView['
                '@text="Skip" or @text="Not Now" or @text="Not now" or '
                '@resource-id="android:id/button2"'
            '] | //android.widget.Button[@text="OK"]'
        )
        
        self.accounts_center = '//android.view.View[@content-desc="Accounts Center"] | //android.view.View[contains(@content-desc, "Password, security, personal details")]'
            
        self.search_xpath = '//android.widget.AutoCompleteTextView[contains(@text, "Search")] | //android.widget.EditText[contains(@text, "Search")] | //android.widget.EditText[contains(@content-desc, "Search")]'

        self.search_btn = (
            '//android.widget.Button[@content-desc="Search"] |'
            '//*[@content-desc="Search"]'
        )

        self.comment_input_xpath = '//android.widget.EditText | //android.widget.AutoCompleteTextView | //*[contains(@text, "Comment as ")]'
        self.comment_btn_xpath = '//android.view.ViewGroup[contains(@content-desc, "Comment")] | //android.widget.Button[contains(@content-desc, "Comment")]'
        self.share_to_group_btn = '//android.view.ViewGroup[contains(@content-desc, "Group") or contains(@content-desc, "group")] | //android.widget.TextView[contains(@text, "Group")]'
        self.post_btn = '//android.view.ViewGroup[@content-desc="POST" or @content-desc="Post"] | //android.widget.Button[contains(@content-desc, "POST")]'
        self.top_home_feed = [
            '//android.view.ViewGroup[contains(@content-desc, "Make a post")] | //android.widget.Button[contains(@content-desc, "Make a post")]',
            '//android.view.ViewGroup[contains(@content-desc, "Go to profile")]',
            '//android.view.View[contains(@content-desc, "Make a post")]',
            '//android.view.ViewGroup[@content-desc="Select photos or videos for your post"]',
            '//android.view.ViewGroup[@content-desc="Stories"]'
        ]




    def _connect_signals(self):
        tracked_setting_keys = [
            "like", "like_from", "like_to", "love", "love_to", "haha", "haha_from", "haha_to",
            "cry", "cry_from", "cry_to", "angry", "angry_from", "angry_to", "get_account_info",
            "add_friends", "add_friends_from", "add_friends_to", "confirm_friends", 
            "confirm_friends_from", "confirm_friends_to", "check_notifycation", 
            "click_join_group_in_notification", "total_click_notification", 
            "total_click_notification_from", "total_click_notification_to", "watch_feeds", 
            "watch_feeds_from", "watch_feeds_to", "delay_watch_feeds_from", "delay_watch_feeds_to",
            "feeds_no_emoji", "feeds_alway_emoji", "feeds_random_emoji", "feeds_like", 
            "feeds_like_from", "feeds_like_to", "feeds_love", "feeds_love_from", "feeds_love_to",
            "feeds_haha", "feeds_haha_from", "feeds_haha_to", "feeds_cry", "feeds_cry_from", 
            "feeds_cry_to", "feeds_angry", "feeds_angry_from", "feeds_angry_to", "watch_videos", 
            "watch_videos_from", "watch_videos_to", "delay_watch_video_from", "delay_watch_video_to",
            "videos_no_emoji", "videos_alway_emoji", "videos_random_emoji", "videos_like", 
            "videos_like_from", "videos_like_to", "videos_love", "videos_love_from", "videos_love_to",
            "videos_haha", "videos_haha_from", "videos_haha_to", "videos_cry", "videos_cry_from", 
            "videos_cry_to", "videos_angry", "videos_angry_from", "videos_angry_to", "chat", 
            "comments", "story", "comments_by_text", "comments_by_text_from", "comments_by_text_to", 
            "comments_text", "comments_sticker", "comments_sticker_from", "comments_sticker_to", 
            "chat_by_text", "chat_by_text_from", "chat_by_text_to", "chat_text", "chat_sticker", 
            "chat_sticker_from", "chat_sticker_to", "story", "story_from", 
            "story_to", "reply_story", "reply_story_from", 
            "reply_story_to", "reply_story_text", "reply_story_no_emoji", "reply_story_alway_emoji", 
            "reply_story_ramdom_emoji", "reply_story_like", "reply_story_like_from", 
            "reply_story_like_to", "reply_story_love", "reply_story_love_from", "reply_story_love_to",
            "reply_story_haha", "reply_story_haha_from", "reply_story_haha_to", "reply_story_cry", 
            "reply_story_cry_from", "reply_story_cry_to", "reply_story_angry", 
            "reply_story_angry_from", "reply_story_angry_to", "get_account_info", "add_email_yandex", 
            "two_fa", "add_mail_with_two_fa", "yandex_mail", "app_password_yandex", "yandex_start", "backup_data_fb_ld", "set_up_mail", "scrape_group"
        ]

        for key in tracked_setting_keys:
            if hasattr(self.ui, key):
                widget = getattr(self.ui, key)
                widget_type = widget.__class__.__name__
                
                try:
                    if widget_type == "QCheckBox":
                        widget.stateChanged.connect(self.save_active_settings)
                    elif widget_type == "QSpinBox":
                        widget.valueChanged.connect(self.save_active_settings)
                    elif widget_type == "QSlider":
                        widget.valueChanged.connect(self.save_active_settings)
                    elif widget_type in ["QLineEdit"]:
                        widget.textChanged.connect(self.save_active_settings)
                    elif widget_type in ["QTextEdit", "QPlainTextEdit"]:
                        widget.textChanged.connect(self.save_active_settings)
                    elif widget_type == "QRadioButton":
                        widget.toggled.connect(self.save_active_settings)
                except Exception as e:
                    print(f"⚠️ Failed to connect auto-save signal for {key}: {e}")
        
    def load_active_settings(self):
        self._loading_settings = True
        
        try:
            
            if not isinstance(self.actives_settings, dict):
                return

            for key, value in self.actives_settings.items():
                if not hasattr(self.ui, key):
                    continue
                    
                widget = getattr(self.ui, key)
                widget_type = widget.__class__.__name__

                # Added QRadioButton here — both use .setChecked(bool)
                if widget_type in ["QCheckBox", "QRadioButton"]:
                    widget.setChecked(bool(value))
                elif widget_type in ["QSpinBox", "QSlider"]:
                    widget.setValue(int(value))
                elif widget_type in ["QLineEdit"]:
                    widget.setText(str(value))
                elif widget_type in ["QTextEdit", "QPlainTextEdit"]:
                    widget.setPlainText(str(value))
                    
        except Exception as e:
            print(f"⚠️ Error loading settings to UI: {e}")
        finally:
            self._loading_settings = False

    def save_active_settings(self):
        if self._loading_settings:
            return
        self._loading_settings = True
        try:
            self.actives_settings = {
                "backup_data_fb_ld": self.ui.backup_data_fb_ld.isChecked(),
                "scrape_group": self.ui.scrape_group.isChecked(),

                "like": self.ui.like.isChecked(),
                "like_from": self.ui.like_from.value(),
                "like_to": self.ui.like_to.value(),

                "love": self.ui.love.isChecked(),
                "love_from": self.ui.love_from.value(),
                "love_to": self.ui.love_to.value(),

                "haha": self.ui.haha.isChecked(),
                "haha_from": self.ui.haha_from.value(),
                "haha_to": self.ui.haha_to.value(),

                "cry": self.ui.cry.isChecked(),
                "cry_from": self.ui.cry_from.value(),
                "cry_to": self.ui.cry_to.value(),

                "angry": self.ui.angry.isChecked(),
                "angry_from": self.ui.angry_from.value(),
                "angry_to": self.ui.angry_to.value(),

                #  ===== General Action ===========
                "get_account_info": self.ui.get_account_info.isChecked(),

                "add_friends": self.ui.add_friends.isChecked(),
                "add_friends_from": self.ui.add_friends_from.value(),
                "add_friends_to": self.ui.add_friends_to.value(),

                "confirm_friends": self.ui.confirm_friends.isChecked(),
                "confirm_friends_from": self.ui.confirm_friends_from.value(),
                "confirm_friends_to": self.ui.confirm_friends_to.value(),

                "check_notifycation": self.ui.check_notifycation.isChecked(),
                "click_join_group_in_notification": self.ui.click_join_group_in_notification.isChecked(),
                
                "total_click_notification": self.ui.total_click_notification.isChecked(),
                "total_click_notification_from": self.ui.total_click_notification_from.value(),
                "total_click_notification_to": self.ui.total_click_notification_to.value(),

                # ======Watch Reed ===================
                "watch_feeds": self.ui.watch_feeds.isChecked(),
                "watch_feeds_from": self.ui.watch_feeds_from.value(),
                "watch_feeds_to": self.ui.watch_feeds_to.value(),

                "delay_watch_feeds_from": self.ui.delay_watch_feeds_from.value(),
                "delay_watch_feeds_to": self.ui.delay_watch_feeds_to.value(),

                "feeds_no_emoji": self.ui.feeds_no_emoji.isChecked(),
                "feeds_alway_emoji": self.ui.feeds_alway_emoji.isChecked(),
                "feeds_random_emoji": self.ui.feeds_random_emoji.isChecked(),

                "feeds_like": self.ui.feeds_like.isChecked(),
                "feeds_like_from": self.ui.feeds_like_from.value(),
                "feeds_like_to": self.ui.feeds_like_to.value(),

                "feeds_love": self.ui.feeds_love.isChecked(),
                "feeds_love_from": self.ui.feeds_love_from.value(),
                "feeds_love_to": self.ui.feeds_love_to.value(),

                "feeds_haha": self.ui.feeds_haha.isChecked(),
                "feeds_haha_from": self.ui.feeds_haha_from.value(),
                "feeds_haha_to": self.ui.feeds_haha_to.value(),

                "feeds_cry": self.ui.feeds_cry.isChecked(),
                "feeds_cry_from": self.ui.feeds_cry_from.value(),
                "feeds_cry_to": self.ui.feeds_cry_to.value(),

                "feeds_angry": self.ui.feeds_angry.isChecked(),
                "feeds_angry_from": self.ui.feeds_angry_from.value(),
                "feeds_angry_to": self.ui.feeds_angry_to.value(),

                # ======Watch Videos  ===================
                "watch_videos": self.ui.watch_videos.isChecked(),
                "watch_videos_from": self.ui.watch_videos_from.value(),
                "watch_videos_to": self.ui.watch_videos_to.value(),

                "delay_watch_video_from": self.ui.delay_watch_video_from.value(),
                "delay_watch_video_to": self.ui.delay_watch_video_to.value(),

                "videos_no_emoji": self.ui.videos_no_emoji.isChecked(),
                "videos_alway_emoji": self.ui.videos_alway_emoji.isChecked(),
                "videos_random_emoji": self.ui.videos_random_emoji.isChecked(),

                "videos_like": self.ui.videos_like.isChecked(),
                "videos_like_from": self.ui.videos_like_from.value(),
                "videos_like_to": self.ui.videos_like_to.value(),

                "videos_love": self.ui.videos_love.isChecked(),
                "videos_love_from": self.ui.videos_love_from.value(),
                "videos_love_to": self.ui.videos_love_to.value(),

                "videos_haha": self.ui.videos_haha.isChecked(),
                "videos_haha_from": self.ui.videos_haha_from.value(),
                "videos_haha_to": self.ui.videos_haha_to.value(),

                "videos_cry": self.ui.videos_cry.isChecked(),
                "videos_cry_from": self.ui.videos_cry_from.value(),
                "videos_cry_to": self.ui.videos_cry_to.value(),

                "videos_angry": self.ui.videos_angry.isChecked(),
                "videos_angry_from": self.ui.videos_angry_from.value(),
                "videos_angry_to": self.ui.videos_angry_to.value(),

                # =============Connect Community=============
                "chat": self.ui.chat.isChecked(),
                "comments": self.ui.comments.isChecked(),

                    # ========= Comments ===============
                "comments_by_text": self.ui.comments_by_text.isChecked(),
                "comments_by_text_from": self.ui.comments_by_text_from.value(),
                "comments_by_text_to": self.ui.comments_by_text_to.value(),
                "comments_text": self.ui.comments_text.toPlainText(),
                "comments_sticker": self.ui.comments_sticker.isChecked(),
                "comments_sticker_from": self.ui.comments_sticker_from.value(),
                "comments_sticker_to": self.ui.comments_sticker_to.value(),

                    # ========= Chat ===============
                "chat_by_text": self.ui.chat_by_text.isChecked(),
                "chat_by_text_from": self.ui.chat_by_text_from.value(),
                "chat_by_text_to": self.ui.chat_by_text_to.value(),
                "chat_text": self.ui.chat_text.toPlainText(),

                "chat_sticker": self.ui.chat_sticker.isChecked(),
                "chat_sticker_from": self.ui.chat_sticker_from.value(),
                "chat_sticker_to": self.ui.chat_sticker_to.value(),

                    # ============ Story =================
                "story": self.ui.story.isChecked(),
                "story_from": self.ui.story_from.value(),
                "story_to": self.ui.story_to.value(),

                "reply_story": self.ui.reply_story.isChecked(),
                "reply_story_from": self.ui.reply_story_from.value(),
                "reply_story_to": self.ui.reply_story_to.value(),
                "reply_story_text": self.ui.reply_story_text.toPlainText(),
                
                "reply_story_no_emoji": self.ui.reply_story_no_emoji.isChecked(),
                "reply_story_alway_emoji": self.ui.reply_story_alway_emoji.isChecked(),
                "reply_story_ramdom_emoji": self.ui.reply_story_ramdom_emoji.isChecked(),

                "reply_story_like": self.ui.reply_story_like.isChecked(),
                "reply_story_like_from": self.ui.reply_story_like_from.value(),
                "reply_story_like_to": self.ui.reply_story_like_to.value(),

                "reply_story_love": self.ui.reply_story_love.isChecked(),
                "reply_story_love_from": self.ui.reply_story_love_from.value(),
                "reply_story_love_to": self.ui.reply_story_love_to.value(),

                "reply_story_haha": self.ui.reply_story_haha.isChecked(),
                "reply_story_haha_from": self.ui.reply_story_haha_from.value(),
                "reply_story_haha_to": self.ui.reply_story_haha_to.value(),

                "reply_story_cry": self.ui.reply_story_cry.isChecked(),
                "reply_story_cry_from": self.ui.reply_story_cry_from.value(),
                "reply_story_cry_to": self.ui.reply_story_cry_to.value(),

                "reply_story_angry": self.ui.reply_story_angry.isChecked(),
                "reply_story_angry_from": self.ui.reply_story_angry_from.value(),
                "reply_story_angry_to": self.ui.reply_story_angry_to.value(),


                "add_email_yandex": self.ui.add_email_yandex.isChecked(),
                "two_fa": self.ui.two_fa.isChecked(),
                "add_mail_with_two_fa": self.ui.add_mail_with_two_fa.isChecked(),

                "set_up_mail": self.ui.set_up_mail.isChecked(),
                "yandex_mail": self.ui.yandex_mail.text(),
                "yandex_start": self.ui.yandex_start.text(),
                "app_password_yandex": self.ui.app_password_yandex.text(),
            }

            self.data_manager.update_active_settings(self.actives_settings)

        finally:
            self._loading_settings = False

    def Start_Active_Accounts(self, driver, bot, acc_id, ld_name, appium_name, data_acc, update_acc_signal, update_ld_signal, stop_event):
        last_milestone = "Initialization"
        execution_report = [] 
        total_adds = 0 


        try:
            # ==========================================
            # 🛡️ 1. VPN SETUP
            # ==========================================
            if data_acc.get("vpn", {}).get("enable"):
                update_acc_signal.emit(acc_id, False, {"status": "🛡️ Connecting VPN..."})
                vpn_success, msg = self.general_function.set_ravo_vpn(acc_id, ld_name, data_acc.get("vpn", {}).get("city", ""), bot, update_ld_signal, stop_event)
                if not vpn_success:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed {msg}")
                    update_acc_signal.emit(acc_id, True, {"status": f"❌ Failed {msg}"})
                    return False
            if stop_event.is_set(): return driver




            # --- I. BACKUP DATA ---
            last_milestone = "BACKUP"
            if self.actives_settings.get("backup_data_fb_ld"):
                update_acc_signal.emit(acc_id, False, {"status": "💾 Backing up device..."})
                try:
                    raw_backup_path = data_acc.get("backup_file_name")
                    if raw_backup_path:
                        out_dir, b_name = os.path.split(raw_backup_path)
                    else:
                        out_dir, b_name = "backups", None
                        
                    # 🟢 1. Back up Main Facebook (Katana)
                    saved_path = self.ld_manager.backup_full_device_with_identity(                
                        acc_id=acc_id,
                        update_ld_signal=update_ld_signal, 
                        ld_name=ld_name, 
                        appium_name=appium_name,
                        backup_name=b_name,
                        output_dir=out_dir,
                        package_name="com.facebook.katana" # Specify the app!
                    ) 
                    
                    # 🟢 2. Ensure both apps go to the same folder!
                    # If this is a new account (b_name was None), grab the newly generated folder name
                    if saved_path and not b_name:
                        b_name = os.path.basename(saved_path)
                        
                    # 🟢 3. Back up Facebook Lite into the exact same folder
                    if saved_path:
                        self.ld_manager.backup_full_device_with_identity(                
                            acc_id=acc_id,
                            update_ld_signal=update_ld_signal, 
                            ld_name=ld_name, 
                            appium_name=appium_name,
                            backup_name=b_name, # Forces Lite into the folder we just used/created
                            output_dir=out_dir,
                            package_name="com.facebook.lite" # Specify the app!
                        )
                        
                except Exception as e:
                    print(e)
                    execution_report.append(f"Backup fail: {str(e)[:20]}")



                update_acc_signal.emit(acc_id, True, {
                    "status": "💾 Backing up device...",
                    "backup_file_name": saved_path})


            # return True

            # ==========================================
            # 🚀 2. LAUNCH FACEBOOK & POPUP HANDLING
            # ==========================================
            update_acc_signal.emit(acc_id, False, {"status": "🚀 Launching Facebook..."})
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Launching Facebook")
            
            # bot.open_app("com.facebook.lite")
            bot.open_app("com.facebook.katana")
            bot.wait(4)

            session_expired_texts = '//android.widget.TextView[@text="Session Expired" or @text="Please log in again."]'
       

            facebook_screen = False
            session_expired = False 
            
            # 1. Define your XPaths clearly at the top
            all_dismiss_xpaths = f"{self.popup_xpaths} | {self.allow_btn} | {self.close_btn}"
            all_home_xpaths = f"{self.top_home_feed} | //*[contains(@content-desc, 'tab 1 of')] | //android.view.View[@content-desc='Home, tab 1 of 6']"

            # 2. Optimized Loop
            for _ in range(6):
                if stop_event.is_set(): return driver

                # Check for Session Expired first (Fatal error)
                if bot.exists_xpath(session_expired_texts, timeout=1):
                    found_ok = bot.wait_any(self.ok_btn, timeout=1)
                    if found_ok: 
                        bot.click_xpath(found_ok)
                        bot.wait(1)
                    break # Break the loop, session is dead

                # Check for Home Feed (Success)
                if bot.exists_xpath(all_home_xpaths, timeout=1):
                    facebook_screen = True
                    break 

                # Check for ANY popup and dismiss immediately
                found_popup = bot.wait_any(all_dismiss_xpaths, timeout=1)
                if found_popup:
                    bot.click_xpath(found_popup)
                    bot.wait(1)

            if session_expired:
                update_acc_signal.emit(acc_id, True, {
                    "status": "❌ Session Expired",
                    "account_status": "LOGGED_OUT",
                    "last_date": self.general_function.current_date_time()
                })
                return driver
            if not facebook_screen:
                uid = data_acc.get("uid")
                public_status = str(self.general_function.check_uid_live_status(uid)).upper()
                
                if "DEAD" in public_status or "DIE" in public_status or "404" in public_status:
                    fail_reason = "Account is Banned/Dead"
                    db_status = "DIE"
                else:
                    fail_reason = "Checkpoint/Locked"
                    db_status = "CHECKPOINT"
                    
                update_acc_signal.emit(acc_id, True, {
                    "status": f"❌ {fail_reason}",
                    "account_status": db_status,
                    "last_date": self.general_function.current_date_time()
                })
                return driver
            
            last_milestone = "Facebook Feed Loaded"

            # ==========================================
            # 🟢 3. MODULE EXECUTION
            # ==========================================
            dynamic_tabs = self.map_dynamic_tabs(bot, update_ld_signal, ld_name)
            if dynamic_tabs is None: 
                update_acc_signal.emit(acc_id, True, {"status": "❌ Tab Facebook not Found"})
                return driver
            tab_bar_xpaths = [data["xpath"] for name, data in dynamic_tabs.items()]


            # --- A. HOME FEED ---
            do_confirm = self.actives_settings.get("confirm_friends")
            do_add = self.actives_settings.get("add_friends")
            last_milestone = "HOME FEED" 
            update_acc_signal.emit(acc_id, False, {"status": "📰 Scrolling Home Feed..."})
            success, result = self.process_home_feed(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
            if success: total_adds += result
            else: execution_report.append(f"Feed fail: {result}")
            if stop_event.is_set(): return driver

            # --- B. FRIENDS ---
            if do_confirm or do_add:
                last_milestone = "PROCESSING FRIENDS"
                update_acc_signal.emit(acc_id, False, {"status": "👥 Processing Friends..."})
                success, reason = self.process_friends(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, total_adds, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Friends fail: {reason}")
            if stop_event.is_set(): return driver
            
            
            # --- C. VIDEOS ---
            last_milestone = "WATCH VIDEOS"
            if self.actives_settings.get("watch_videos"):
                success, reason = self.process_videos(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Video fail: {reason}")
        
            
            # --- D. REELS (WATCHING) ---
            last_milestone = "WATCH VIDEOS REELS"
            if self.actives_settings.get("watch_feeds"):
                success, reason = self.process_videos_reels(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Reels fail: {reason}")
        

            # --- E. STORIES ---
            last_milestone = "WATCH STORY"
            if self.actives_settings.get("story"):
                success, reason = self.process_stories(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Story fail: {reason}")

            # --- F. CHAT ---
            last_milestone = "PROCESSING CHAT"
            if self.actives_settings.get("chat"):
                success, reason = self.process_chat_module(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Chat fail: {reason}")

            # --- G. NOTIFICATIONS ---
            last_milestone = "CHECK NOTIFYCATION"
            if self.actives_settings.get("check_notifycation"):
                success, reason = self.process_notifications(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Notifs fail: {reason}")

            # --- H. SETTINGS / INFO EXTRACT ---
            last_milestone = "GET ACCOUNT INFO"
            if (self.actives_settings.get("get_account_info") or self.actives_settings.get("set_up_mail")):
                success, reason = self.setting_options(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, data_acc, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Settings fail: {reason}")


             # --- POST STORY ---
            last_milestone = "POST STORY"
            datas_post = self.data_manager.get_post_setting_by_id(acc_id)
            if datas_post and datas_post.get("post_storys", {}).get("post_story", False):
                success, reason = self.process_posts_storys(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success:
                    update_acc_signal.emit(acc_id, True, {"status": f"❌ Post Story Fail: {reason}", "last_date": self.general_function.current_date_time()})
                    return driver
            if stop_event.is_set(): return driver

             # --- POST REELS ---
            last_milestone = "POST VIDEOS REELS"
            if datas_post and datas_post.get("post_reels", {}).get("post", False):
                success, reason = self.process_posts_reels(acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, data_acc, appium_name, stop_event)
                if not success:
                    update_acc_signal.emit(acc_id, True, {"status": f"❌ Post Reels Fail: {reason}", "last_date": self.general_function.current_date_time()})
                    return driver
            if stop_event.is_set(): return driver

             # --- POST VIDEO LONG ---
            last_milestone = "POST VIDEOS LONG"
            if datas_post and datas_post.get("post_videos", {}).get("post_video", False):
                success, reason = self.process_posts_videos(acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, data_acc, appium_name, stop_event)
                if not success:
                    update_acc_signal.emit(acc_id, True, {"status": f"❌ Post Video Fail: {reason}", "last_date": self.general_function.current_date_time()})
                    return driver
            if stop_event.is_set(): return driver

             # --- POST IMAGES ---
            last_milestone = "POST IMAGES"
            if datas_post and datas_post.get("post_images", {}).get("post_image", False):
                success, reason = self.process_posts_images(acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, data_acc, appium_name, stop_event)
                if not success:
                    update_acc_signal.emit(acc_id, True, {"status": f"❌ Post Images Fail: {reason}", "last_date": self.general_function.current_date_time()})
                    return driver
            if stop_event.is_set(): return driver



            if self.actives_settings.get("scrape_group"):
                success, reason = self.extract_and_save_groups(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success: execution_report.append(f"Extract Group fail: {reason}")
            if stop_event.is_set(): return driver

            # --- I. BACKUP DATA ---
            last_milestone = "BACKUP"
            if self.actives_settings.get("backup_data_fb_ld"):
                update_acc_signal.emit(acc_id, False, {"status": "💾 Backing up device..."})
                try:
                    raw_backup_path = data_acc.get("backup_file_name")
                    if raw_backup_path:
                        out_dir, b_name = os.path.split(raw_backup_path)
                    else:
                        out_dir, b_name = "backups", None
                        
                    # 🟢 1. Back up Main Facebook (Katana)
                    saved_path = self.ld_manager.backup_full_device_with_identity(                
                        acc_id=acc_id,
                        update_ld_signal=update_ld_signal, 
                        ld_name=ld_name, 
                        appium_name=appium_name,
                        backup_name=b_name,
                        output_dir=out_dir,
                        package_name="com.facebook.katana" # Specify the app!
                    ) 
                    
                    # 🟢 2. Ensure both apps go to the same folder!
                    # If this is a new account (b_name was None), grab the newly generated folder name
                    if saved_path and not b_name:
                        b_name = os.path.basename(saved_path)
                        
                    # 🟢 3. Back up Facebook Lite into the exact same folder
                    if saved_path:
                        self.ld_manager.backup_full_device_with_identity(                
                            acc_id=acc_id,
                            update_ld_signal=update_ld_signal, 
                            ld_name=ld_name, 
                            appium_name=appium_name,
                            backup_name=b_name, # Forces Lite into the folder we just used/created
                            output_dir=out_dir,
                            package_name="com.facebook.lite" # Specify the app!
                        )
                        
                except Exception as e:
                    print(e)
                    execution_report.append(f"Backup fail: {str(e)[:20]}")

            # ==========================================
            # 🏁 4. FINAL STATUS
            # ==========================================
            if stop_event.is_set(): return driver
                
            final_status = "✅ Completed" if not execution_report else f"⚠️ Issues: {', '.join(execution_report)}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] {final_status}")
            
            # SAVE=TRUE at the very end to write to the database
            update_acc_signal.emit(acc_id, True, {
                "status": final_status,
                "last_date": self.general_function.current_date_time()
            })
            return driver

        except Exception as e:
            final_status = f"❌ Crashed: {str(e)[:30]} | 🟢 Last: {last_milestone}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] {final_status}")
            print(f"❌ Crashed: {str(e)} | 🟢 Last: {last_milestone}")
            
            # SAVE=TRUE to remember it crashed
            update_acc_signal.emit(acc_id, True, {
                "status": final_status,
                "last_date": self.general_function.current_date_time()
            })
            return driver

    def map_dynamic_tabs(self, bot, update_ld_signal, ld_name):
        dynamic_tabs = {}
        try:
            tab_elements = bot.find_elements('//*[contains(@content-desc, ", tab ")]', timeout=5)

            if not tab_elements:
                update_ld_signal.emit(ld_name, "⚠️ No tabs found!")
                return dynamic_tabs

            for backup_index, element in enumerate(tab_elements, start=1):
                raw_desc = element.get_attribute("content-desc")
                if not raw_desc: continue

                desc_lower = raw_desc.lower()
                # print(desc_lower)
                match = re.search(r"tab (\d+) of", desc_lower)
                tab_index = int(match.group(1)) if match else backup_index

                def build_tab_xpath(tab_name):
                    return f'//android.view.View[contains(@content-desc, "{tab_name}") and contains(@content-desc, "tab {tab_index}")]'

                if "home" in desc_lower: dynamic_tabs["home"] = {"xpath": build_tab_xpath("Home"), "index": tab_index}
                elif "feeds" in desc_lower: dynamic_tabs["feeds"] = {"xpath": build_tab_xpath("Feeds"), "index": tab_index}
                elif "feed" in desc_lower: dynamic_tabs["home"] = {"xpath": build_tab_xpath("Feed"), "index": tab_index}
                elif "video" in desc_lower or "watch" in desc_lower: dynamic_tabs["video"] = {"xpath": build_tab_xpath("Video"), "index": tab_index}
                elif "friend" in desc_lower: dynamic_tabs["friends"] = {"xpath": build_tab_xpath("Friends"), "index": tab_index}
                elif "marketplace" in desc_lower: dynamic_tabs["marketplace"] = {"xpath": build_tab_xpath("Marketplace"), "index": tab_index}
                elif "notification" in desc_lower: dynamic_tabs["notifications"] = {"xpath": build_tab_xpath("Notifications"), "index": tab_index}
                elif "menu" in desc_lower: dynamic_tabs["menu"] = {"xpath": build_tab_xpath("Menu"), "index": tab_index}
                elif "profile" in desc_lower: dynamic_tabs["profile"] = {"xpath": build_tab_xpath("Profile"), "index": tab_index}
                elif "gaming" in desc_lower: dynamic_tabs["gaming"] = {"xpath": build_tab_xpath("Gaming"), "index": tab_index}

            update_ld_signal.emit(ld_name, "✅ Tabs Mapped")
            return dynamic_tabs

        except Exception as e:
            update_ld_signal.emit(ld_name, f"❌ Tab Map Error: {e}")
            print(f"❌ Tab Map Error: {e}")
            return {}
 
    def ensure_on_home(self, appium_name, bot, tab_bar_xpaths, stop_event):
        for attempt in range(4):
            if stop_event.is_set(): return False

            self.goto_via_deeplink(appium_name, "fb://home")
            
            if  bot.wait_any(tab_bar_xpaths, timeout=1.0):
                return True
                
            bot.press_back()
            bot.wait(0.5)

            if  bot.wait_any(tab_bar_xpaths, timeout=1.0):
                return True
            
            try:
                if bot.driver.current_package != "com.facebook.katana":
                    bot.driver.activate_app("com.facebook.katana") 
                    bot.wait(2)
            except Exception: pass 
 
        return False

    def build_reaction_pool(self, main_name: str = None):
        pool = []
        reactions = [
            ("like", "Like"), 
            ("love", "Love"), 
            ("haha", "Haha"), 
            ("cry", "Care"), 
            ("angry", "Angry")
        ]
        
        for base_key, emoji_name in reactions:
            prefixed_key = f"{main_name}_{base_key}" if main_name else base_key
            is_active = self.actives_settings.get(prefixed_key) or self.actives_settings.get(base_key)
            
            if is_active:
                actual_key = prefixed_key if self.actives_settings.get(prefixed_key) is not None else base_key
                
                # 🟢 SAFELY GET AND CONVERT TO INTEGERS
                count_from = int(self.actives_settings.get(f"{actual_key}_from", 0))
                count_to = int(self.actives_settings.get(f"{actual_key}_to", 0))
                
                # 🟢 USE MIN() AND MAX() TO PREVENT CRASHES
                count = random.randint(min(count_from, count_to), max(count_from, count_to))
                
                pool.extend([emoji_name] * count)
        
        random.shuffle(pool)
        return pool

    def get_dynamic_tab(self, bot, update_ld_signal, ld_name):
        found = False
        for _ in range(6):
            tab_elements = '//*[contains(@content-desc, ", tab ")] '
            if bot.exists_xpath(tab_elements, timeout=10):
                found = True
                break
           
        if not found:
            msg = "❌ Tab Facebook not Found"
            return False, msg
        
        dynamic_tabs = self.map_dynamic_tabs(bot, update_ld_signal, ld_name)
        if dynamic_tabs is None: 
            msg = "❌ Tab Facebook not Found"
            return False, msg
        
        tab_bar_xpaths = [data["xpath"] for name, data in dynamic_tabs.items()]

        return dynamic_tabs, tab_bar_xpaths

    def is_content_btn_bar(self, bot):
        return (bot.exists_xpath(self.fs_comment_xpath, timeout=3) and bot.exists_xpath(self.fs_share_xpath, timeout=3))

    def is_videos_tab(self, bot):
        videos_bar_search_btn = '//android.view.ViewGroup[@content-desc="Videos search results"]'
        video_current = '//android.widget.ImageView[@content-desc="Play current video"]'
        found = False
        for _ in range(1):
            if bot.exists_xpath(self.sound_icon_xpath, timeout=1) and self.is_content_btn_bar(bot) or bot.exists_xpath(videos_bar_search_btn, timeout=1) and self.is_content_btn_bar(bot) or bot.exists_xpath(video_current, timeout=1):
                return True
            bot.scroll_down(speed_ms=2000)
            bot.wait(1)
        if not found: 
            if self.is_fullscreen_video(bot):
                print("see is full screen video click back1 and find again")
                bot.click_xpath(self.fs_back_xpath, timeout=1)
                for _ in range(1):
                    if bot.exists_xpath(self.sound_icon_xpath, timeout=1) and self.is_content_btn_bar(bot):
                        return True
                    bot.scroll_down(speed_ms=2000)
                    bot.wait(1)
                
                if bot.exists_xpath(videos_bar_search_btn, timeout=1):
                    bot.click_xpath(videos_bar_search_btn)
                    for _ in range(1):
                        if self.is_content_btn_bar(bot):
                            print("found like comment share return true")
                            return True
                        bot.scroll_down(speed_ms=2000)
                        bot.wait(1)

        return False

    def is_fullscreen_video(self, bot):
        has_back = bot.exists_xpath(self.fs_back_xpath, timeout=1)
        has_optional = bot.wait_any([self.fs_search_xpath, self.fs_reels_prof_xpath, self.fs_create_reels_xpath], timeout=1) is not None
        return has_back and self.is_content_btn_bar(bot)  and has_optional

    def goto_tab_with_search(self, acc_id, ld_name, bot, update_ld_signal, dynamic_tabs, tab_key, search_fallback_text, verification_func):
        # 1. Try Direct Tab Click
        if tab_key in dynamic_tabs:
            bot.safe_click_tab(dynamic_tabs[tab_key]["xpath"], target_tab_index=dynamic_tabs[tab_key]["index"])
            bot.wait(1)
            if verification_func(bot):
                return True
                
        # 2. Hard Recovery via Menu Search Fallback
        menu_tab = dynamic_tabs.get("menu")
        
        if menu_tab:
            bot.safe_click_tab(menu_tab["xpath"], target_tab_index=menu_tab["index"])
            bot.wait(1)
            
            if bot.menu_search_fallback(search_fallback_text, self.search_btn, self.search_xpath):
                bot.wait(4)
                if verification_func(bot):
                    return True
                    
        return False
    
    def goto_profile_from_menu(self, bot, dynamic_tabs):
        """
        Navigates to the Profile from the Menu tab.
        Placed in active_tab.py to keep navigation logic centralized.
        """
        # Navigate to the Menu
        bot.safe_click_tab(dynamic_tabs["menu"]["xpath"], target_tab_index=dynamic_tabs["menu"]["index"])
        bot.wait(2)
        
        # Click the profile row banner (Universal match)
        profile_row_xpath = '//android.view.ViewGroup[contains(@content-desc, "see your profile")]'
        
        if bot.exists_xpath(profile_row_xpath, timeout=5):
            bot.click_xpath(profile_row_xpath)
            bot.wait(2)
        profile_verification = '//android.view.View[@content-desc="Add to story"] | //android.view.View[@content-desc="Edit profile"]'

        if bot.exists_xpath(profile_verification, timeout=5):
            return True
        return False


    # =====================================================================
    # STORY MODULE HELPERS
    # =====================================================================

    def _hunt_and_enter_reel(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        """Scrolls the video feed to find a reel. Uses video-specific geometric fallbacks."""
        total_attempts = 0
        scrolls_since_reset = 0
        max_attempts = 3
        
        while total_attempts < max_attempts:
            if stop_event.is_set(): return False

            if self.is_fullscreen_video(bot):
                return True
            
            # ==========================================
            # 1. SMART GEOMETRIC TARGETING
            # ==========================================
            target_y = None
            center_x = bot.size['width'] // 2
            
            # STRATEGY A: Look for elements that ONLY exist on Videos!
            video_specific_xpaths = [
                '//android.widget.ImageView[@content-desc="Play current video"]',
                self.sound_icon_xpath,
                '//android.view.ViewGroup[@content-desc="Video player"]',
                '//android.widget.ImageView[@content-desc="Play" or @content-desc="Pause"]'
            ]
            
            for xpath in video_specific_xpaths:
                elements = bot.find_elements(xpath, timeout=1)
                if elements:
                    rect = elements[0].rect
                    target_y = rect['y'] + (rect['height'] // 2)
                    break # Stop looking, we found a guaranteed video!
                
            # STRATEGY B: Last Resort - The Like Button 
            # (Only runs if Facebook completely hides ALL video elements)
            if not target_y:
                feed_like_xpath = '//android.view.ViewGroup[contains(@content-desc, "Like button") or contains(@text, "Like")]'
                like_btns = bot.find_elements(feed_like_xpath, timeout=1)
                if like_btns:
                    target_y = like_btns[0].rect['y'] - int(bot.size['height'] * 0.25)

            # Safety check: Ensure target_y is on the screen
            if target_y:
                target_y = max(100, min(target_y, bot.size['height'] - 100))
            else:
                target_y = int(bot.size['height'] * 0.40) # Blind tap upper-middle if absolutely nothing is found

            # ==========================================
            # 2. EXECUTE TAP AND VERIFY
            # ==========================================
            try:
                bot.tap(center_x, target_y)
                bot.wait(1.5) # Wait for UI to change
                
                if self.is_fullscreen_video(bot):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Successfully entered Full-Screen View!")
                    return True
                else:
                    # If it accidentally clicked a picture or ad, it will instantly back out!
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Clicked a picture/ad. Backing out...")
                    bot.press_back()
                    bot.wait(1.5)
            except Exception as e:
                print(f"Error tapping video: {e}")
            
            # ==========================================
            # 3. SCROLL OR RECOVER LOGIC
            # ==========================================
            scrolls_since_reset += 1
            total_attempts += 1
            
            if scrolls_since_reset >= 3:
                update_acc_signal.emit(acc_id, False, {"status": "🔄 Refreshing feed to find a Reel..."})
                
                # 🟢 UPDATED: Recover to home, then use your smart search method!
                if self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
                    self.goto_tab_with_search(
                        acc_id, ld_name, bot, update_ld_signal, dynamic_tabs, 
                        tab_key="video", 
                        search_fallback_text="Reels ", 
                        verification_func=self.is_fullscreen_video
                    )
                
                bot.wait(1.5)
                scrolls_since_reset = 0 
            else:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ➡️ Scrolling to find next video... ({scrolls_since_reset}/3)")
                bot.scroll_down(speed_ms=1200)
                bot.wait(1.5)

        return False
    
    def is_story_viewer_active(self, bot):
        """Shared helper to quickly verify if the bot is currently viewing a story."""
        story_reply_xpath = '//android.view.ViewGroup[contains(@content-desc,"Reply to")]'
        story_options_xpath = '//android.view.ViewGroup[@content-desc="More options for this item"]'
        story_close_xpath = '//android.view.ViewGroup[contains(@content-desc, "Close") or @content-desc="Back"]'
        return bot.wait_any([story_options_xpath, story_close_xpath, story_reply_xpath], timeout=0.5) is not None

    def smart_find_and_open_story(self, appium_name, bot, dynamic_tabs, stop_event):
        """Hunts for the stories tray and clicks the first available story."""
        story_container_xpath = '//android.view.ViewGroup[@content-desc="Stories"]'
        home_tab_xpath = '//android.view.ViewGroup[contains(@content-desc, "tab 1 of")]'
        
        self.goto_via_deeplink(appium_name, "fb://home")

        # Snap to Top
        top_feed_anchor = '//android.view.ViewGroup[contains(@content-desc, "Make a post") or contains(@content-desc, "Go to profile")]'
        if not (bot.exists_xpath(top_feed_anchor, timeout=1) and bot.exists_xpath(home_tab_xpath, timeout=1)):
            if "home" in dynamic_tabs:
                bot.safe_click_tab(dynamic_tabs["home"]["xpath"], target_tab_index=dynamic_tabs["home"]["index"])
        
        # Triangulation Attempt 1: Direct Stories Container
        elements = bot.find_elements(story_container_xpath, timeout=2)
        if elements:
            rect = elements[0].rect
            bot.tap(rect['x'] + (rect['width'] // 2), rect['y'] + (rect['height'] // 2))
            bot.wait(0.5)
            if self.is_story_viewer_active(bot): return True

        # Triangulation Attempt 2: Math from "Create Story"
        create_story = bot.find_elements('//android.view.ViewGroup[@content-desc="Create story"]', timeout=1.5)
        if create_story:
            rect = create_story[0].rect
            bot.tap(rect['x'] + rect['width'] + int(bot.size['width'] * 0.25), rect['y'] + rect['height']//2)
            bot.wait(0.5)
            if self.is_story_viewer_active(bot): return True
        
        # Triangulation Attempt 3: Math from "Make a post"
        make_post = bot.find_elements('//android.view.ViewGroup[contains(@content-desc, "Make a post")]', timeout=1.5)
        if make_post:
            rect = make_post[0].rect
            bot.tap(bot.size['width'] // 4, rect['y'] + rect['height'] + int(bot.size['height'] * 0.18))
            bot.wait(0.5)
            if self.is_story_viewer_active(bot): return True
            
        return False

    def recover_story_viewer(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event): 
        """Recovers the bot if it accidentally falls out of the story viewer."""
        if stop_event.is_set(): return False
        
        if self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Pulling to refresh feed...")
            bot.pull_to_refresh()
            bot.wait(3) # Give network time to load new feed
            return self.smart_find_and_open_story(appium_name, bot, dynamic_tabs, stop_event)
        return False

    def process_stories(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Starting Story Module")
        update_acc_signal.emit(acc_id, False, {"status": "📖 Running Watch Story..."})
        
        try:
            # 1. SETUP TARGETS & QUEUES
            target_stories = random.randint(
                self.actives_settings.get("story_from", 0),
                self.actives_settings.get("story_to", 0)
            )
            
            if target_stories <= 0:
                return True, "No story targets configured"

            do_reply = self.actives_settings.get("reply_story")
            target_replies = 0
            reply_pool = []

            if do_reply:
                target_replies = random.randint(
                    self.actives_settings.get("reply_story_from", 0),
                    self.actives_settings.get("reply_story_to", 0)
                )
                raw_text = self.actives_settings.get("reply_story_text", "")
                try: raw_text = raw_text.plaintext
                except AttributeError: raw_text = str(raw_text)
                    
                reply_pool = [t.strip() for t in raw_text.split(",") if t.strip()]
                if not reply_pool: target_replies = 0

            update_ld_signal.emit(ld_name, f"[{acc_id}] 📸 Stories: {target_stories} | Replies: {target_replies}")

            story_reply_xpath = '//android.view.ViewGroup[contains(@content-desc,"Reply to")]'

            def build_story_reaction_pool():
                pool = []
                mapping = {"reply_story_like": 0, "reply_story_love": 1, "reply_story_cry": 2, "reply_story_haha": 3, "reply_story_angry": 6}
                for key, emoji_index in mapping.items():
                    if self.actives_settings.get(key):
                        count = random.randint(self.actives_settings.get(f"{key}_from", 0), self.actives_settings.get(f"{key}_to", 0))
                        pool.extend([emoji_index] * count)
                random.shuffle(pool)
                return pool

            # 2. START THE MODULE (Using Class Helper)
            if not self.smart_find_and_open_story(appium_name, bot, dynamic_tabs, stop_event):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Stories tray not visible. Skipping module.")
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return False, "Stories tray not visible"

            # 3. MAIN STORY WATCHING LOOP
            stories_watched = 0
            replies_done = 0
            reaction_pool = build_story_reaction_pool()
            w, h = bot.size['width'], bot.size['height']

            while stories_watched < target_stories:
                # 🛑 Quick exit if user clicks stop
                if stop_event.is_set(): 
                    return False, "🛑 Stopped by user"


                update_acc_signal.emit(acc_id, False, {"status": f"📖 Watching Story {stories_watched + 1}/{target_stories}..."})
                
                update_ld_signal.emit(ld_name, f"[{acc_id}] 👀 Viewing Story {stories_watched + 1}/{target_stories}")


                # B. REPLY
                if do_reply and replies_done < target_replies and reply_pool:
                    try:
                        if bot.exists_xpath(story_reply_xpath, timeout=1):
                            bot.click_xpath(story_reply_xpath)
                            
                            edit_text_xpath = '//android.widget.EditText'
                            if bot.exists_xpath(edit_text_xpath, timeout=2):
                                selected_reply = random.choice(reply_pool)
                                bot.type_xpath(edit_text_xpath, selected_reply)

                                send_btn_ui = 'new UiSelector().className("android.widget.Button").descriptionMatches("(?i)send")'
                                if bot.exists_ui(send_btn_ui, timeout=2):
                                    bot.click_ui(send_btn_ui)
                                    replies_done += 1
                                    update_ld_signal.emit(ld_name, f"[{acc_id}] 💬 Replied: '{selected_reply}' ({replies_done}/{target_replies})")
                                    bot.wait(1.5) 
                                else:
                                    bot.press_back()
                    except Exception as e:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Reply failed: {str(e).split(chr(10))[0][:30]}")
                        bot.press_back()

                # C. REACT
                do_react = False
                if self.actives_settings.get("reply_story_no_emoji"): do_react = False
                elif self.actives_settings.get("reply_story_alway_emoji"): do_react = True
                else: do_react = random.choice([True, False])

                if do_react:
                    if not reaction_pool: reaction_pool = build_story_reaction_pool()
                    if reaction_pool:
                        next_reaction_index = reaction_pool.pop(0)
                        if bot.react_to_story(next_reaction_index):
                            update_ld_signal.emit(ld_name, f"[{acc_id}] 👍 Reacted to Story (Index {next_reaction_index}).")
               

                # D. MOVE NEXT
                stories_watched += 1
                if stories_watched >= target_stories:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🎯 Target of {target_stories} stories reached. Exiting.")
                    break

                update_ld_signal.emit(ld_name, f"[{acc_id}] ➡️ Moving to next story...")
                bot.tap(w * 0.90, h * 0.50) # Safe middle-right tap

                # E. AD SKIPPER / RECOVERY (Using Class Helper)
                if not self.is_story_viewer_active(bot):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Verification failed. Checking for Ad/Loading...")
 
                    
                    if self.is_story_viewer_active(bot): continue
                        
                    # Soft Recovery (Ad Skipper)
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⏭️ Attempting Soft Recovery (Skipping Ad)...")
                    bot.tap(w * 0.90, h * 0.50)
        
                    
                    if self.is_story_viewer_active(bot):
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Ad skipped! Recovered organically.")
                        continue

                    # Hard Recovery
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Lost story view. Executing Hard Recovery...")
                    if not self.recover_story_viewer(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Fatal: Could not recover Story Viewer. Skipping remaining.")
                        self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                        return False, f"Lost story view after {stories_watched} stories"

            # 4. FINAL CLEANUP & RETURN
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎉 Stories Module Complete! (Watched: {stories_watched} | Replies: {replies_done})")
            
            # Back out safely
            bot.press_back()
            bot.wait(1)
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            
            return True, f"Watched {stories_watched}, Replied {replies_done}"
            
        except Exception as e:
            error_msg = f"Story Crash: {str(e).split(chr(10))[0][:40]}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg

    def process_posts_storys(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        """Automates posting Images or Videos to Facebook Stories."""
        # 1. RETRIEVE SETTINGS & VALIDATE
        data = self.data_manager.get_post_setting_by_id(acc_id)
        if not data: return True, "No Story settings found"
            
        storys = data.get("post_storys", {})
        if not storys.get("post_story", False): return True, "Story posting is disabled"

        total_posts = storys.get("total_post_story", 1)
        story_path = storys.get("story_path", "")

        if not os.path.exists(story_path):
            update_acc_signal.emit(acc_id, True, {"status": f"❌ Story folder path invalid"})
            return False, f"Story folder path invalid"

        update_acc_signal.emit(acc_id, False, {"status": f"🎬 Starting Story Posting ({total_posts} target)"})
        posts_count = 0
        
        # Valid extensions for Stories (Supports both Images and Videos)
        valid_exts = (".mp4", ".mov", ".jpg", ".jpeg", ".png", ".webp")
        
        # 2. MAIN LOOP
        try:
            for post_index in range(total_posts):
                if stop_event.is_set(): return False, "Stopped by user"
                
                # 🟢 REFRESH MEDIA LIST EVERY LOOP (Prevents selecting moved files)
                local_files = [
                    os.path.join(story_path, f) for f in os.listdir(story_path)
                    if f.lower().endswith(valid_exts) and os.path.isfile(os.path.join(story_path, f))
                ]
                
                if not local_files:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ No more media in story folder. Stopping.")
                    break

                selected_file = random.choice(local_files)
                file_filename = os.path.basename(selected_file)
                
                update_acc_signal.emit(acc_id, False, {"status": f"🔄 Story Post ({post_index+1}/{total_posts})"})

                # A. INJECT MEDIA (Reusing your ADB injection helper)
                success, msg = self._inject_video_via_adb(acc_id, ld_name, appium_name, selected_file, update_acc_signal, update_ld_signal, post_index, total_posts)
                if not success: return False, msg
                bot.wait(2)
                
                # B. NAVIGATE TO HOME FEED
                # We teleport to 'home' to guarantee the "Create story" button is visible at the very top
                self.goto_via_deeplink(appium_name, "home") 
                bot.wait(3)
                
                bot.pull_to_refresh() # Ensure UI resets
                bot.wait(2)
                
                # C. CLICK 'CREATE STORY'
                create_story_btn = '//android.view.ViewGroup[@content-desc="Create story"]'
                if not bot.exists_xpath(create_story_btn, timeout=4):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ 'Create story' button not found.")
                    continue
                    
                bot.click_xpath(create_story_btn)
                bot.wait(1)
                
                # D. SELECT MEDIA FROM GALLERY

                all_dismiss_buttons = f"{self.allow_btn} | {self.continue_btn}"
                for _ in range(3):
                    if bot.exists_xpath(all_dismiss_buttons, timeout=0.5):
                        bot.click_xpath(all_dismiss_buttons)
                        bot.wait(0.5)
                    else:
                        break
                # Since we just injected it via ADB, it will be the VERY FIRST item in the gallery!
                media_item_xpath = '//android.view.ViewGroup[contains(@content-desc, "Photo taken") or contains(@content-desc, "Video")]'
                media_elements = bot.find_elements(media_item_xpath, timeout=4)
                
                if not media_elements:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Could not find injected media in gallery.")
                    bot.press_back() # Escape gallery
                    continue
                    
                # Click the newest media (Index 0)
                media_elements[0].click()
                bot.wait(3)
                
                # E. SHARE STORY
                share_btn = '//android.widget.Button[@content-desc="Share"] | //android.view.ViewGroup[@content-desc="Share"]'
                if not bot.exists_xpath(share_btn, timeout=4):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ 'Share' button not found.")
                    if media_elements:
                        bot.tap_percentage(90, 90)
                    else:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ 'Share' button not found.")
                        continue
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Uploading Story...")
                    bot.click_xpath(share_btn)
                    
                        
                
                # Wait for story upload to complete (Videos take a bit longer, so 15s is safe)
                bot.wait(15) 
                
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Story {post_index+1} posted!")
                posts_count += 1
                
                # F. MOVE FILE TO 'posted' FOLDER
                try:
                    posted_folder = os.path.join(story_path, "posted")
                    if not os.path.exists(posted_folder): 
                        os.makedirs(posted_folder)
                    shutil.move(selected_file, os.path.join(posted_folder, file_filename))
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 📁 Media moved to 'posted' folder.")
                except Exception as e:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ File move failed: {e}")

            # FINAL SUMMARY
            final_msg = f"Successfully posted {posts_count} Stories"
            update_acc_signal.emit(acc_id, True, {"status": final_msg})
            return True, final_msg

        except Exception as e:
            error_msg = f"Post Story Crash: {str(e)}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            update_acc_signal.emit(acc_id, True, {"status": f"❌ {error_msg}"})
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg







    def process_home_feed(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Starting Home Feed Module")
        update_acc_signal.emit(acc_id, False, {"status": "📰 Running Home Feed..."})
        try:
            # ---------------------------------------------------------
            # 1. SETUP TARGETS & POOLS
            # ---------------------------------------------------------
            do_add = self.actives_settings.get("add_friends")
            target_adds = random.randint(
                self.actives_settings.get("add_friends_from", 0),
                self.actives_settings.get("add_friends_to", 0)
            ) if do_add else 0

            do_comments = self.actives_settings.get("comments")
            target_comments = random.randint(
                self.actives_settings.get("comments_by_text_from", 0),
                self.actives_settings.get("comments_by_text_to", 0)
            ) if do_comments else 0

            # Use Global Helpers to build pools
            reaction_pool = self.build_reaction_pool(None)
            target_reactions = len(reaction_pool)
            comment_pool = []

            # Safe exit if everything is 0
            if target_reactions == 0 and target_comments == 0 and target_adds == 0:
                return True, 0

            update_ld_signal.emit(ld_name, f"[{acc_id}] 🏠 Targets -> Reactions: {target_reactions} | Comments: {target_comments} | Adds: {target_adds}")

            if do_comments:
                raw_data = self.actives_settings.get("comments_text", "")
                try:
                    raw_text = raw_data.plaintext
                except AttributeError:
                    raw_text = str(raw_data)
                
                comment_pool = [c.strip() for c in raw_text.split(",") if c.strip()]
                if not comment_pool:
                    target_comments = 0 

            adds_done = 0
            reactions_done = 0
            comments_done = 0

            # ---------------------------------------------------------
            # 2. INITIALIZE & VERIFY HOME FEED
            # ---------------------------------------------------------
            if not self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Fatal: Could not establish Home Feed base. Skipping Feed module.")
                return False, "Failed to establish Home Feed base"

            # ---------------------------------------------------------
            # 3. FEED SCROLLING (MULTI-TASKING LOOP)
            # ---------------------------------------------------------
            max_swipes = max(20, (target_reactions + target_comments + target_adds) * 3) 
            swipes_done = 0
            
            # Dual-locators for maximum compatibility across FB app versions
            like_btn_xpath = '//android.view.ViewGroup[contains(@content-desc, "Like button")] | //android.widget.Button[contains(@content-desc, "Like button")]'
            inline_add_xpath = '//android.view.ViewGroup[@content-desc="Add friend"] | //android.widget.Button[@content-desc="Add friend"]'

            while swipes_done < max_swipes:
                if stop_event.is_set(): return False
                    
                # UI SPAM REDUCTION: Only update the UI table every 5 swipes
                if swipes_done % 5 == 0 and swipes_done > 0:
                    update_acc_signal.emit(acc_id, False, {"status": f"📰 Scrolling Home Feed (Swipe {swipes_done})..."})

                # Exit early if ALL targets are met
                if (len(reaction_pool) == 0 or reactions_done >= target_reactions) and (not do_comments or comments_done >= target_comments):
                    break

                # --- A. ACTION 1: INLINE ADD FRIEND ---
                if do_add and adds_done < target_adds:
                    add_btns = bot.find_elements(inline_add_xpath, timeout=1)
                    if add_btns:
                        for btn in add_btns:
                            if adds_done >= target_adds: break
                            try:
                                btn.click()
                                adds_done += 1
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ➕ Added friend from Feed ({adds_done}/{target_adds})")
                                bot.wait(1) 
                            except Exception:
                                break

                # --- B. ACTION 2: POST REACTIONS ---
                if len(reaction_pool) > 0 and reactions_done < target_reactions:
                    like_visible = bot.exists_xpath(like_btn_xpath, timeout=1)
                    
                    if like_visible:
                        next_reaction = reaction_pool.pop(0) 
                        if bot.react_to_post(reaction_type=next_reaction):
                            reactions_done += 1
                            update_ld_signal.emit(ld_name, f"[{acc_id}] 👍 Sent '{next_reaction}' ({reactions_done}/{target_reactions})...")
                            bot.wait(1)
                        else:
                            reaction_pool.append(next_reaction)

                # --- C. ACTION 3: POST COMMENTS & SMART ESCAPE ---
                if do_comments and comments_done < target_comments and comment_pool:
                    comment_btns = bot.find_elements(self.comment_btn_xpath, timeout=1.5)
                    
                    if comment_btns:
                        try:
                            comment_btns[0].click()
                            bot.wait(1.5) 
                            
                        
                            if bot.exists_xpath(self.comment_input_xpath, timeout=2):
                                selected_comment = random.choice(comment_pool)
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ✍️ Typing comment: '{selected_comment[:15]}...'")
                                
                                bot.type_xpath(self.comment_input_xpath, selected_comment)
                                
                                send_btn_ui = 'new UiSelector().descriptionMatches("(?i)send")'
                                if bot.exists_ui(send_btn_ui, timeout=2):
                                    bot.click_ui(send_btn_ui)
                                    comments_done += 1
                                    update_ld_signal.emit(ld_name, f"[{acc_id}] 💬 Comment sent! ({comments_done}/{target_comments})")
                                    bot.wait(1.5)
                                else:
                                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Send button missing. Aborting comment.")
                            else:
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Comment box did not load. Aborting.")
                                
                        except Exception as e:
                            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Comment interaction failed: {str(e).split(chr(10))[0][:30]}")
                            
                        # 🟢 ULTIMATE SMART ESCAPE LOOP
                        update_ld_signal.emit(ld_name, f"[{acc_id}] 🔙 Exiting comment screen...")
                        
                        feed_recovered = False
                        for _ in range(3):
                            if stop_event.is_set(): return False
                            
                            if bot.exists_xpath(dynamic_tabs["home"]["xpath"], timeout=1.0):
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Safely returned to feed.")
                                feed_recovered = True
                                break
                            else:
                                bot.press_back()
                                bot.wait(1.0)
                                
                        if not feed_recovered:
                            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Trapped in comments. Triggering Global Reset...")
                            if self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
                                bot.safe_click_tab(dynamic_tabs["home"]["xpath"], target_tab_index=dynamic_tabs["home"]["index"])

                # --- D. MOVE TO NEXT POST ---
                bot.scroll_down(speed_ms=200)
                swipes_done += 1
                bot.wait(1)

            # ---------------------------------------------------------
            # 4. FINAL CLEANUP & RETURN
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎉 Feed tasks complete! (Reactions: {reactions_done}, Comments: {comments_done}, Adds: {adds_done})")
            
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            
            return True, adds_done

        except Exception as e:
            error_msg = f"Feed Crash: {str(e).split(chr(10))[0][:40]}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg
    
    def process_friends(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, adds_done_in_feed, dynamic_tabs, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Starting Friends Module")
        update_acc_signal.emit(acc_id, False, {"status": "👥 Running Confirm & Add"})
        try:
            # Initialize trackers early to avoid variable reference errors
            confirms_done = 0
            adds_done = adds_done_in_feed

            # ---------------------------------------------------------
            # 1. SETUP TARGETS & CONDITIONS
            # ---------------------------------------------------------
            do_confirm = self.actives_settings.get("confirm_friends")
            target_confirms = 0
            if do_confirm:
                target_confirms = random.randint(
                    self.actives_settings.get("confirm_friends_from", 0),
                    self.actives_settings.get("confirm_friends_to", 0)
                )

            do_add = self.actives_settings.get("add_friends")
            target_adds = 0
            if do_add:
                target_adds = random.randint(
                    self.actives_settings.get("add_friends_from", 0),
                    self.actives_settings.get("add_friends_to", 0)
                )

            # 🟢 SMART CHECK: Only run if we actually have targets left to hit
            if target_confirms <= 0 and (not do_add or adds_done >= target_adds):
                return True, "No friend targets configured or already hit in feed"


            # ---------------------------------------------------------
            # SMART HELPERS: Verification & Recovery
            # ---------------------------------------------------------
            def is_on_friends():
                """Smartly checks UI clues without crashing the Appium server."""
                indicators = [
                    '//android.view.ViewGroup[@content-desc="Your friends"]',
                    '//android.view.ViewGroup[@content-desc="Suggestions"]',
                    '//android.view.ViewGroup[contains(@content-desc, "See all")]',
                    '//android.widget.TextView[@text="Friends"]'
                ]
                return bot.wait_any(indicators, timeout=1.5) is not None

            def recover_friends_tab():
                """Ironclad 'Return to Base' using the Global Home Reset."""
                if is_on_friends():
                    return True
                    
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Attempting to recover Friends page...")
                
                # 1. Soft Recovery
                for _ in range(3):
                    if stop_event.is_set(): return False
                    bot.press_back()
                    bot.wait(1.5)
                    if is_on_friends():
                        return True
                        
                # 2. Hard Recovery via Global Shield
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Soft recovery failed. Executing Global Home Reset...")
                if self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
                    if "friends" in dynamic_tabs:
                        bot.safe_click_tab(dynamic_tabs["friends"]["xpath"], target_tab_index=dynamic_tabs["friends"]["index"])
                    bot.wait(3)
                    return is_on_friends()
                    
                return False

            # ---------------------------------------------------------
            # 2. INITIAL NAVIGATION
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 👥 Navigating to Friends Tab...")
            if not bot.safe_click_tab(dynamic_tabs["friends"]["xpath"], target_tab_index=dynamic_tabs["friends"]["index"]):
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return False, "Failed to click Friends tab"
                
            bot.wait(2)
            
            if not recover_friends_tab():
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Fatal: Could not verify Friends page. Skipping module.")
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return False, "Could not load or verify the Friends tab"

            # ---------------------------------------------------------
            # 3. PART A: CONFIRM FRIENDS
            # ---------------------------------------------------------
            if do_confirm and target_confirms > 0:
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🤝 Searching for Friend Requests...")
                empty_scrolls = 0
                
                # Catch both ViewGroups and Buttons!
                confirm_xpath = '//android.view.ViewGroup[starts-with(@content-desc, "Confirm")] | //android.widget.Button[starts-with(@content-desc, "Confirm")]'
                
                while confirms_done < target_confirms and empty_scrolls < 1:
                    if stop_event.is_set(): return False
                    
                    # UI SPAM REDUCTION: Only update the UI table occasionally
                    if confirms_done % 5 == 0 and confirms_done > 0:
                        update_acc_signal.emit(acc_id, False, {"status": f"🤝 Confirming Friends ({confirms_done}/{target_confirms})..."})
                        
                    confirm_btns = bot.find_elements(confirm_xpath, timeout=2)
                    
                    if confirm_btns:
                        empty_scrolls = 0 
                        for btn in confirm_btns:
                            if confirms_done >= target_confirms: 
                                break
                            try:
                                btn.click()
                                confirms_done += 1
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Confirmed request ({confirms_done}/{target_confirms})")
                                bot.wait(random.uniform(1.0, 1.5))
                            except Exception:
                                break 
                    else:
                        empty_scrolls += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ➡️ No requests found. Scrolling down...")
                        bot.scroll_down(speed_ms=100)
                        bot.wait(1.5)
                        
                        # 🟢 SAFEGUARD: Check if we accidentally clicked a profile while scrolling
                        if not is_on_friends():
                            if not recover_friends_tab():
                                return False, "Lost Friends view while scrolling confirmations"
                        
                if confirms_done == 0:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🤷 No friend requests available to confirm.")

            # ---------------------------------------------------------
            # 4. PART B: FINISH ADDING FRIENDS (Suggestions)
            # ---------------------------------------------------------
            if do_add and adds_done < target_adds:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ➕ Finishing Adds... ({adds_done}/{target_adds} total)")
                
                # Snap back to top of the Friends tab
                bot.safe_click_tab(dynamic_tabs["friends"]["xpath"], target_tab_index=dynamic_tabs["friends"]["index"])
                bot.wait(2)
                
                # Click Suggestions if it exists
                suggestions_tab = '//*[@content-desc="Suggestions"]'
                if bot.exists_xpath(suggestions_tab, timeout=2):
                    bot.click_xpath(suggestions_tab)
                    bot.wait(2.5) 
                
                empty_scrolls = 0
                # Catch both ViewGroups and Buttons!
                add_xpath = '//android.view.ViewGroup[starts-with(@content-desc, "Add ")] | //android.widget.Button[starts-with(@content-desc, "Add ")]'
                
                while adds_done < target_adds and empty_scrolls < 2:
                    if stop_event.is_set(): return False

                    # UI SPAM REDUCTION: Only update the UI table occasionally
                    if adds_done % 5 == 0 and adds_done > 0:
                        update_acc_signal.emit(acc_id, False, {"status": f"➕ Adding Friends ({adds_done}/{target_adds})..."})
                        
                    add_btns = bot.find_elements(add_xpath, timeout=2)
                    
                    if add_btns:
                        empty_scrolls = 0 
                        for btn in add_btns:
                            if adds_done >= target_adds: 
                                break
                            try:
                                btn.click()
                                adds_done += 1
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Sent friend request ({adds_done}/{target_adds})")
                                bot.wait(random.uniform(1, 1.5))
                            except Exception:
                                # THE STALE ELEMENT SHIELD
                                break 
                    else:
                        empty_scrolls += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ➡️ No add buttons found. Scrolling down...")
                        bot.scroll_down(speed_ms=300)
                        bot.wait(1.5)
                        
                        # 🟢 SAFEGUARD: Ensure we didn't click into a user profile
                        if not is_on_friends():
                            if not recover_friends_tab():
                                return False, "Lost Friends view while scrolling suggestions"

            # ---------------------------------------------------------
            # 5. FINAL CLEANUP & RETURN
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎉 Friends Module Complete! (Confirmed: {confirms_done} | Added: {adds_done})")
            
            # Escape safely back to the home feed before passing to the next module
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            
            return True, f"Confirmed {confirms_done}, Added {adds_done}"

        except Exception as e:
            error_msg = f"Friends Crash: {str(e).split(chr(10))[0][:40]}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg
    
    def process_notifications(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Starting Notifications Module")
        update_acc_signal.emit(acc_id, False, {"status": "🔔 Running Notifications..."})
        try:
            # ---------------------------------------------------------
            # 1. SETUP TARGETS & LIMITS
            # ---------------------------------------------------------
            do_join = self.actives_settings.get("click_join_group_in_notification")
            do_click_notifs = self.actives_settings.get("total_click_notification")
            
            target_unread = 0
            if do_click_notifs:
                target_unread = random.randint(
                    self.actives_settings.get("total_click_notification_from", 0),
                    self.actives_settings.get("total_click_notification_to", 0)
                )
            
            # Skip if both are disabled or target is 0
            if not do_join and target_unread <= 0:
                return True, "No notification targets configured"

            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔔 Initiating... (Unread: {target_unread}, Join Groups: {do_join})")
            
            join_xpath = '//android.view.ViewGroup[@content-desc="Join"] | //android.widget.Button[@content-desc="Join"]'
            unread_xpath = '//android.view.ViewGroup[contains(@content-desc, "Unread")]' 
            
            # ---------------------------------------------------------
            # SMART HELPERS: Verification & Recovery
            # ---------------------------------------------------------
            def is_on_notifications():
                indicators = [
                    '//android.view.ViewGroup[@content-desc="Notifications"]',
                    '//android.view.ViewGroup[contains(@content-desc, "Mark all") or contains(@content-desc, "Mark All")]',
                    '//android.view.ViewGroup[contains(@content-desc, "Unread")]',
                    '//android.view.ViewGroup[contains(@content-desc, "Earlier")]'
                ]
                return bot.wait_any(indicators, timeout=1.5) is not None

            def recover_notifications_tab():
                if is_on_notifications(): return True
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Attempting to recover Notifications page...")
                
                for _ in range(3):
                    if stop_event.is_set(): return False
                    bot.press_back()
                    bot.wait(1.5)
                    if is_on_notifications(): return True
                        
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Soft recovery failed. Executing Global Home Reset...")
                if self.goto_via_deeplink(appium_name, "notifications"):
                    return is_on_notifications()
                else:
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    if "notifications" in dynamic_tabs:
                        bot.safe_click_tab(dynamic_tabs["notifications"]["xpath"], target_tab_index=dynamic_tabs["notifications"]["index"])
                    bot.wait(3)
                    return is_on_notifications()

            # ---------------------------------------------------------
            # 2. INITIAL NAVIGATION
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔔 Navigating to Notifications Tab...")
            if self.goto_via_deeplink(appium_name, "notifications"):
                return is_on_notifications()
            else:
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                if "notifications" in dynamic_tabs:
                    if not bot.safe_click_tab(dynamic_tabs["notifications"]["xpath"], target_tab_index=dynamic_tabs["notifications"]["index"]):
                        return False, "Failed to navigate to Notifications Tab"
            
            bot.wait(3)
            if not recover_notifications_tab():
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Fatal: Could not open Notifications page. Stopping module.")
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return False, "Could not load or verify Notifications Tab"

            # ---------------------------------------------------------
            # 3. MAIN PROCESSING LOOP
            # ---------------------------------------------------------
            empty_screens_in_a_row = 0
            MAX_EMPTY_SCREENS = 1 
            unread_clicked_count = 0

            while empty_screens_in_a_row < MAX_EMPTY_SCREENS:
                if stop_event.is_set(): return False
                
                if (not do_join or empty_screens_in_a_row >= MAX_EMPTY_SCREENS) and unread_clicked_count >= target_unread:
                    break

                screen_had_action = False

                # --- A. SCAN FOR JOINS ---
                if do_join:
                    join_btns = bot.find_elements(join_xpath, timeout=1.5)
                    if join_btns:
                        try:
                            join_btns[0].click() 
                            bot.wait(2)
                            update_ld_signal.emit(ld_name, f"[{acc_id}] 🤝 Clicked 'Join' Group button.")
                            screen_had_action = True
                            
                            if not recover_notifications_tab():
                                return False, "Lost context after clicking Join"
                            empty_screens_in_a_row = 0
                            continue 
                        except Exception: pass

                # --- B. SCAN FOR UNREADS ---
                if target_unread > 0 and unread_clicked_count < target_unread:
                    if not screen_had_action: 
                        unread_items = bot.find_elements(unread_xpath, timeout=1.5)
                        if unread_items:
                            try:
                                unread_items[0].click()
                                unread_clicked_count += 1
                                
                                # UI SPAM REDUCTION: Status update only for unreads
                                update_acc_signal.emit(acc_id, False, {"status": f"🔔 Reading Notification {unread_clicked_count}/{target_unread}..."})
                                
                                watch_delay = random.uniform(2.0, 3.0)
                                bot.wait(watch_delay) 
                                
                                if not recover_notifications_tab():
                                    return False, f"Lost context after reading {unread_clicked_count} notifications"
                                    
                                empty_screens_in_a_row = 0
                                continue 
                            except Exception: pass

                # --- C. SCROLL LOGIC ---
                empty_screens_in_a_row += 1
                update_ld_signal.emit(ld_name, f"[{acc_id}] ➡️ Scrolling... ({empty_screens_in_a_row}/{MAX_EMPTY_SCREENS})")
                bot.scroll_down(speed_ms=1000)
                bot.wait(0.5)

            # ---------------------------------------------------------
            # 4. FINAL CLEANUP
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎉 Notification tasks complete! (Read: {unread_clicked_count})")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, f"Read {unread_clicked_count} notifications"

        except Exception as e:
            error_msg = f"Notifs Crash: {str(e).split(chr(10))[0][:40]}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg


    # =====================================================================
    # CHAT MODULE HELPERS
    # =====================================================================
    def _nav_to_messenger(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        """Safely navigates to the Messenger inbox, clearing popups along the way."""
        messaging_xpath = '//android.widget.Button[@content-desc="Messaging"] | //android.widget.Button[contains(@content-desc, "conversations")]/android.view.View'
        setting = '//android.view.ViewGroup[@content-desc="Settings"]'
        new_setting = '//android.view.ViewGroup[@content-desc="New message"]'
        fs_back_xpath = '//android.view.ViewGroup[@content-desc="Back"]'
        search_field = '//android.view.ViewGroup[@content-desc="Search field"]'

        popup_xpaths = [
            '//android.view.ViewGroup[starts-with(@content-desc, "Dismiss")]',
            '//android.view.ViewGroup[@content-desc="Chat on Facebook"]',
            '//android.view.ViewGroup[@content-desc="OK"]',
            '//android.widget.Button[@text="OK"]',
            '//android.view.ViewGroup[@content-desc="Close"]',
            '//android.widget.ImageView[@content-desc="Close"]',
            '//android.view.View[@content-desc="Skip"] |',
            '//android.widget.Button[contains(@text, "Skip") or contains(@text, "Skip") or contains(@text, "SKIP")]',
            '//android.view.ViewGroup[@content-desc="SKIP"]'
        ]

        for entry_attempt in range(3):
            if stop_event.is_set(): return False
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Attempt {entry_attempt + 1}/3 to enter Messenger")

            if self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
                if "home" in dynamic_tabs:
                    bot.safe_click_tab(dynamic_tabs["home"]["xpath"], target_tab_index=dynamic_tabs["home"]["index"])
                bot.wait(1)
            else:
                return False

            if bot.exists_xpath(messaging_xpath, timeout=2.5):
                bot.click_xpath(messaging_xpath)
            else:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Messaging button hidden. Tapping top-right corner")
                w, h = bot.size['width'], bot.size['height']
                bot.tap(w * 0.95, h * 0.05)
            bot.wait(3) 

            # VERIFY SCREEN & CLEAR POPUPS
            for attempt in range(6): 
                if bot.exists_xpath(search_field, timeout=1) and bot.exists_xpath(fs_back_xpath, timeout=1) and bot.exists_xpath(new_setting, timeout=1) and bot.exists_xpath(setting, timeout=1):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Verified: Chat Inbox found.")
                    bot.wait(1)
                    return True
                
                found_xpath = bot.wait_any(popup_xpaths, timeout=1.5)
                if found_xpath:
                    bot.click_xpath(found_xpath)
                    bot.wait(2)

            # Hard Fallback
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Standard verification failed. Attempting Hard Fallback tap...")
            w, h = bot.size['width'], bot.size['height']
            bot.tap(w * 0.05, h * 0.05)
            bot.wait(2)
            
            if bot.exists_xpath(search_field, timeout=1) and bot.exists_xpath(fs_back_xpath, timeout=1):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Hard fallback succeeded!")
                return True

        return False

    def _send_chat_text(self, acc_id, ld_name, bot, update_ld_signal, comment_pool, edit_text_ui):
        """Selects a random comment from the pool and sends it."""
        try:
            selected_text = random.choice(comment_pool)
            bot.click_ui(edit_text_ui)
            bot.type_ui(edit_text_ui, selected_text)
            
            send_btn_xpath = '//android.view.ViewGroup[@content-desc="Send" or @content-desc="SEND"]'
            if bot.exists_xpath(send_btn_xpath, timeout=1.5):
                bot.click_xpath(send_btn_xpath)
                bot.wait(1)
                return True
        except Exception as e:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Text send failed: {str(e)[:30]}")
        return False

    def _send_chat_sticker(self, acc_id, ld_name, bot, update_ld_signal, sticker_xpath_pool):
        """Opens the sticker menu, attempts to send a random sticker, falls back to Moodies or safe tap."""
        open_sticker = '//android.view.ViewGroup[contains(@content-desc, "Open sticker")]'
        if bot.exists_xpath(open_sticker, timeout=2):
            bot.click_xpath(open_sticker)
            bot.wait(1.5)
            
            stickers_tab_xpath = '//android.view.ViewGroup[@content-desc="Stickers"]'
            if bot.exists_xpath(stickers_tab_xpath, timeout=2):
                bot.click_xpath(stickers_tab_xpath)
                bot.wait(2.5) 
                
                random_sticker_xpath = random.choice(sticker_xpath_pool)
                
                # Primary Attempt
                if bot.exists_xpath(random_sticker_xpath, timeout=2):
                    bot.click_xpath(random_sticker_xpath)
                    bot.wait(2)
                    return True
                else:
                    # Fallback Attempt
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Sticker not found. Trying 'Moodies' pack...")
                    moodies_tab_xpath = '//android.view.ViewGroup[@content-desc="Moodies"]'
                    if bot.exists_xpath(moodies_tab_xpath, timeout=2):
                        bot.click_xpath(moodies_tab_xpath)
                        bot.wait(2.5) 
                        
                        if bot.exists_xpath(random_sticker_xpath, timeout=2):
                            bot.click_xpath(random_sticker_xpath)
                            bot.wait(2)
                            return True
                    
                    # Hard Fallback
                    bot.tap(bot.size['width'] // 2, int(bot.size['height'] * 0.7))
                    bot.wait(2)
                    return True
        return False

    def process_chat_module(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Starting Chat Module")
        update_acc_signal.emit(acc_id, False, {"status": "💬 Starting Chat Module"})

        try:
            # 1. SETUP TARGETS
            target_texts = 0
            comment_pool = []
            if self.actives_settings.get("chat_by_text"):
                target_texts = random.randint(self.actives_settings.get("chat_by_text_from", 0), self.actives_settings.get("chat_by_text_to", 0))
                raw_comment_data = self.actives_settings.get("chat_text", "")
                try: raw_text = raw_comment_data.plaintext
                except AttributeError: raw_text = str(raw_comment_data)
                comment_pool = [c.strip() for c in raw_text.split(",") if c.strip()]
                if not comment_pool: target_texts = 0

            target_stickers = 0
            if self.actives_settings.get("chat_sticker"):
                target_stickers = random.randint(self.actives_settings.get("chat_sticker_from", 0), self.actives_settings.get("chat_sticker_to", 0))

            total_people_target = max(target_texts, target_stickers)
            if total_people_target <= 0:
                return True, "No chat targets configured"

            update_ld_signal.emit(ld_name, f"[{acc_id}] 💬 Target Chat: {target_texts} Texts | {target_stickers} Stickers")

            # 2. NAVIGATE TO MESSENGER
            if not self._nav_to_messenger(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return False, "Could not verify Chat Inbox after retries"

            # 3. VERIFY INBOX IS NOT EMPTY
            empty_inbox_text = '//android.widget.TextView[@text="Message Your Friends" or contains(@text, "Send and receive")]'
            if bot.exists_xpath(empty_inbox_text, timeout=2):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Inbox is completely empty! Skipping chat module.")
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return True, "Inbox empty, skipped chatting" 

            # 4. MAIN CHAT LOOP
            texts_done = 0
            stickers_done = 0
            people_contacted = 0
            contacted_names = set()
            scroll_attempts = 0
            w, h = bot.size['width'], bot.size['height']

            sticker_xpath_pool = [
                '//android.view.ViewGroup[@content-desc="Sticker, Animated yellow face emoji, grinning and moving its eyes left and right."]',
                '//android.view.ViewGroup[@content-desc="Sticker, Animated yellow face emoji, crying itself into a puddle of tears."]',
                '//android.view.ViewGroup[@content-desc="Sticker, Animated red faced emoji, frowning and looking angry while its head shakes."]',
                '//android.view.ViewGroup[@content-desc="Sticker, Animated yellow face emoji, smiling, with two beating hearts instead of eyes."]',
                '//android.view.ViewGroup[@content-desc="Sticker, Animated pink heart, pulsating, with wide open eyes and grin."]'
            ]
            smart_chat_row_xpath = '//androidx.recyclerview.widget.RecyclerView//android.view.ViewGroup[1][@content-desc and not(contains(@content-desc, "Search")) and not(contains(@content-desc, "Settings")) and not(contains(@content-desc, "Get Messenger")) and not(contains(@content-desc, "Message Your Friends")) and not(contains(@content-desc, "Meta AI"))]'
            edit_text_ui = 'new UiSelector().className("android.widget.EditText").descriptionMatches("(?i).*message.*")'
            fs_back_xpath = '//android.view.ViewGroup[@content-desc="Back"]'
            search_field = '//android.view.ViewGroup[@content-desc="Search field"]'

            while people_contacted < total_people_target:
                if stop_event.is_set(): return False, "Stopped by user"
                
                chat_rows = bot.find_elements(smart_chat_row_xpath, timeout=2)
                found_new_person = False
                
                if chat_rows:
                    for row in chat_rows:
                        try:
                            person_name = row.get_attribute("content-desc")
                            if not person_name or person_name in contacted_names: continue
                            
                            found_new_person = True
                            contacted_names.add(person_name)
                            scroll_attempts = 0 
                            
                            update_ld_signal.emit(ld_name, f"[{acc_id}] 👤 Opening chat with: {person_name[:15]}...")
                            row.click()
                            bot.wait(1.5) 
                            break 
                        except Exception: continue 

                # Scroll Logic
                if not found_new_person:
                    if scroll_attempts >= 3:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Reached absolute bottom of inbox.")
                        break
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⬇️ Scrolling for new people...")
                    bot.swipe(w * 0.5, h * 0.8, w * 0.5, h * 0.4, speed_ms=1400) 
                    bot.wait(1.5)
                    scroll_attempts += 1
                    continue 

                # THE SAFE ENTRY CHECK
                if not bot.exists_ui(edit_text_ui, timeout=2.5):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ False click detected. Validating screen state")
                    if bot.exists_xpath(search_field, timeout=1): continue 
                    else:
                        bot.press_back()
                        bot.wait(1.5)
                        continue
                
                # Inside Chat Popups
                ok_btn = bot.wait_any(['//android.view.ViewGroup[@content-desc="OK"]', '//android.widget.Button[@text="OK"]'], timeout=1)
                if ok_btn: bot.click_xpath(ok_btn)

                # TEXT ACTION
                if texts_done < target_texts and comment_pool:
                    if self._send_chat_text(acc_id, ld_name, bot, update_ld_signal, comment_pool, edit_text_ui):
                        texts_done += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] 💬 Sent Text ({texts_done}/{target_texts})")

                # STICKER ACTION
                if stickers_done < target_stickers:
                    if self._send_chat_sticker(acc_id, ld_name, bot, update_ld_signal, sticker_xpath_pool):
                        stickers_done += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Sticker sent! ({stickers_done}/{target_stickers})")

                # ESCAPE TO INBOX
                if bot.exists_xpath(fs_back_xpath, timeout=1.5): bot.click_xpath(fs_back_xpath)
                else: bot.press_back() 
                bot.wait(1.5)
                
                # Double-check escape
                if bot.exists_ui(edit_text_ui, timeout=1):
                    if bot.exists_xpath(fs_back_xpath, timeout=1): bot.click_xpath(fs_back_xpath)
                    else: bot.press_back()
                    bot.wait(1)

                people_contacted += 1

            # 5. ESCAPE AND RETURN SUCCESS
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎉 Chat Complete! Escaping to Home...")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, f"Contacted {people_contacted} people"

        except Exception as e:
            error_msg = f"Chat Crash: {str(e).split(chr(10))[0][:40]}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg



    def _nav_to_add_email(self, acc_id, ld_name, bot, update_ld_signal, stop_event):
        """Navigates from Settings menu to the 'Add Email' input screen."""
        contact_info = '//android.widget.Button[starts-with(@content-desc, "Contact info")] | //*[starts-with(@content-desc, "Contact info")]'
        add_email_btn = '//android.widget.Button[@content-desc="Add email"]'
        email_xpath = '//android.widget.EditText[@content-desc="Enter email,"] | //android.widget.EditText[contains(@content-desc, "email")]'
        
        for attempt in range(2):
            if stop_event.is_set(): return False
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔍 Navigating to Add Email (Attempt {attempt+1}/2)")
            
            if bot.exists_xpath(email_xpath, timeout=2): return True
                
            if bot.exists_xpath(self.personal_details, timeout=10):
                bot.click_xpath(self.personal_details)
                bot.wait(2)
                
            for _ in range(2):
                if bot.exists_xpath(contact_info, timeout=10):
                    bot.click_xpath(contact_info)
                    bot.wait(2)
                    break
                bot.scroll_down(speed_ms=400)
                bot.wait(2)
                
            if bot.exists_xpath(add_email_btn, timeout=10):
                bot.click_xpath(add_email_btn)
                bot.wait(2)
                
            if bot.exists_xpath(email_xpath, timeout=10):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Add Email screen loaded.")
                return True
            else:
                bot.press_back()
                bot.wait(2)
        return False

    def _find_available_email(self, acc_id, ld_name, bot, update_acc_signal, stop_event):
        """Loops up to 20 times to find a Yandex email that isn't already taken."""
        email_xpath = '//android.widget.EditText[@content-desc="Enter email,"] | //android.widget.EditText[contains(@content-desc, "email")]'
        next_btn = '//android.view.View[@content-desc="Next"] | //android.widget.Button[@content-desc="Next"]'
        already_in_use_xpath = '//android.view.View[contains(@content-desc, "already in use")] | //android.view.View[contains(@content-desc, "can\'t be used")] | //android.view.View[contains(@content-desc, "Try a different")]'
        confirm_code_screen = '//android.widget.EditText[contains(@content-desc, "Code")] | //android.view.View[contains(@content-desc, "Enter the code")] | //android.view.View[contains(@content-desc, "Check your email")]'

        if not bot.exists_xpath(email_xpath, timeout=10): return False, ""

        for email_attempt in range(20):
            if stop_event.is_set(): return False, ""
            
            new_email = self.data_manager.get_next_tracking_email(self.actives_settings.get("yandex_start"))
            update_acc_signal.emit(acc_id, False, {"status": f"📧 Trying Email ({email_attempt+1}/20)"})
            bot.click_xpath(email_xpath) 
            bot.type_xpath(email_xpath, new_email)
            bot.wait(1)
            
            if bot.exists_xpath(next_btn, timeout=2):
                bot.click_xpath(next_btn)
                bot.wait(3) 
                
            if bot.exists_xpath(already_in_use_xpath, timeout=2):
                update_acc_signal.emit(acc_id, False, {"status": f"⚠️ Email {new_email} is taken."})
                continue 
                
            if bot.exists_xpath(confirm_code_screen, timeout=2):
                username, domain = new_email.split('@')
                expected_suffix = f"{username[-1].lower()}@{domain}".lower()
                verify_email_xpath = f'//android.view.View[contains(@content-desc, "Enter the code we sent to") and contains(translate(@content-desc, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{expected_suffix}")]'
                
                if bot.exists_xpath(verify_email_xpath, timeout=2):
                    update_acc_signal.emit(acc_id, False, {"status": f"✅ Email {new_email} is available!"})
                    return True, new_email
                else:
                    update_acc_signal.emit(acc_id, False, {"status": f"📧 Facebook sent the code to an old/different email"})
                    return False, "Facebook sent the code to an old/different email"
                    
        return False, "Exhausted all 20 email attempts"

    def _nav_to_2fa_setup(self, acc_id, ld_name, bot, update_ld_signal, data_acc):
        """Navigates from Settings menu to 2FA Profile Selection."""
        target_name = data_acc.get("name", "")
        pass_sec = '//android.view.View[@content-desc="Password and security"] | //android.widget.Button[@content-desc="Password and security"]'
        two_factor = '//android.widget.Button[@content-desc="Two-factor authentication"] | //android.widget.Button[contains(@content-desc, "Two-factor")]'
        profile_xpath = f'//android.view.ViewGroup[contains(@content-desc, "{target_name}")] | //android.view.ViewGroup[contains(@content-desc, "Facebook")] | //android.view.View[contains(@content-desc, "{target_name}")]'

        for attempt in range(3):
            if bot.exists_xpath(pass_sec, timeout=10):
                bot.click_xpath(pass_sec)
                bot.wait(2)

            if bot.exists_xpath(two_factor, timeout=10):
                bot.click_xpath(two_factor)
                bot.wait(2)

            if bot.exists_xpath(profile_xpath, timeout=10):
                update_ld_signal.emit(ld_name, f"[{acc_id}] 👤 Selecting profile: {target_name}...")
                bot.click_xpath(profile_xpath)
                bot.wait(2) 
                return True
        return False

    def _handle_2fa_barriers(self, acc_id, ld_name, bot, update_acc_signal, update_ld_signal, data_acc):
        """Checks for password prompts, 'Can't setup' blocks, or email verifications before 2FA setup."""
        # Check Password
        password_input = '//android.widget.EditText[contains(@content-desc, "Password")]'
        if bot.exists_xpath(password_input, timeout=3):
            update_acc_signal.emit(acc_id, False, {"status": "🔑 Entering account password"})
            bot.type_xpath(password_input, data_acc.get("password", ""))
            bot.click_xpath(self.continue_btn) # Ensure self.continue_btn is defined in your class
            bot.wait(3) 
            if bot.exists_xpath(self.wrong_pass_error, timeout=2): # Ensure self.wrong_pass_error is defined
                return "FAILED", "Incorrect Password!"
                
        # Check 'Can't Setup' Block
        cannot_setup = '//android.widget.TextView[contains(@text, "This is because we noticed you are using a device")]'
        for _ in range(3):
            if bot.exists_xpath(self.ok_btn, timeout=2) or bot.exists_xpath(cannot_setup, timeout=2):
                bot.click_xpath(self.ok_btn) # Ensure self.ok_btn is defined
        if bot.exists_xpath(self.accounts_center, timeout=2): # Ensure self.accounts_center is defined
            return "FAILED", "This Account Can't Setup 2FA" 

        # Check Email Verification
        email_code_header = '//android.view.View[@content-desc="Enter confirmation code"] | //android.view.View[@content-desc="Get a new code"] | //android.view.View[contains(@content-desc, "We\'ve sent a confirmation code")]'
        if bot.exists_xpath(email_code_header, timeout=3):
            email_address = self.actives_settings.get("yandex_mail")
            app_password = self.actives_settings.get("app_password_yandex")
            if not email_address or not app_password: return "FAILED", "Missing Yandex credentials in data_acc!"

            email_input = '//android.widget.EditText[contains(@content-desc, "Confirmation code")]'
            get_new_code_btn = '//android.view.View[@content-desc="Get a new code"]'
            
            email_verified = False
            for attempt in range(3):
                yandex_code = self.general_function.get_yandex_code(email_address, app_password)
                if yandex_code:
                    bot.type_xpath(email_input, yandex_code)
                    bot.click_xpath('//android.widget.Button[@content-desc="Next" or @content-desc="Continue"]')
                    bot.wait(4)
                    
                    if bot.exists_xpath('//android.view.View[@content-desc="This code doesn\'t work. Check it\'s correct or try a new one."]', timeout=2):
                        if bot.exists_xpath(get_new_code_btn, timeout=1): bot.click_xpath(get_new_code_btn)
                        bot.wait(10) 
                        continue
                    else:
                        email_verified = True
                        break 
                else:
                    if bot.exists_xpath(get_new_code_btn, timeout=1): bot.click_xpath(get_new_code_btn)
                    bot.wait(10)
            if not email_verified: return "FAILED", "Failed to verify email code for 2FA"

        return "SUCCESS", "Barriers cleared"

    def setting_options(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, data_acc, dynamic_tabs, tab_bar_xpaths, stop_event):
        # =========================================================
        # 0. INITIALIZATION & TASK ROUTING (Dual-Signal)
        # =========================================================
        two_fa = False
        add_email = False

        if self.actives_settings.get("get_account_info"):
            update_ld_signal.emit(ld_name, f"[{acc_id}] 📋 Task Queued: Extract Info")
            update_acc_signal.emit(acc_id, False, {"status": "📋 Starting Get Account Primary"})

        if self.actives_settings.get("set_up_mail"):
            if self.actives_settings.get("add_email_yandex"):
                add_email = True
                update_ld_signal.emit(ld_name, f"[{acc_id}] 📋 Task Queued: Add Email")
                update_acc_signal.emit(acc_id, False, {"status": "📋 Starting Add Email"})

            if self.actives_settings.get("two_fa"):
                two_fa = True
                update_ld_signal.emit(ld_name, f"[{acc_id}] 📋 Task Queued: Setup 2FA")
                update_acc_signal.emit(acc_id, False, {"status": "📋 Starting 2FA"})

            if self.actives_settings.get("add_mail_with_two_fa"):
                add_email = True
                two_fa = True
                update_ld_signal.emit(ld_name, f"[{acc_id}] 📋 Task Queued: Email + 2FA")
                update_acc_signal.emit(acc_id, False, {"status": "📋 Starting Add Email and 2FA"})


        # 🟢 CRITICAL FIX: Ensure emails and phones are initialized as LISTS
        existing_email = data_acc.get("email")
        existing_phone = data_acc.get("phone_number")
        
        extracted_data = {
            "name": "",
            "birthday": "",
            "emails": [existing_email] if existing_email and isinstance(existing_email, str) else (existing_email if isinstance(existing_email, list) else []),
            "phones": [existing_phone] if existing_phone and isinstance(existing_phone, str) else (existing_phone if isinstance(existing_phone, list) else [])
        }

        try:
            # =========================================================
            # 1. BASE NAVIGATION TO ACCOUNTS CENTER
            # =========================================================
            nav_success = False
            settings_gear = '//android.view.ViewGroup[@content-desc="Settings"] | //android.widget.Button[@content-desc="Settings"]'

            for attempt in range(3):
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Resetting to Home for Settings Navigation ({attempt+1}/3)...")
                
                if self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🖱️ Clicking Menu Tab...")
                    bot.safe_click_tab(dynamic_tabs["menu"]["xpath"], target_tab_index=dynamic_tabs["menu"]["index"])
                    bot.wait(1.5)
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Failed to reach Home. Retrying...")
                    continue 

                if bot.exists_xpath(settings_gear, timeout=15):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🖱️ Clicking Settings Gear...")
                    bot.click_xpath(settings_gear)
                    bot.wait(2)
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Could not find Settings Gear.")
                    continue 

                if bot.exists_xpath(self.accounts_center, timeout=15):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] 🖱️ Opening Accounts Center...")
                    bot.click_xpath(self.accounts_center)
                    bot.wait(3)
                    nav_success = True
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Reached Accounts Center.")
                    break 
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Could not find Accounts Center button.")
            if not nav_success:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to open Accounts Center.")
                update_acc_signal.emit(acc_id, False, {"status": "❌ Failed to open Accounts Center"})
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return False, "Failed to open Account Center"


            if self.actives_settings.get("get_account_info"):   

                # Step 1: Personal Details
                if bot.exists_xpath(self.personal_details, timeout=4):
                    bot.click_xpath(self.personal_details)
                    bot.wait(2)
                    
                data_elements_xpath = (
                    '//android.widget.Button[contains(@content-desc, "Contact info") '
                    'or contains(@content-desc, "Birthday") '
                    'or contains(@content-desc, "Facebook")]'
                )
                
                extraction_success = False
                MAX_SCROLLS = 3
                
                for scroll_attempt in range(MAX_SCROLLS):
                    if stop_event.is_set(): return False, "Stopped by user"
                    
                    elements = bot.find_elements(data_elements_xpath, timeout=2)
                    
                    # --- INNER LOOP: Check all visible elements first ---
                    for el in elements:
                        try:
                            desc = el.get_attribute("content-desc")
                            if not desc: continue
                            
                            if desc.startswith("Contact info"):
                                emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', desc)
                                for email in emails:
                                    if email not in extracted_data["emails"]:
                                        clean_email = email.rstrip('.')
                                        extracted_data["emails"].append(clean_email)
                                
                                phones = re.findall(r'\+?\d{8,15}', desc)
                                for phone in phones:
                                    if phone not in extracted_data["phones"]:
                                        extracted_data["phones"].append(phone)
                                        
                            elif desc.startswith("Birthday"):
                                clean_bday = desc.split("Birthday,")[-1].strip()
                                extracted_data["birthday"] = clean_bday
                                
                            elif desc.endswith(", Facebook"):
                                if not extracted_data.get("name"): 
                                    clean_name = desc.split(", Facebook")[0].strip()
                                    extracted_data["name"] = clean_name

                        except Exception:
                            continue
                    # --- END OF INNER LOOP ---

                    # Check what we found so far
                    has_contact = len(extracted_data["emails"]) > 0 or len(extracted_data["phones"]) > 0
                    has_bday = bool(extracted_data.get("birthday"))
                    has_name = bool(extracted_data.get("name"))
                    
                    # 🟢 FIX: If we found at least the name, consider it a partial success so the script doesn't crash
                    if has_name:
                        extraction_success = True
                    
                    # If we found absolutely everything, exit the scroll loop early!
                    if has_name and has_contact and has_bday:
                        print(f"[{acc_id}] ✅ Found all personal details!")
                        break 
                        
                    # If we are still missing data, scroll down!
                    if scroll_attempt < MAX_SCROLLS - 1:
                        print(f"[{acc_id}] 👇 Scrolling down to find missing info (Attempt {scroll_attempt + 1}/{MAX_SCROLLS})")
                        bot.scroll_down() 
                        bot.wait(2) 

                # ---------------------------------------------------------
                # FAILED EXTRACTION CHECK
                # ---------------------------------------------------------
                # If it scrolled 3 times and couldn't even find the account Name
                if not extraction_success:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to read Personal Details.")
                    update_acc_signal.emit(acc_id, True, {"status": "❌ Could not read Personal Details"})
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    return False, "Could not read Personal Details"

                # ---------------------------------------------------------
                # 6. ESCAPE AND SAVE
                # ---------------------------------------------------------
                update_ld_signal.emit(ld_name, f"[{acc_id}] 💾 Saving extracted data to database...")
                
                # 🟢 KEEP THIS: Emitting with True flag saves the actual DATA to the DB.
                update_acc_signal.emit(
                    acc_id, 
                    True, 
                    {
                        "name": extracted_data.get("name", ""),
                        "email": extracted_data.get("emails"),
                        "birthday": extracted_data.get("birthday", ""),
                        "phone_number": extracted_data.get("phones"), 
                    }
                )
                for _ in range(5):
                    pass_sec_check = '//android.view.View[@content-desc="Password and security"] | //android.widget.Button[@content-desc="Password and security"]'
                    if bot.exists_xpath(pass_sec_check, timeout=2):
                        break 
                    bot.press_back()
                    bot.wait(1.5)

            if add_email:
                update_acc_signal.emit(acc_id, False, {"status": "➡️ Starting Add Email"})
                success, reason = self.add_email(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, extracted_data, tab_bar_xpaths, stop_event)
                if not success:
                    for i in range(4):
                        if bot.exists_xpath(self.close_btn):
                            bot.click_xpath(self.close_btn)
                        else:
                            bot.tap_percentage(6, 0.8)
                        if bot.exists_xpath(dynamic_tabs["home"]["xpath"]):
                            break
                        time.sleep(1)
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    return False, reason

            if two_fa:
                update_acc_signal.emit(acc_id, False, {"status": "➡️ Starting 2FA Setup"})
                success, reason = self.setup_2fa(acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, data_acc, dynamic_tabs, tab_bar_xpaths, stop_event)
                if not success:
                    for i in range(4):
                        if bot.exists_xpath(self.close_btn):
                            bot.click_xpath(self.close_btn)
                        else:
                            bot.tap_percentage(6, 0.8)
                        if bot.exists_xpath(dynamic_tabs["home"]["xpath"]):
                            break
                        time.sleep(1)
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    return False, reason # Pass the exact reason up the chain
   

            for i in range(4):
                if bot.exists_xpath(self.close_btn):
                    bot.click_xpath(self.close_btn)
                else:
                    bot.tap_percentage(6, 0.8)
                if bot.exists_xpath(dynamic_tabs["home"]["xpath"]):
                    break
                time.sleep(1)
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, "Successfully updated Settings"

        except Exception as e:
            error_msg = f"Script Exception: {str(e)[:30]}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Setting Crash: {error_msg}")
            update_acc_signal.emit(acc_id, False, {"status": f"❌ Setting Crash: {error_msg}"})
            print(f"❌Setup Failed: {e}")
            for i in range(6):
                if bot.exists_xpath(self.close_btn):
                    bot.click_xpath(self.close_btn)
                if bot.exists_xpath(dynamic_tabs["home"]["xpath"]):
                    break
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg

    def add_email(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, extracted_data, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Starting Add Email Process...")
        
        # 1. NAVIGATION
        if not self._nav_to_add_email(acc_id, ld_name, bot, update_ld_signal, stop_event):
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to reach Add Email screen.")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, "Could not reach Add Email screen"

        # 2. CREDENTIAL CHECK
        email_address = self.actives_settings.get("yandex_mail")
        app_password = self.actives_settings.get("app_password_yandex")
        if not email_address or not app_password:
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, "Missing Yandex credentials!"

        # 3. FIND AVAILABLE EMAIL
        success, new_email_or_msg = self._find_available_email(acc_id, ld_name, bot, update_acc_signal, stop_event)
        if not success:
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, new_email_or_msg

        extracted_data["emails"].append(new_email_or_msg)

        # 4. FETCH AND ENTER YANDEX CODE
        code_accepted = False
        next_btn = '//android.view.View[@content-desc="Next"] | //android.widget.Button[@content-desc="Next"]'
        
        for attempt in range(3):
            if stop_event.is_set(): return False, "Stopped by user"
            update_acc_signal.emit(acc_id, False, {"status": f"⏳ Waiting code 10s ({attempt+1}/3)"})
            bot.wait(10) 
            
            yandex_code = self.general_function.get_yandex_code(email_address, app_password)
            if yandex_code:
                update_acc_signal.emit(acc_id, False, {"status": f"⌨️ Submitting Code: {yandex_code}"})
                code_xpath = '//android.widget.EditText[contains(@content-desc, "Code")]'
                bot.click_xpath(code_xpath)
                bot.type_xpath(code_xpath, yandex_code)
                bot.click_xpath(next_btn)
                bot.wait(5)
                
                if bot.exists_xpath(code_xpath, timeout=2):
                    if bot.exists_xpath(self.close_btn, timeout=3): # Ensure self.close_btn is defined
                        bot.click_xpath(self.close_btn)
                        code_accepted = True
                        break
                    bot.wait(5)
                else:
                    code_accepted = True
                    break

        if not code_accepted:
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, "Verify email code not accepted!"

        # 5. VERIFY SUCCESS & SAVE
        success_msg_xpath = '//android.view.View[contains(@content-desc, "You’ve added your email")] | //android.view.View[contains(@content-desc, "only be visible to you")] | //android.view.ViewGroup[contains(@content-desc, "Facebook")]'
        
        if bot.exists_xpath(success_msg_xpath, timeout=5) or bot.exists_xpath(self.close_btn, timeout=3):
            update_acc_signal.emit(acc_id, True, {"email": extracted_data.get("emails"), "status": "✅ Email added to DB"})
            if bot.exists_xpath(self.close_btn, timeout=3):
                bot.click_xpath(self.close_btn)
                bot.wait(2)
                
            bot.press_back() # Back out of menu safely
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, "Successfully added Email"
            
        return False, "Added email, but got stuck returning to Accounts Center"

    def setup_2fa(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, data_acc, dynamic_tabs, tab_bar_xpaths, stop_event):
        import pyotp
        import re
        
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Starting 2FA Setup")
        already_on_xpath = '//android.view.View[contains(@content-desc, "Two-factor authentication is on")] | //android.view.View[contains(@content-desc, "We\'ll now ask for a login code")] | //android.view.View[contains(@content-desc, "from your authentication app")]'

        # 1. NAVIGATION
        if not self._nav_to_2fa_setup(acc_id, ld_name, bot, update_ld_signal, data_acc):
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, "Could not reach Setup 2FA menu"
            
        # 2. CHECK IF ALREADY ACTIVE
        if bot.exists_xpath(already_on_xpath, timeout=3):
            update_acc_signal.emit(acc_id, True, {"status": "✅ 2FA Already Active"})
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, "2FA Already Active"

        # 3. HANDLE BARRIERS (Password, Email Verification, etc)
        status, msg = self._handle_2fa_barriers(acc_id, ld_name, bot, update_acc_signal, update_ld_signal, data_acc)
        if status == "FAILED":
            for _ in range(5): bot.press_back()
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, msg
            
        if bot.exists_xpath(already_on_xpath, timeout=3):
            update_acc_signal.emit(acc_id, True, {"status": "✅ 2FA Already Active"})
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, "2FA Already Active"

        # 4. SELECT AUTHENTICATOR APP
        auth_app_btn = '//android.widget.Button[contains(@content-desc, "Authentication app")] | //android.view.View[contains(@content-desc, "Authentication app")]'
        if bot.exists_xpath(auth_app_btn, timeout=4):
            bot.click_xpath(auth_app_btn)
            bot.click_xpath('//android.widget.Button[@content-desc="Next"]')
            bot.wait(3)

        if bot.exists_xpath('//android.view.ViewGroup[contains(@content-desc, "My Authenticator app")]', timeout=2):
            update_acc_signal.emit(acc_id, True, {"status": "✅ 2FA Already Active"})
            for _ in range(4): bot.press_back()
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, "2FA Already Active"

        # 5. EXTRACT SECRET KEY
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🕵️‍♂️ Scanning screen for 2FA Secret Key...")
        secret_key = None
        all_elements = bot.find_elements('//android.view.View | //android.widget.TextView', timeout=5)
        
        for el in all_elements:
            try:
                content = ((el.get_attribute("content-desc") or "") + " " + (el.get_attribute("text") or "")).upper()
                match = re.search(r'(?:[A-Z2-7]{4}\s+){7}[A-Z2-7]{4}', content)
                if match:
                    secret_key = match.group(0).replace(" ", "").strip()
                    break
            except Exception: continue
        
        if not secret_key or len(secret_key) != 32:
            update_acc_signal.emit(acc_id, True, {"status": "❌ Could not find valid 2FA Secret Key"})
            for _ in range(5): bot.press_back()
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, "Could not find valid 2FA Secret Key on screen"
            
        update_acc_signal.emit(acc_id, False, {"two_fa": secret_key}) # Save to DB

        bot.click_xpath('//android.widget.Button[@content-desc="Enter code"]')
        bot.wait(2)

        # 6. GENERATE & INPUT TOTP
        code_input_xpath = '//android.widget.EditText[contains(@content-desc, "Enter code") or contains(@text, "Code")]'
        setup_success = False
        
        for attempt in range(3):
            live_code = pyotp.TOTP(secret_key).now()
            if bot.exists_xpath(code_input_xpath, timeout=2):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⌨️ Entering TOTP: {live_code}")
                bot.click_xpath(code_input_xpath) 
                bot.type_xpath(code_input_xpath, live_code)
                bot.click_xpath('//android.widget.Button[@content-desc="Next"]')
                bot.wait(3)
                
                if bot.exists_xpath('//android.view.View[contains(@content-desc, "isn\'t right") or contains(@content-desc, "invalid")]', timeout=2):
                    bot.wait(10) 
                    continue
                else:
                    setup_success = True
                    break 
                    
        if not setup_success:
            update_acc_signal.emit(acc_id, True, {"status": "❌ Live TOTP Code rejected 3 times"})
            for _ in range(4): bot.press_back()
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, "Live TOTP Code rejected 3 times"
            
        bot.wait(2)
        done_btn = '//android.widget.Button[@content-desc="Done" or @text="Done" or @content-desc="OK" or @text="OK" or contains(@content-desc, "Continue")] | //android.view.View[@content-desc="Done" or @text="Done" or @content-desc="OK" or @text="OK"]'
        if bot.exists_xpath(done_btn, timeout=5):
            bot.click_xpath(done_btn)
            bot.wait(2)
            
        update_acc_signal.emit(acc_id, True, {"status": "✅ Successfully Setup 2FA"})
        self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
        return True, "Successfully Setup 2FA"

    # =====================================================================
    # Videos MODULE HELPERS
    # =====================================================================
    def is_group_screen(self, bot):
        your_groups_btn = '//android.view.ViewGroup[@content-desc="Your groups"] | //*[@text="Your groups"]'
        if bot.exists_xpath(your_groups_btn, timeout=6):
            bot.click_xpath(your_groups_btn)
            bot.wait(3)
            return True
        else:
            error_msg = "Could not find 'Your groups' button"
            return False, error_msg

    def extract_and_save_groups(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        try:
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            success = self.goto_tab_with_search(
                acc_id, ld_name, bot, update_ld_signal, dynamic_tabs, 
                tab_key="group", 
                search_fallback_text="Groups ", 
                verification_func=self.is_group_screen
            )
            
            if not success:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Fatal: Could not load Group tab.")
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                return False, "Could not load or verify the Group tab"



            # =========================================================
            # 3. UNLIMITED EXTRACTION LOOP
            # =========================================================
            update_acc_signal.emit(acc_id, False, {"status": "🔍 Extracting ALL groups..."})
            extracted_groups = []
            
            ignore_list = [
                "Groups", "Your groups", "Create", "Discover", "Settings", 
                "Groups you manage", "Others", "Pinned", "Joined", "See all", 
                "Search", "Sort", "Menu", "Back", "Recent activity", 
                "null", "For you", "Posts", "Currently previewing", "Join", 
                "Delete", "See all invites", "Create group", 
                "Sort your other groups", "Search groups"
            ]
            
            # 🟢 NEW: Bottom detection variables
            no_new_items_streak = 0
            MAX_SAFE_SCROLLS = 20 # A massive safety limit just in case Facebook glitches
            
            for scroll_attempt in range(MAX_SAFE_SCROLLS):
                if stop_event.is_set(): return False, "Stopped by user"
                
                # Remember how many groups we had before looking at this screen
                groups_count_before = len(extracted_groups)
                
                elements = bot.find_elements('//*[@content-desc or @text]', timeout=2)
                
                for el in elements:
                    try:
                        desc = el.get_attribute("content-desc")
                        text = el.get_attribute("text")
                        raw_name = desc if desc else text
                        
                        if raw_name:
                            raw_str = str(raw_name).strip()
                            
                            if "invited you" in raw_str.lower():
                                continue
                                
                            clean_name = raw_str.split("Button")[0].strip()
                            clean_name = re.sub(r'(\d+\+ new posts|Updated.*)', '', clean_name, flags=re.IGNORECASE).strip()
                            
                            if clean_name and clean_name not in ignore_list and clean_name.lower() != "null":
                                if len(clean_name) > 3 and not clean_name.isdigit():
                                    if clean_name not in extracted_groups:
                                        extracted_groups.append(clean_name)
                                        # Show total count live!
                                        update_acc_signal.emit(acc_id, False, {"status": f"📝 Total: {len(extracted_groups)} | {clean_name[:20]}..."})
                    except Exception:
                        continue
                
                # 🟢 NEW: Bottom Detection Logic
                groups_count_after = len(extracted_groups)
                
                if groups_count_after == groups_count_before:
                    # We didn't find any new groups on this screen
                    no_new_items_streak += 1
                else:
                    # We found new groups! Reset the streak.
                    no_new_items_streak = 0
                    
                # If we scrolled 2 times in a row and found NOTHING new, we are at the bottom!
                if no_new_items_streak >= 2:
                    update_acc_signal.emit(acc_id, False, {"status": "✅ Reached the bottom of the list!"})
                    break # Break out of the loop and move to save!
                        
                # Scroll down to reveal more groups
                bot.scroll_down()
                bot.wait(2) # Give Facebook 2 seconds to load the next page of groups

            # 4. Save using your new DataManager helper
            if extracted_groups:
                self.data_manager.save_groups(acc_id, extracted_groups)
                update_acc_signal.emit(acc_id, True, {"status": f"✅ Saved {len(extracted_groups)} groups!"})
                return True, f"✅ Scraped Group Total: {groups_count_after}"
            else:
                return False, "No groups found"
                
        except Exception as e:
            return False, f"Error: {str(e)}"

    def process_videos(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Starting Standard Videos Module")
        update_acc_signal.emit(acc_id, False, {"status": "📺 Running Watch Videos..."})
        
        try:
            target_videos = random.randint(
                self.actives_settings.get("watch_videos_from", 0),
                self.actives_settings.get("watch_videos_to", 0)
            )
            if target_videos <= 0:
                return True, "No video targets configured"

            reaction_pool = self.build_reaction_pool("videos")
            videos_watched = 0
            reactions_done = 0

            # ---------------------------------------------------------
            # 1. INITIAL NAVIGATION (Using our new smart helper!)
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎬 Navigating to Videos Tab (Target: {target_videos})")

            self.goto_via_deeplink(appium_name, "watch")

            if not self.is_videos_tab(bot):
                self.goto_via_deeplink(appium_name, "home")
                success = self.goto_tab_with_search(
                    acc_id, ld_name, bot, update_ld_signal, dynamic_tabs, 
                    tab_key="video", 
                    search_fallback_text="Video ", 
                    verification_func=self.is_videos_tab
                )
                
                if not success:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Fatal: Could not load Videos tab.")
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    return False, "Could not load or verify the Videos tab"

            # ---------------------------------------------------------
            # 2. MAIN WATCH LOOP
            # ---------------------------------------------------------
            while videos_watched < target_videos:
                if stop_event.is_set(): return False

                like_btn = None
                empty_scrolls = 0
                
                # --- A. Hunt for Video ---
                while not like_btn and empty_scrolls < 5:
                    if stop_event.is_set(): return False
                    
                    elements = bot.find_elements(self.reaction_xpath, timeout=2)
                    if elements:
                        like_btn = elements[0] # We found the video's action bar!
                        break
                        
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ➡️ Scrolling Alittle bit")
                    bot.scroll_down(speed_ms=1000) 
                    bot.wait(2)
                    
                    # Basic Feed check
                    if not self.is_videos_tab(bot):
                        bot.press_back()
                        bot.wait(1)
                        if not self.is_videos_tab(bot):
                            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Lost video feed context.")
                            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                            return False, f"Lost feed after {videos_watched} videos"
                    empty_scrolls += 1

                if not like_btn:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ No playable videos found. Exiting early.")
                    break

                # --- B. Smart Positioning (Using new helper) ---
                bot.nudge_element_into_view(like_btn)

                # --- C. Watch Video ---
                watch_delay = random.randint(
                    self.actives_settings.get("delay_watch_video_from", 5),
                    self.actives_settings.get("delay_watch_video_to", 15)
                )
                
                if videos_watched % 3 == 0 or videos_watched == target_videos - 1:
                    update_acc_signal.emit(acc_id, False, {"status": f"📺 Watching Video {videos_watched + 1}/{target_videos}..."})
                
                update_ld_signal.emit(ld_name, f"[{acc_id}] 👀 Watching video {videos_watched + 1}/{target_videos} for {watch_delay}s...")
                bot.wait(watch_delay)

                # --- D. Reaction Logic ---
                do_react = False
                if self.actives_settings.get("videos_alway_emoji"): do_react = True
                elif self.actives_settings.get("videos_random_emoji"): do_react = random.choice([True, False])

                if do_react and len(reaction_pool) > 0:
                    next_reaction = reaction_pool.pop(0) 
                    if bot.react_to_post(reaction_type=next_reaction):
                        reactions_done += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] 👍 Sent '{next_reaction}' ({reactions_done} total)...")
                        bot.wait(random.uniform(1.5, 3.5))

                # --- E. Swipe Next ---
                videos_watched += 1
                if videos_watched >= target_videos:
                    break
                    
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Swiping to next video...")
                bot.scroll_down(speed_ms=300) 
                bot.wait(3.0) 

            # ---------------------------------------------------------
            # 3. FINAL CLEANUP & RETURN
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎉 Videos completed! (Watched: {videos_watched} | Reactions: {reactions_done})")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return True, f"Watched {videos_watched} videos, {reactions_done} reactions"

        except Exception as e:
            error_msg = f"Video Crash: {str(e).split(chr(10))[0][:40]}"
            print(f"Video Crash: {str(e)}")
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg

    def process_videos_reels(self, acc_id, ld_name, appium_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Starting Full-Screen Reels Module")
        update_acc_signal.emit(acc_id, False, {"status": "🎬 Running Watch Videos Reels"})
        
        try:
            # ---------------------------------------------------------
            # 1. SETUP TARGETS
            # ---------------------------------------------------------
            feed_from = int(self.actives_settings.get("watch_feeds_from", 0))
            feed_to = int(self.actives_settings.get("watch_feeds_to", 0))
            target_videos = random.randint(min(feed_from, feed_to), max(feed_from, feed_to))
            
            if target_videos <= 0:
                update_acc_signal.emit(acc_id, True, {"status": "⚠️ No reels targets configured"})
                return True, "No reels targets configured"

            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎬 Reels (Target: {target_videos})")
            update_acc_signal.emit(acc_id, False, {"status": f"🎬 Target: {target_videos} Reels"})

            videos_watched = 0
            reactions_done = 0
            reaction_pool = self.build_reaction_pool("feeds")

            # ---------------------------------------------------------
            # 2. INITIAL NAVIGATION (Using smart helper)
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎬 Navigating to Videos Tab...")
            
            success = self.goto_tab_with_search(
                acc_id, ld_name, bot, update_ld_signal, dynamic_tabs, 
                tab_key="video", 
                search_fallback_text="Reels ", 
                verification_func=self.is_fullscreen_video
            )
            if not success:
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                update_acc_signal.emit(acc_id, True, {"status": "❌ Failed to load Video tab"})
                return False, "Failed to navigate to Videos Tab or recover Home Feed"

            # ---------------------------------------------------------
            # 3. ENTER FIRST FULL-SCREEN REEL (Using new hunt helper)
            # ---------------------------------------------------------
            update_acc_signal.emit(acc_id, False, {"status": "🔎 Hunting for a playable Reel..."})
            if not self._hunt_and_enter_reel(acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Fatal: Could not find any playable reels after 12 scrolls.")
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                update_acc_signal.emit(acc_id, True, {"status": "❌ No playable Reels found"})
                return False, "Exhausted scrolls; could not find a playable Reel"

            # ---------------------------------------------------------
            # 4. MAIN WATCHING & SWIPING LOOP (TikTok Style)
            # ---------------------------------------------------------
            while videos_watched < target_videos:
                if stop_event.is_set(): return False
                
                # --- A. WATCH THE REEL ---
                delay_from = int(self.actives_settings.get("delay_watch_feeds_from", 5))
                delay_to = int(self.actives_settings.get("delay_watch_feeds_to", 15))
                watch_delay = random.randint(min(delay_from, delay_to), max(delay_from, delay_to))

                update_ld_signal.emit(ld_name, f"[{acc_id}] 👀 Watching Reel {videos_watched + 1}/{target_videos} for {watch_delay} seconds...")
                update_acc_signal.emit(acc_id, False, {"status": f"👀 Watching Reel {videos_watched + 1}/{target_videos}"})
                bot.wait(watch_delay)

                # --- B. REACT LOGIC ---
                do_react = False
                if self.actives_settings.get("feeds_alway_emoji"): do_react = True
                elif self.actives_settings.get("feeds_random_emoji"): do_react = random.choice([True, False])

                if do_react and len(reaction_pool) > 0:
                    next_reaction = reaction_pool.pop(0) 
                    if bot.react_to_reel(reaction_type=next_reaction):
                        reactions_done += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] 👍 Sent '{next_reaction}' ({reactions_done} total)...")
                        bot.wait(random.uniform(1.5, 3.5))

                # --- C. MOVE TO NEXT REEL & VERIFY ---
                videos_watched += 1
                if videos_watched >= target_videos:
                    update_acc_signal.emit(acc_id, False, {"status": f"🎯 Target reached ({target_videos}/{target_videos})"})
                    break
                    
                update_ld_signal.emit(ld_name, f"[{acc_id}] ➡️ Swiping up to next Reel")
                bot.scroll_down(speed_ms=300) 
                bot.wait(3.0) 
                
                # --- D. STRICT POST-SWIPE VERIFICATION & RECOVERY ---
                if not self.is_fullscreen_video(bot):
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Swipe invalid page. Recovering...")
                    bot.press_back()
                    bot.wait(2)
                    
                    if not self.is_fullscreen_video(bot):
                        update_ld_signal.emit(ld_name, f"[{acc_id}] 🔄 Fell out of viewer. Hunting for new Reel...")
                        
                        if self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event):
                            self.goto_tab_with_search(acc_id, ld_name, bot, update_ld_signal, dynamic_tabs, "video", "Reels ", self.is_fullscreen_video)
                        
                        if not self._hunt_and_enter_reel(acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
                            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                            return False, f"Lost Reel viewer context after watching {videos_watched} reels"

            # ---------------------------------------------------------
            # 5. FINAL CLEANUP & RETURN
            # ---------------------------------------------------------
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎉 Reels completed! (Watched: {videos_watched} | Reactions: {reactions_done})")
            update_acc_signal.emit(acc_id, True, {"status": f"🎉 Reels Complete ({videos_watched})"})
            
            bot.press_back()
            bot.wait(1.5)
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            
            return True, f"Watched {videos_watched} Reels, {reactions_done} reactions"

        except Exception as e:
            error_msg = f"Reels Crash: {str(e).split(chr(10))[0][:40]}"
            print(f"Reels Crash: {str(e)}")
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            update_acc_signal.emit(acc_id, True, {"status": f"❌ {error_msg}"})
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg

    # =====================================================================
    # REELS MODULE HELPERS
    # =====================================================================
    def _inject_video_via_adb(self, acc_id, ld_name, appium_name, selected_media, update_acc_signal, update_ld_signal, post_index, total_posts):
        """Clears old media, pushes new media with a unique name, and triggers media scan. Safe for Reels, Videos, and Stories!"""
        import time # Ensure this is imported at the top of your file
        
        filename = os.path.basename(selected_media)
        _, ext = os.path.splitext(filename) # 🟢 FIX 1: Gets the real extension (.jpg, .mp4, etc.)
        
        update_acc_signal.emit(acc_id, False, {"status": f"📥 Pushing Media ({post_index+1}/{total_posts})"})
        
        # 🟢 FIX 2: Delete everything in the emulator's Camera folder first
        self.ld_manager.run_adb('shell rm -f /sdcard/DCIM/Camera/*', device=appium_name)
        
        # 🟢 FIX 3: Give the file a unique timestamp name so Android never caches it
        unique_name = f"media_{int(time.time())}{ext}"
        remote_path = f"/sdcard/DCIM/Camera/{unique_name}"
        
        push_result = self.ld_manager.run_adb(f'push "{selected_media}" {remote_path}', device=appium_name)
        
        if push_result is None:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ ADB push failed for {filename}")
            return False, f"ADB push failed for {filename}"
            
        # Broadcast the new file to the gallery
        self.ld_manager.run_adb(
            f'shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{remote_path}',
            device=appium_name
        )
        return True, "Success"

    def _nav_to_reels_creator(self, acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        """Navigates to the Reels creation screen using smart fallbacks."""
        if stop_event.is_set(): return False
        self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
        
        reels_ready = False
        
        # PATH A: Home Feed Create Button
        create_btn = '//android.widget.Button[@content-desc="Create, Double tap to create a new post, story, or reel"]'
        if bot.exists_xpath(create_btn, timeout=5):
            bot.click_xpath(create_btn)
            bot.wait(0.5)
            reel_btn = '//android.widget.Button[@content-desc="Reel"]'
            if bot.exists_xpath(reel_btn, timeout=3):
                bot.click_xpath(reel_btn)
                bot.wait(1)
                reels_ready = True

        # PATH B: Fallback to Profile Navigation
        if not reels_ready:
            if self.goto_via_deeplink(appium_name, "fb://profile"):
                update_ld_signal.emit(ld_name, f"[{acc_id}] 📜 Scrolling to find Reels in Profile...")
                reel_xpath = '//android.view.ViewGroup[@content-desc="Reels"] | //android.view.ViewGroup[@content-desc="Reel"]'
                for _ in range(6): 
                    if bot.exists_xpath(reel_xpath, timeout=2):
                        bot.click_xpath(reel_xpath)
                        bot.wait(2)
                        reels_ready = True
                        break
                    else:
                        bot.scroll_down(speed_ms=1200)
                        bot.wait(1.5)

        if not reels_ready: return False

        # Clear Discard Prompts
        discard_btn = '//*[@resource-id="android:id/button3"] | //*[contains(@text, "DISCARD") or contains(@text, "Discard")]'
        if bot.exists_xpath(discard_btn, timeout=2):
            bot.click_xpath(discard_btn)
            bot.wait(1)

        # Smart Coordinate Camera Tap
        camera_reel = '//android.view.ViewGroup[@content-desc="Start a Camera reel"] | //android.view.ViewGroup[@content-desc="Start a Music reel"] | //android.view.ViewGroup[@content-desc="Start a Templates reel"]'
        for attempt in range(3):
            if bot.exists_xpath(camera_reel, timeout=5): return True
            
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Reels Camera not ready (Attempt {attempt+1}/3). Tapping screen...")
            target_x = int(bot.size['width'] * 0.79)
            target_y = int(bot.size['height'] * 0.68)
            
            if attempt == 1: target_y -= int(bot.size['height'] * 0.05)
            elif attempt == 2: target_y += int(bot.size['height'] * 0.05)
            
            bot.tap(target_x, target_y)
            bot.wait(3) 

        return False

    def _select_injected_video(self, acc_id, ld_name, bot, update_ld_signal):
        """Robustly selects the latest video/photo by finding its unique UI coordinate."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🛡️ Checking Camera/Storage permissions")
        all_dismiss_buttons = f"{self.allow_btn} | {self.continue_btn}"
        for _ in range(3):
            if bot.exists_xpath(all_dismiss_buttons, timeout=0.5):
                bot.click_xpath(all_dismiss_buttons)
                bot.wait(0.5)
            else:
                break

        update_ld_signal.emit(ld_name, f"[{acc_id}] 🎥 Finding and selecting media...")
        bot.wait(3) # Give gallery time to render the injected file

        # 🟢 DYNAMIC FINDER: Looks for the first Video or Photo element
        media_xpath = '//android.view.ViewGroup[contains(@content-desc, "Video") or contains(@content-desc, "Photo")]'
        media_elements = bot.find_elements(media_xpath, timeout=8)
        
        found_center = None
        if media_elements:
            # Get the first unique coordinate to avoid the 'double element' nested-viewgroup bug
            bounds = media_elements[0].get_attribute("bounds")
            if bounds:
                coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                if len(coords) == 4:
                    cx = (coords[0] + coords[2]) // 2
                    cy = (coords[1] + coords[3]) // 2
                    found_center = (cx, cy)
        
        if found_center:
            bot.tap(found_center[0], found_center[1])
            bot.wait(3)
        else:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Could not find media in gallery!")
            return False

        # 🟢 PROCEED TO COMPOSER
        next_btn = '//android.view.ViewGroup[@content-desc="Next"] | //android.widget.Button[@content-desc="Next"]'
        if bot.exists_xpath(next_btn, timeout=10):
            bot.click_xpath(next_btn)
            bot.wait(3)
        else:
            return False

        # 🟢 CONFIRMATION (If prompted)
        if bot.exists_xpath(self.ok_btn, timeout=5):
            bot.click_xpath(self.ok_btn)
            
        return True

    def _add_reels_title_and_hashtags(self, acc_id, ld_name, bot, update_ld_signal, reels_data, video_filename):
        """Generates and types the title and hashtags."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 📝 Writing Title & Hashtags...")
        title_input = '//android.widget.AutoCompleteTextView[contains(@text, "Describe your reel")] | //android.widget.EditText[@text="Describe your reel. You can also add hashtags here…"] | //*[contains(@text, "Describe your reel")]'
        
        final_text = ""
        if reels_data.get("use_tittle_from_videos"):
            final_text += video_filename.replace('.mp4', '') + " "
        elif reels_data.get("use_fixed_tittle"):
            final_text += reels_data.get("tittle_text", "") + " "
            
        if reels_data.get("hastag"):
            hashtag_pool = reels_data.get("post_reels_hastag", "")
            if reels_data.get("use_fixed_hastag"):
                clean_fixed_tags = " ".join([f"#{tag.strip()}" if not tag.strip().startswith("#") else tag.strip() for tag in hashtag_pool.split(",") if tag.strip()])
                final_text += clean_fixed_tags + " "
            elif reels_data.get("use_random_hastag"):
                final_text += self.general_function.get_random_items_from_string(hashtag_pool, min_items=1, max_items=4, prefix="#", separator=" ")

        clean_final_text = final_text.strip()
        if bot.exists_xpath(title_input, timeout=3):
            bot.type_xpath(title_input, clean_final_text)
            bot.wait(1.5)
            bot.press_back() 
            
        return clean_final_text

    def _tag_people_in_reels(self, acc_id, ld_name, bot, update_ld_signal, target_tags):
        """Scrolls and systematically checks boxes to tag friends."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 👥 Tagging {target_tags} friends")
        tag_btn = '//android.view.ViewGroup[@content-desc="Tag people"]'
        
        if bot.exists_xpath(tag_btn, timeout=2):
            bot.click_xpath(tag_btn)
            bot.wait(3)
            
            tags_done = 0
            checkbox_xpath = '//android.widget.CheckBox'
            
            for _ in range(5):
                initial_boxes = bot.find_elements(checkbox_xpath, timeout=2)
                visible_count = len(initial_boxes)
                
                for i in range(visible_count):
                    if tags_done >= target_tags: break
                        
                    try:
                        fresh_boxes = bot.find_elements(checkbox_xpath, timeout=1)
                        if i < len(fresh_boxes):
                            cb = fresh_boxes[i]
                            if cb.get_attribute("checked") == "false":
                                cb.click()
                                tags_done += 1
                                bot.wait(1.5) 
                    except Exception: pass
                        
                if tags_done >= target_tags: break
                bot.scroll_down(speed_ms=1900)
                bot.wait(2)

            # 🟢 FIXED XPATH: Only selects "Tag [number] people", excludes "Tag people"
            confirm_tag_btn = '//android.view.ViewGroup[starts-with(@content-desc, "Tag ") and contains(@content-desc, "people") and not(normalize-space(@content-desc)="Tag people")]'
            
            if bot.exists_xpath(confirm_tag_btn, timeout=3):
                bot.click_xpath(confirm_tag_btn)
            else:
                bot.click_bottom_center()
            bot.wait(2)

    def _add_location_to_reels(self, acc_id, ld_name, bot, update_ld_signal, check_in_word):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 📍 Adding location: {check_in_word}")
        loc_btn = '//android.view.ViewGroup[@content-desc="Add location"] | //android.view.ViewGroup[@content-desc="Location"]'
        if bot.exists_xpath(loc_btn, timeout=2):
            bot.click_xpath(loc_btn)
            print("clcik location")
            bot.wait(2)
            
            turn_on = '//android.view.ViewGroup[@content-desc="Turn on"]'
            for _ in range(4):
                if bot.exists_xpath(self.allow_btn, timeout=1):
                    bot.click_xpath(self.allow_btn)
                    bot.wait(1)
                if bot.exists_xpath(turn_on, timeout=1):
                    bot.click_xpath(turn_on)
                    bot.wait(1)

            search_input = '//android.widget.EditText[@text="Search" or contains(@text, "Search")]'
            if bot.exists_xpath(search_input, timeout=3):
                bot.click_xpath(search_input)
                bot.type_xpath(search_input, check_in_word)
                bot.press_backspace(1)
                bot.wait(4)

                result_xpath = f'//android.view.ViewGroup[contains(@content-desc, "More actions, {check_in_word[:5]}")]'
                result_element = bot.find_elements(result_xpath, timeout=5)
                
                if result_element:
                    bounds = result_element[0].get_attribute("bounds")
                    if bounds:
                        coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                        if len(coords) == 4:
                            center_x = ((coords[0] + coords[2]) // 2) - 120
                            center_y = (coords[1] + coords[3]) // 2
                            bot.tap(center_x, center_y)
                            bot.wait(2)
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Location result not found. Skipping...")
                    bot.tap_percentage(50, 60)

    def _wait_for_post_to_publish(self, acc_id, ld_name, appium_name, bot, update_ld_signal, posted_title, stop_event, max_wait_minutes=3):
        """Refreshes the profile and waits until the new post appears by checking the title."""
        clean_title = posted_title.replace('"', '').replace("'", "").strip()[:15]
        
        if not clean_title:
            # Fallback if no title was provided
            update_ld_signal.emit(ld_name, f"[{acc_id}] 📜 No title provided, skipping processing wait...")
            self.goto_via_deeplink(appium_name, "fb://profile")
            bot.wait(3)
            bot.scroll_down(speed_ms=1900)
            return True

        update_ld_signal.emit(ld_name, f"[{acc_id}] ⏳ Waiting for Facebook to process the Reel...")
        
        # Calculate how many times to check (every 15 seconds)
        max_attempts = (max_wait_minutes * 60) // 15 
        title_xpath = f'//*[contains(@text, "{clean_title}")]'
        
        for attempt in range(max_attempts):
            if stop_event.is_set(): return False
            
            # 1. Teleport to Profile (This safely forces the app back to the top of the feed)
            self.goto_via_deeplink(appium_name, "fb://profile")
            bot.wait(0.5)
            
            # 2. Pull to Refresh
            bot.pull_to_refresh()
            
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🔍 Checking for post: '{clean_title}...' (Attempt {attempt+1}/{max_attempts})")
            
            # 3. Scroll down slightly to check the top few posts
            title_found = False
            for _ in range(4): 
                if stop_event.is_set(): return False
                if bot.exists_xpath(title_xpath, timeout=1.5):
                    title_found = True
                    break
                bot.scroll_down(speed_ms=1300)
                bot.wait(0.5)
                
            if title_found:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Post successfully published and verified!")
                return True
                
            # 4. If not found, wait 15 seconds before refreshing again
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🕒 Post still processing. Waiting 15 seconds...")
            bot.wait(15)
            
        update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Timeout: Post did not appear after {max_wait_minutes} minutes.")
        return False

    def _comment_on_own_post(self, acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, comment_text, posted_title, stop_event):
        update_ld_signal.emit(ld_name, f"[{acc_id}] 👤 Preparing to comment on new Reel...")
        
        # 🟢 1. Wait for the post to actually appear!
        if not self._wait_for_post_to_publish(acc_id, ld_name, appium_name, bot, update_ld_signal, posted_title, stop_event):
            return False # Stop if it timed out and never appeared

        # 2. FIND THE COMMENT BUTTON 
        # (We are already looking at the post because the helper function scrolled to it!)
        found = False
        for _ in range(3): 
            if stop_event.is_set(): return False
            
            comment_btns = bot.find_elements(self.comment_btn_xpath, timeout=2)
            if comment_btns:
                found = True
                break
            bot.scroll_down(speed_ms=1100)
            bot.wait(0.5)
            
        if not found:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Could not find the Comment button on this post.")
            return False
            
        # 3. EXECUTE YOUR COMMENT LOGIC
        try:
            update_ld_signal.emit(ld_name, f"[{acc_id}] 💬 Opening comments...")
            comment_btns[0].click()
            bot.wait(2.5)
                    
            if bot.exists_xpath(self.comment_input_xpath, timeout=3):
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✍️ Typing comment: '{comment_text[:15]}...'")
                bot.type_xpath(self.comment_input_xpath, comment_text)
                
                send_btn_ui = 'new UiSelector().descriptionMatches("(?i)send")'
                if bot.exists_ui(send_btn_ui, timeout=2):
                    bot.click_ui(send_btn_ui)
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Comment sent successfully!")
                    bot.wait(2)
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Send button missing. Aborting comment.")
            else:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Comment box did not load. Aborting.")
                
        except Exception as e:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Comment failed: {str(e).split(chr(10))[0][:30]}")
            
        # 6. SAFE ESCAPE
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🔙 Exiting comment screen...")
        bot.press_back() 
        bot.wait(1)
        bot.press_back() 
        bot.wait(1)
        
        return True

    def _execute_group_share_post(self, bot, reels_data):
        """Helper to type the title and click POST inside the group share screen."""
        auto_complete = '//android.widget.AutoCompleteTextView'
        if bot.exists_xpath(auto_complete, timeout=4):
            if reels_data.get("share_to_group_tittle"):
                title_text = ""
                raw_title = reels_data.get("share_to_group_word", "")
                
                if reels_data.get("use_fixed_share_group_tittle"):
                    title_text = raw_title
                elif reels_data.get("use_random_share_group_tittle"):
                    pool = [t.strip() for t in raw_title.split(",") if t.strip()]
                    if pool: title_text = random.choice(pool)
                    
                if title_text:
                    bot.type_xpath(auto_complete, title_text)
                    bot.wait(1.5)
                    bot.press_back() # Hide keyboard
                    bot.wait(1)
                    
        # CLICK POST
        post_btn = '//android.view.ViewGroup[@content-desc="POST" or @content-desc="Post"] | //android.widget.Button[contains(@content-desc, "POST")]'
        if bot.exists_xpath(post_btn, timeout=3):
            bot.click_xpath(post_btn)
            bot.wait(2) # Wait for it to process and return to the list
            return True
            
        return False

    def _robust_clear_search_box(self, bot, ld_name, acc_id, update_ld_signal, active_search_xpath, group_name):
        """Attempts to clear the search box safely, taps the right edge if needed, and verifies success."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🧹 Clearing search box...")
        
        # 1. Try the "X" (Clear) button first
        clear_btn = '//android.widget.ImageView[@content-desc="Clear" or @content-desc="Clear text"] | //android.view.ViewGroup[@content-desc="Clear"]'
        if bot.exists_xpath(clear_btn, timeout=2):
            bot.click_xpath(clear_btn)
            bot.wait(1.5)
            
        # 2. Check if the text actually cleared
        search_elements = bot.find_elements(active_search_xpath, timeout=2)
        if not search_elements: 
            return True # Box is gone/hidden, that is fine
            
        current_text = search_elements[0].get_attribute("text")
        
        # If the text is empty or reset to "Search", we are good!
        if not current_text or current_text == "Search" or current_text == "Search groups":
            return True
            
        # 3. MANUAL FALLBACK: Tap the FAR RIGHT edge to place cursor at the end
        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Manual clear needed. Deleting text...")
        bounds = search_elements[0].get_attribute("bounds")
        if bounds:
            coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
            if len(coords) == 4:
                # coords[2] is the far right edge of the box. We tap 30 pixels left of the edge.
                right_x = coords[2] - 30
                center_y = (coords[1] + coords[3]) // 2
                
                bot.tap(right_x, center_y)
                
                # Delete the length of the word + 10 extra just to be completely safe
                bot.press_backspace(len(group_name) + 10)
                bot.wait(0.4)
                
        # 4. FINAL VERIFICATION: Did it actually clear?
        search_elements = bot.find_elements(active_search_xpath, timeout=2)
        if search_elements:
            final_text = search_elements[0].get_attribute("text")
            # If the group name is still stuck in the search box, trigger a failure
            if final_text and group_name in final_text:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Search box is stuck!")
                return False 
                
        return True

    def _share_reel_to_groups(self, acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, reels_data, posted_title, stop_event):
        """Shares the successfully published reel to Facebook groups."""
        share_btn_xpath = '//android.view.ViewGroup[contains(@content-desc, "Share") or contains(@content-desc, "share") or contains(@content-desc, "Send")]' 
        update_ld_signal.emit(ld_name, f"[{acc_id}] 👥 Starting Share Reel to Groups...")
        
        # =========================================================
        # 1. SMART NAVIGATION & TITLE VERIFICATION
        # =========================================================
        # If the share button isn't visible, we must wait for the post to publish!
        if not bot.exists_xpath(share_btn_xpath, timeout=2):
            if not self._wait_for_post_to_publish(acc_id, ld_name, appium_name, bot, update_ld_signal, posted_title, stop_event):
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🛑 Aborting share to groups because the post was not found.")
                return False

        # =========================================================
        # 2. FIND & CLICK SHARE BUTTON
        # =========================================================
        found = False
        for _ in range(4):
            if stop_event.is_set(): return False
            if bot.exists_xpath(share_btn_xpath, timeout=2):
                bot.click_xpath(share_btn_xpath)
                found = True
                break
            bot.scroll_down(speed_ms=1100)
            bot.wait(0.5)
            
        if not found:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Could not find Share button on the reel.")
            return False
        bot.wait(1.5)
        
        # 3. CLICK 'SHARE TO GROUP'
        share_to_group_btn = '//android.view.ViewGroup[contains(@content-desc, "Group") or contains(@content-desc, "group")] | //android.widget.TextView[contains(@text, "Group")]'
        if bot.exists_xpath(share_to_group_btn, timeout=3):
            bot.click_xpath(share_to_group_btn)
            bot.wait(3)
        else:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Share to Group button not found.")
            return False

        # =========================================================
        # 4. PREPARE MODES & COUNTS
        # =========================================================
        use_selected = reels_data.get("share_to_group_use_by_seleted", False)
        use_suggest = reels_data.get("share_to_group_use_by_suggest", False)
        
        if not use_selected and not use_suggest: return True
            
        s_from = int(reels_data.get("share_to_group_from", 1))
        s_to = int(reels_data.get("share_to_group_to", 1))
        target_count = random.randint(min(s_from, s_to), max(s_from, s_to))
        
        shares_done = 0
        search_input = '//android.widget.EditText[@text="Search" or contains(@text, "Search")]'
        
        # =======================================================
        # PATH A: SEARCH & SELECT (share_to_group_use_by_seleted)
        # =======================================================
        if use_selected:
            groups_list = reels_data.get("groups_to_post", [])
            target_count = min(target_count, len(groups_list))
            selected_groups = random.sample(groups_list, target_count)
            
            for group_name in selected_groups:
                if stop_event.is_set(): break
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🔍 Searching for group: {group_name}")
                
                if bot.exists_xpath(search_input, timeout=4):
                    bot.click_xpath(search_input)
                    bot.clear_xpath(search_input)
                    bot.type_xpath(search_input, group_name)
                    bot.wait(2.5)
                    
                    active_search_box = '//android.widget.EditText'
                    search_element = bot.find_elements(active_search_box, timeout=2)
                    
                    # 🟢 NEW: Tracker to ensure we actually clicked the group
                    clicked_group = False 
                    
                    if isinstance(search_element, list) and len(search_element) > 0:
                        bounds = search_element[0].get_attribute("bounds")
                        if bounds:
                            coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                            if len(coords) == 4:
                                center_x = (coords[0] + coords[2]) // 2
                                search_box_height = coords[3] - coords[1] 
                                tap_y = coords[3] + int(search_box_height * 0.5) 
                                
                                bot.tap(center_x, tap_y)
                                bot.wait(3)
                                clicked_group = True # 🟢 Mark as successfully clicked
                    
                    # 🟢 CHECK: Only post if we successfully clicked into the group!
                    if clicked_group and self._execute_group_share_post(bot, reels_data):
                        shares_done += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Shared to group ({shares_done}/{target_count})")
                        
                        if not self._robust_clear_search_box(bot, ld_name, acc_id, update_ld_signal, active_search_box, group_name):
                            update_ld_signal.emit(ld_name, f"[{acc_id}] 🛑 Aborting group sharing to prevent errors.")
                            break
                    else:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Failed to click or post to group: {group_name}")
                        bot.press_back() 
                        bot.wait(1.5)
                        
                        if not self._robust_clear_search_box(bot, ld_name, acc_id, update_ld_signal, active_search_box, group_name):
                            break
                            
        # =======================================================
        # PATH B: SUGGESTED LIST (share_to_group_use_by_suggest)
        # =======================================================
        elif use_suggest:
            for i in range(target_count):
                if stop_event.is_set(): break
                update_ld_signal.emit(ld_name, f"[{acc_id}] 💡 Sharing to suggested group ({shares_done+1}/{target_count})")
                
                search_element = bot.find_elements(search_input, timeout=4)
                if isinstance(search_element, list) and len(search_element) > 0: # 🟢 Protected against string crash
                    bounds = search_element[0].get_attribute("bounds")
                    if bounds:
                        coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                        if len(coords) == 4:
                            # 1. Tap exactly below the Search Box
                            center_x = (coords[0] + coords[2]) // 2
                            tap_y = coords[3] + int(bot.size['height'] * 0.12)
                            
                            bot.tap(center_x, tap_y)
                            bot.wait(3)
                            
                            # 2. Write Title & Post
                            if self._execute_group_share_post(bot, reels_data):
                                shares_done += 1
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Shared to group ({shares_done}/{target_count})")
                                
                                # 3. SCROLL DOWN 1 SLOT FOR THE NEXT ITERATION
                                swipe_start_y = tap_y + int(bot.size['height'] * 0.15)
                                bot.swipe(center_x, swipe_start_y, center_x, tap_y, speed_ms=1000)
                                bot.wait(2)
                            else:
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Failed to post to suggested group.")
                                bot.press_back()
                                bot.wait(1)
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Search bar missing, cannot anchor taps.")
                    break
        
        # =======================================================
        # 6. SAFELY EXIT
        # =======================================================
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🔙 Finished sharing to {shares_done} groups.")
        for _ in range(3): 
            bot.press_back()
            bot.wait(1)
            
        return True

    def process_posts_reels(self, acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, data_acc, appium_name, stop_event):
        # 1. RETRIEVE SETTINGS & VALIDATE
        data = self.data_manager.get_post_setting_by_id(acc_id)
        if not data: return True, "No Reel settings found"
            
        reels = data.get("post_reels", {})
        if not reels.get("post", False): return True, "Reel posting is disabled"

        total_posts = reels.get("total_posts", 1)
        videos_reel_path = reels.get("videos_reel_path", "")

        if not os.path.exists(videos_reel_path):
            update_acc_signal.emit(acc_id, True, {"status": f"❌ Videos folder path invalid"})
            return False, f"Videos folder path invalid"

        update_acc_signal.emit(acc_id, False, {"status": f"🎬 Starting Reel Posting ({total_posts} target)"})
        failed_comments = 0
        failed_shares = 0
        posts_count = 0
        
        # 2. MAIN LOOP
        try:
            for post_index in range(total_posts):
                if stop_event.is_set(): return False, "Stopped by user"
                
                # 🟢 REFRESH VIDEO LIST EVERY LOOP (Prevents selecting moved files)
                local_videos = glob.glob(os.path.join(videos_reel_path, "*.mp4"))
                if not local_videos:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ No more videos in folder. Stopping.")
                    break

                selected_video = random.choice(local_videos)
                video_filename = os.path.basename(selected_video)
                
                update_acc_signal.emit(acc_id, False, {"status": f"🔄 Reel Post ({post_index+1}/{total_posts})"})

                # A. INJECT VIDEO
                success, msg = self._inject_video_via_adb(acc_id, ld_name, appium_name, selected_video, update_acc_signal, update_ld_signal, post_index, total_posts)
                if not success: return False, msg
                bot.wait(2)
                
                # B. NAVIGATE & SELECT
                if not self._nav_to_reels_creator(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
                    return False, "Could not navigate to Reels creation screen"
                
                if not self._select_injected_video(acc_id, ld_name, bot, update_ld_signal):
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    continue

                # C. DETAILS
                posted_title = self._add_reels_title_and_hashtags(acc_id, ld_name, bot, update_ld_signal, reels, video_filename)
                
                
                if reels.get("tag"):
                    target_tags = random.randint(reels.get("tag_from", 1), reels.get("tag_to", 3))
                    self._tag_people_in_reels(acc_id, ld_name, bot, update_ld_signal, target_tags)

                if reels.get("check_in") and reels.get("check_in_word"):
                    self._add_location_to_reels(acc_id, ld_name, bot, update_ld_signal, reels.get("check_in_word"))

                if reels.get("ai_label_reels"):
                    update_acc_signal.emit(acc_id, False, {"status": "🤖 Checking AI Label..."})
                    toggle_btn = '//android.widget.Switch'
                    if bot.exists_xpath(toggle_btn, timeout=2):
                        switch_elements = bot.find_elements(toggle_btn, timeout=2)
                        if switch_elements and switch_elements[0].get_attribute("checked") == "false":
                            bot.click_xpath(toggle_btn)
                            update_acc_signal.emit(acc_id, False, {"status": "🤖 AI Label turned ON"})
                        else:
                            update_acc_signal.emit(acc_id, False, {"status": "🤖 AI Label already ON"})
                # D. UPLOAD
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Uploading...")
                share_btn = '//android.view.ViewGroup[@content-desc="Share now"] | //android.widget.Button[@content-desc="Share now"]'
                    
                if bot.exists_xpath(share_btn, timeout=3):
                    bot.click_xpath(share_btn) # Ensure you click it!
                    bot.wait(30) 
                    
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Reel {post_index+1} posted!")
                    posts_count += 1
                    
                    # 🟢 MOVE FILE AFTER SUCCESSFUL CLICK
                    try:
                        posted_folder = os.path.join(videos_reel_path, "posted")
                        if not os.path.exists(posted_folder): os.makedirs(posted_folder)
                        shutil.move(selected_video, os.path.join(posted_folder, video_filename))
                    except Exception as e:
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ File move failed: {e}")
                    
                    # =========================================================
                    # 🟢 F. AUTO-COMMENT (Independent)
                    # =========================================================
                    if reels.get("comments"): 
                        raw_comment = reels.get("comments_text", "")
                        final_comment = ""
                        if raw_comment.strip():
                            if reels.get("comments_use_random"):
                                comment_pool = [c.strip() for c in raw_comment.split(",") if c.strip()]
                                if comment_pool: final_comment = random.choice(comment_pool)
                            elif reels.get("comments_use_fixed"):
                                final_comment = raw_comment.strip()
                                
                            if final_comment:
                                if not self._comment_on_own_post(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, final_comment, posted_title, stop_event):
                                    failed_comments += 1
                    # =========================================================
                    # 🟢 G. SHARE TO GROUPS (Independent)
                    # =========================================================
                    if reels.get("share_to_group"):
                        if not self._share_reel_to_groups(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, reels, posted_title, stop_event):
                            failed_shares += 1
 
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ Failed to find Share Now button.")
                    update_acc_signal.emit(acc_id, False, {"status": f"❌ Reel {post_index+1}/{total_posts} share button not found"})
                    
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)

            final_msg = f"Successfully posted {posts_count} Reels"
            has_failures = (failed_comments > 0 or failed_shares > 0)
            if failed_comments > 0:
                final_msg += f" | ❌ {failed_comments} Comment Fails"
            if failed_shares > 0:
                final_msg += f" | ❌ {failed_shares} Share Fails"
            update_acc_signal.emit(acc_id, True, {"status": final_msg})
            return (not has_failures), final_msg

        except Exception as e:
            error_msg = f"Post Reels Crash: {str(e)}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            update_acc_signal.emit(acc_id, True, {"status": f"❌ {error_msg}"})
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg
        
    def goto_via_deeplink(self, appium_name, target_page):
        deeplinks = {
            "home": "fb://feed",
            "profile": "fb://profile",
            "groups": "fb://groups_feed", # or whichever one worked for your groups
            "marketplace": "fb://marketplace",
            "watch": "fb://watch",
            "notifications": "fb://notifications",
            "menu": "fb://menu",
            "videos": "fb://videos",
        }
        
        # 🟢 If the user passed a raw deep link (starts with fb:// or http), use it directly!
        if target_page.startswith("fb://") or target_page.startswith("http"):
            link = target_page
        else:
            # Otherwise, look up the short-name in the dictionary (default to feed if not found)
            link = deeplinks.get(target_page.lower(), "fb://feed")
        
        adb_command = f'shell am start -a android.intent.action.VIEW -d "{link}" com.facebook.katana'
        self.ld_manager.run_adb(adb_command, device=appium_name)
        
        return True

    # =====================================================================
    # LONG VIDEO MODULE HELPERS
    # =====================================================================
    def _universal_share_to_groups(self, acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, mapped_data, posted_title, stop_event):
        """Universal function to share ANY post (Reel, Video, Image) to groups using standardized mapped_data."""
        share_btn_xpath = '//android.view.ViewGroup[contains(@content-desc, "Share") or contains(@content-desc, "share") or contains(@content-desc, "Send")]' 
        update_ld_signal.emit(ld_name, f"[{acc_id}] 👥 Starting Share to Groups...")
        
        # =========================================================
        # 1. SMART NAVIGATION & TITLE VERIFICATION
        # =========================================================
        if not bot.exists_xpath(share_btn_xpath, timeout=2):
            if not self._wait_for_post_to_publish(acc_id, ld_name, appium_name, bot, update_ld_signal, posted_title, stop_event):
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🛑 Aborting share to groups because the post was not found.")
                return False

        # =========================================================
        # 2. FIND & CLICK SHARE BUTTON
        # =========================================================
        found = False
        for _ in range(4):
            if stop_event.is_set(): return False
            if bot.exists_xpath(share_btn_xpath, timeout=2):
                bot.click_xpath(share_btn_xpath)
                found = True
                break
            bot.scroll_down(speed_ms=1100)
            bot.wait(0.5)
            
        if not found:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Could not find Share button on the post.")
            return False
        bot.wait(1.5)
        
        # 3. CLICK 'SHARE TO GROUP'
        share_to_group_btn = '//android.view.ViewGroup[contains(@content-desc, "Group") or contains(@content-desc, "group")] | //android.widget.TextView[contains(@text, "Group")]'
        if bot.exists_xpath(share_to_group_btn, timeout=3):
            bot.click_xpath(share_to_group_btn)
            bot.wait(3)
        else:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Share to Group button not found.")
            return False

        # =========================================================
        # 4. PREPARE MODES & COUNTS (Reading from mapped_data!)
        # =========================================================
        use_selected = mapped_data.get("share_to_group_use_by_seleted", False)
        use_suggest = mapped_data.get("share_to_group_use_by_suggest", False)
        
        if not use_selected and not use_suggest: return True
            
        s_from = int(mapped_data.get("share_to_group_from", 1))
        s_to = int(mapped_data.get("share_to_group_to", 1))
        target_count = random.randint(min(s_from, s_to), max(s_from, s_to))
        
        shares_done = 0
        search_input = '//android.widget.EditText[@text="Search" or contains(@text, "Search")]'
        
        # =======================================================
        # PATH A: SEARCH & SELECT
        # =======================================================
        if use_selected:
            groups_list = mapped_data.get("groups_to_post", [])
            target_count = min(target_count, len(groups_list))
            selected_groups = random.sample(groups_list, target_count)
            
            for group_name in selected_groups:
                if stop_event.is_set(): break
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🔍 Searching for group: {group_name}")
                
                if bot.exists_xpath(search_input, timeout=4):
                    bot.click_xpath(search_input)
                    bot.clear_xpath(search_input)
                    bot.type_xpath(search_input, group_name)
                    bot.wait(2.5)
                    
                    active_search_box = '//android.widget.EditText'
                    search_element = bot.find_elements(active_search_box, timeout=2)
                    
                    if isinstance(search_element, list) and len(search_element) > 0: 
                        bounds = search_element[0].get_attribute("bounds")
                        if bounds:
                            coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                            if len(coords) == 4:
                                center_x = (coords[0] + coords[2]) // 2
                                search_box_height = coords[3] - coords[1] 
                                tap_y = coords[3] + int(search_box_height * 0.5) 
                                bot.tap(center_x, tap_y)
                                bot.wait(3)
                    
                    # Pass the mapped_data to your post helper
                    if self._execute_group_share_post(bot, mapped_data):
                        shares_done += 1
                        update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Shared to group ({shares_done}/{target_count})")
                        if not self._robust_clear_search_box(bot, ld_name, acc_id, update_ld_signal, active_search_box, group_name): break 
                    else:
                        bot.press_back() 
                        bot.wait(1.5)
                        if not self._robust_clear_search_box(bot, ld_name, acc_id, update_ld_signal, active_search_box, group_name): break
                            
        # =======================================================
        # PATH B: SUGGESTED LIST
        # =======================================================
        elif use_suggest:
            for i in range(target_count):
                if stop_event.is_set(): break
                update_ld_signal.emit(ld_name, f"[{acc_id}] 💡 Sharing to suggested group ({shares_done+1}/{target_count})")
                
                search_element = bot.find_elements(search_input, timeout=4)
                if isinstance(search_element, list) and len(search_element) > 0:
                    bounds = search_element[0].get_attribute("bounds")
                    if bounds:
                        coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                        if len(coords) == 4:
                            center_x = (coords[0] + coords[2]) // 2
                            tap_y = coords[3] + int(bot.size['height'] * 0.12)
                            bot.tap(center_x, tap_y)
                            bot.wait(3)
                            
                            if self._execute_group_share_post(bot, mapped_data):
                                shares_done += 1
                                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Shared to group ({shares_done}/{target_count})")
                                swipe_start_y = tap_y + int(bot.size['height'] * 0.15)
                                bot.swipe(center_x, swipe_start_y, center_x, tap_y, speed_ms=1000)
                                bot.wait(2)
                            else:
                                bot.press_back()
                                bot.wait(1)
                else: break
        
        # 6. SAFELY EXIT
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🔙 Finished sharing to {shares_done} groups.")
        for _ in range(3): 
            bot.press_back()
            bot.wait(1)
            
        return True

    def _nav_to_video_creator(self, acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
        """Navigates to the standard Post -> Photo/Video creation screen."""
        if stop_event.is_set(): return False
        self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
        
        create_btn = '//android.widget.Button[@content-desc="Create, Double tap to create a new post, story, or reel"]'
        if bot.exists_xpath(create_btn, timeout=5):
            bot.click_xpath(create_btn)
            bot.wait(0.5)
            
            post_btn = '//android.widget.Button[@content-desc="Post"]'
            if bot.exists_xpath(post_btn, timeout=3):
                bot.click_xpath(post_btn)
                bot.wait(0.5)
                
                photo_video_btn = '//android.view.ViewGroup[@content-desc="Photo/video"]'
                if bot.exists_xpath(photo_video_btn, timeout=3):
                    bot.click_xpath(photo_video_btn)
                    bot.wait(0.5)
                    return True
                    
        return False

    def _select_injected_video_for_post(self, acc_id, ld_name, bot, update_ld_signal):
        """Clears permissions, selects the latest video, and advances."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🛡️ Checking Camera/Storage permissions")
        all_dismiss_buttons = f"{self.allow_btn} | {self.continue_btn}"
        for _ in range(3):
            if bot.exists_xpath(all_dismiss_buttons, timeout=0.5):
                bot.click_xpath(all_dismiss_buttons)
                bot.wait(0.5)
            else:
                break

        update_ld_signal.emit(ld_name, f"[{acc_id}] 🎥 Selecting the video")
        bot.tap(bot.size['width'] // 4, int(bot.size['height'] * 0.42)) 
        bot.wait(3)

        # Standard post composer might require clicking "Done" or "Next" after selecting media
        done_btn = '//android.widget.Button[contains(@content-desc, "DONE") or contains(@content-desc, "Done") or contains(@content-desc, "NEXT") or contains(@content-desc, "Next")] | //android.view.ViewGroup[contains(@content-desc, "DONE") or contains(@content-desc, "Done") or contains(@content-desc, "NEXT") or contains(@content-desc, "Next")]'
        if bot.exists_xpath(done_btn, timeout=2):
            bot.click_xpath(done_btn)
            bot.wait(2)
            
        return True

    def _add_video_title_and_hashtags(self, acc_id, ld_name, bot, update_ld_signal, videos_data, video_filename):
        """Generates and types the title and hashtags into the Say Something box."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 📝 Writing Video Title & Hashtags...")
        title_input = '//android.widget.AutoCompleteTextView[contains(@text, "Say something about this video")] | //android.widget.EditText[contains(@text, "Say something")]'
        
        final_text = ""
        if videos_data.get("video_use_tittle_from_videos"):
            final_text += video_filename.replace('.mp4', '') + " "
        elif videos_data.get("video_use_fixed_tittle"):
            final_text += videos_data.get("video_tittle_text", "") + " "
            
        if videos_data.get("hastag_video"): # Using your specific key
            hashtag_pool = videos_data.get("post_videos_hastag", "") # Assumed key based on reel pattern
            if videos_data.get("video_use_fixed_hastag"):
                clean_fixed_tags = " ".join([f"#{tag.strip()}" if not tag.strip().startswith("#") else tag.strip() for tag in hashtag_pool.split(",") if tag.strip()])
                final_text += clean_fixed_tags + " "
            elif videos_data.get("video_use_random_hastag"):
                final_text += self.general_function.get_random_items_from_string(hashtag_pool, min_items=1, max_items=4, prefix="#", separator=" ")

        clean_final_text = final_text.strip()
        if bot.exists_xpath(title_input, timeout=3):
            bot.type_xpath(title_input, clean_final_text)
            bot.wait(1.5)
            bot.press_back() # hide keyboard
            
        return clean_final_text

    def _tag_people_in_videos(self, acc_id, ld_name, bot, update_ld_signal, target_tags):
        """Scrolls and systematically checks boxes to tag friends, uses BACK instead of Confirm."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 👥 Tagging {target_tags} friends in video")
        tag_btn = '//android.view.ViewGroup[@content-desc="Tag people"]'
        
        if bot.exists_xpath(tag_btn, timeout=2):
            bot.click_xpath(tag_btn)
            bot.wait(3)
            
            tags_done = 0
            checkbox_xpath = '//android.widget.CheckBox'
            
            for _ in range(5):
                initial_boxes = bot.find_elements(checkbox_xpath, timeout=2)
                visible_count = len(initial_boxes)
                
                for i in range(visible_count):
                    if tags_done >= target_tags: break
                    try:
                        fresh_boxes = bot.find_elements(checkbox_xpath, timeout=1)
                        if i < len(fresh_boxes):
                            cb = fresh_boxes[i]
                            if cb.get_attribute("checked") == "false":
                                cb.click()
                                tags_done += 1
                                bot.wait(1.5) 
                    except Exception: pass
                        
                if tags_done >= target_tags: break
                bot.scroll_down(speed_ms=1900)
                bot.wait(2)

            # 🟢 SPECIFIC TO VIDEOS: No confirm button, just press back
            bot.press_back()
            bot.wait(2)

    def _add_location_to_video(self, acc_id, ld_name, bot, update_ld_signal, check_in_word):
        """Searches for a location via the Check In button."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 📍 Adding video location: {check_in_word}")
        loc_btn = '//android.view.ViewGroup[@content-desc="Check in"]'
        
        if bot.exists_xpath(loc_btn, timeout=2):
            bot.click_xpath(loc_btn)
            bot.wait(2)
            
            turn_on = '//android.view.ViewGroup[@content-desc="Turn on"]'
            for _ in range(4):
                if bot.exists_xpath(self.allow_btn, timeout=1):
                    bot.click_xpath(self.allow_btn)
                    bot.wait(1)
                if bot.exists_xpath(turn_on, timeout=1):
                    bot.click_xpath(turn_on)
                    bot.wait(1)

            search_input = '//android.widget.EditText[@text="Search" or contains(@text, "Search")]'
            if bot.exists_xpath(search_input, timeout=3):
                bot.click_xpath(search_input)
                bot.type_xpath(search_input, check_in_word)
                bot.press_backspace(1)
                bot.wait(4)

                result_xpath = f'//android.view.ViewGroup[contains(@content-desc, "More actions, {check_in_word[:5]}")]'
                result_element = bot.find_elements(result_xpath, timeout=5)
                
                if result_element:
                    bounds = result_element[0].get_attribute("bounds")
                    if bounds:
                        coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                        if len(coords) == 4:
                            center_x = ((coords[0] + coords[2]) // 2) - 120
                            center_y = (coords[1] + coords[3]) // 2
                            bot.tap(center_x, center_y)
                            bot.wait(2)
                else:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Location result not found. Skipping...")
                    bot.tap_percentage(50, 60)

    def _set_ai_label_for_video(self, acc_id, ld_name, bot, update_ld_signal):
        """Turns on the AI label specifically for the video UI."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🤖 Activating AI Label...")
        ai_btn = '//android.view.ViewGroup[@content-desc="AI label off"]'
        if bot.exists_xpath(ai_btn, timeout=2):
            bot.click_xpath(ai_btn)
            bot.wait(1.5)
            
            toggle_btn = '//android.widget.Switch'
            if bot.exists_xpath(toggle_btn, timeout=2):
                switch_elements = bot.find_elements(toggle_btn, timeout=2)
                if switch_elements and switch_elements[0].get_attribute("checked") == "false":
                    bot.click_xpath(toggle_btn)
                    bot.wait(1)
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ AI Label turned ON")
            
            # Escape back to composer
            bot.press_back()
            bot.wait(1)

    def _add_feeling_to_video(self, acc_id, ld_name, bot, update_ld_signal, videos_data):
        """Adds a feeling to the video post based on JSON data."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🎭 Adding Feeling/Activity...")
        
        # 1. Click the Feeling/activity button
        feeling_btn = '//android.view.ViewGroup[@content-desc="Feeling/activity"]'
        if bot.exists_xpath(feeling_btn, timeout=3):
            bot.click_xpath(feeling_btn)
            bot.wait(2.5)
        else:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Feeling/activity button not found.")
            return

        # 2. Map the JSON keys to the exact Facebook content-desc
        feeling_map = {
            "feeling_happy_video": "happy",
            "feeling_blessed_video": "blessed",
            "feeling_loved_video": "loved",
            "feeling_sad_video": "sad",
            "feeling_lovely_video": "lovely",
            "feeling_crazy_video": "crazy",
            "feeling_thankful_video": "thankful",
            "feeling_inlove_video": "in love", # Note the space matching the UI!
            "feeling_excited_video": "excited"
        }

        selected_feeling = None

        # 3. Determine which feeling to pick
        if videos_data.get("feeling_random_video"):
            selected_feeling = random.choice(list(feeling_map.values()))
        else:
            # Find the first one that is marked True
            for key, desc in feeling_map.items():
                if videos_data.get(key):
                    selected_feeling = desc
                    break
        
        # Fallback just in case they enabled "use_feeling" but forgot to check a box
        if not selected_feeling:
            selected_feeling = "happy"

        update_ld_signal.emit(ld_name, f"[{acc_id}] 🎭 Selecting feeling: '{selected_feeling}'")
        
        # 4. Find and click the selected feeling
        target_feeling_xpath = f'//android.view.ViewGroup[@content-desc="{selected_feeling}"]'
        
        found = False
        for _ in range(3): # Scroll a few times in case the feeling is lower down
            if bot.exists_xpath(target_feeling_xpath, timeout=2):
                bot.click_xpath(target_feeling_xpath)
                found = True
                break
            bot.scroll_down(speed_ms=1000)
            bot.wait(1)
            
        if not found:
            update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ Could not find '{selected_feeling}'. Escaping...")
            bot.press_back() # Escape the menu so it doesn't get stuck

        bot.wait(2) # Wait for it to return to the composer UI

    def process_posts_videos(self, acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, data_acc, appium_name, stop_event):
        # 1. RETRIEVE SETTINGS & VALIDATE
        data = self.data_manager.get_post_setting_by_id(acc_id)
        if not data: return True, "No Video settings found"
            
        videos_data = data.get("post_videos", {})
        if not videos_data.get("post_video", False): return True, "Video posting is disabled"

        total_posts = videos_data.get("total_posts_video", 1)
        videos_path = videos_data.get("videos_tab_videos_path", "")

        if not os.path.exists(videos_path):
            update_acc_signal.emit(acc_id, True, {"status": f"❌ Videos folder path invalid"})
            return False, f"Videos folder path invalid"

        update_acc_signal.emit(acc_id, False, {"status": f"🎬 Starting Long Video Posting ({total_posts} target)"})
        failed_comments = 0
        failed_shares = 0
        posts_count = 0
        
        # 2. MAIN LOOP
        try:
            for post_index in range(total_posts):
                if stop_event.is_set(): return False, "Stopped by user"
                
                # REFRESH VIDEO LIST EVERY LOOP
                local_videos = glob.glob(os.path.join(videos_path, "*.mp4"))
                if not local_videos:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ No more videos in folder. Stopping.")
                    break

                selected_video = random.choice(local_videos)
                video_filename = os.path.basename(selected_video)
                
                update_acc_signal.emit(acc_id, False, {"status": f"🔄 Video Post ({post_index+1}/{total_posts})"})

                # A. INJECT VIDEO (Reusing Reel Helper)
                success, msg = self._inject_video_via_adb(acc_id, ld_name, appium_name, selected_video, update_acc_signal, update_ld_signal, post_index, total_posts)
                if not success: return False, msg
                bot.wait(2)
                
                # B. NAVIGATE & SELECT
                if not self._nav_to_video_creator(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
                    return False, "Could not navigate to Video creation screen"
                
                if not self._select_injected_video_for_post(acc_id, ld_name, bot, update_ld_signal):
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    continue

                # C. DETAILS
                posted_title = self._add_video_title_and_hashtags(acc_id, ld_name, bot, update_ld_signal, videos_data, video_filename)
                
                if videos_data.get("video_tag"):
                    target_tags = random.randint(videos_data.get("video_tag_from", 1), videos_data.get("video_tag_to", 3))
                    self._tag_people_in_videos(acc_id, ld_name, bot, update_ld_signal, target_tags)

                if videos_data.get("use_feeling_video"):
                    self._add_feeling_to_video(acc_id, ld_name, bot, update_ld_signal, videos_data)

                if videos_data.get("video_check_in") and videos_data.get("video_check_in_word"):
                    self._add_location_to_video(acc_id, ld_name, bot, update_ld_signal, videos_data.get("video_check_in_word"))
                    
                if videos_data.get("ai_label_videos"):
                    self._set_ai_label_for_video(acc_id, ld_name, bot, update_ld_signal)

                # D. UPLOAD
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Uploading Video...")
                post_btn = '//android.view.ViewGroup[@content-desc="POST" or @content-desc="Post"] | //android.widget.Button[contains(@content-desc, "POST")]'
                
                # if bot.exists_xpath(post_btn, timeout=2):
                #     bot.click_xpath(post_btn)
                # else:
                #     bot.tap(int(bot.size['width'] * 0.90), int(bot.size['height'] * 0.08)) # Forced fallback tap
                
                # Videos take longer than reels to compress and upload
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⏳ Waiting 45s for video upload to finish...")
                bot.wait(45) 
                
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Video {post_index+1} posted!")
                posts_count += 1
                
                # E. MOVE FILE
                try:
                    posted_folder = os.path.join(videos_path, "posted")
                    if not os.path.exists(posted_folder): os.makedirs(posted_folder)
                    shutil.move(selected_video, os.path.join(posted_folder, video_filename))
                except Exception as e:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ File move failed: {e}")
                
                # F. AUTO-COMMENT (Using your Video keys)
                if videos_data.get("video_comments"): 
                    raw_comment = videos_data.get("video_comments_text", "")
                    final_comment = ""
                    if raw_comment.strip():
                        if videos_data.get("video_comments_use_random"):
                            comment_pool = [c.strip() for c in raw_comment.split(",") if c.strip()]
                            if comment_pool: final_comment = random.choice(comment_pool)
                        elif videos_data.get("video_comments_use_fixed"):
                            final_comment = raw_comment.strip()
                            
                        if final_comment:
                            # Reuses the exact same logic as Reels to find the post on the profile
                            if not self._comment_on_own_post(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, final_comment, posted_title, stop_event):
                                failed_comments += 1

                # G. SHARE TO GROUPS
                if videos_data.get("share_to_group_video"):
                    mapped_data = {
                        "share_to_group_use_by_seleted": videos_data.get("share_to_group_use_by_seleted_video", False),
                        "share_to_group_use_by_suggest": videos_data.get("share_to_group_use_by_suggest_video", False),
                        "share_to_group_from": videos_data.get("share_to_group_from_video", 1),
                        "share_to_group_to": videos_data.get("share_to_group_to_video", 1),
                        "groups_to_post": videos_data.get("groups_to_post_videos", []),
                        
                        "share_to_group_tittle": videos_data.get("share_to_group_tittle_videos"),
                        "share_to_group_word": videos_data.get("share_group_tittle_videos_words", ""),
                        "use_fixed_share_group_tittle": videos_data.get("use_fixed_share_group_tittle_videos"),
                        "use_random_share_group_tittle": videos_data.get("use_random_share_group_tittle_videos")
                    }

                    if not self._universal_share_to_groups(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, mapped_data, posted_title, stop_event):
                        failed_shares += 1

                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)

            # FINAL REPORT
            final_msg = f"Successfully posted {posts_count} Videos"
            has_failures = (failed_comments > 0 or failed_shares > 0)
            if failed_comments > 0: final_msg += f" | ❌ {failed_comments} Comment Fails"
            if failed_shares > 0: final_msg += f" | ❌ {failed_shares} Share Fails"
            update_acc_signal.emit(acc_id, True, {"status": final_msg})
            return (not has_failures), final_msg

        except Exception as e:
            error_msg = f"Post Video Crash: {str(e)}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            update_acc_signal.emit(acc_id, True, {"status": f"❌ {error_msg}"})
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg

    # =====================================================================
    # MULTIPLE IMAGE MODULE HELPERS
    # =====================================================================
    def _inject_images_via_adb(self, acc_id, ld_name, appium_name, selected_images, update_acc_signal, update_ld_signal, post_index, total_posts):
        """Pushes multiple images to the emulator and triggers media scans."""
        for idx, img_path in enumerate(selected_images):
            filename = os.path.basename(img_path)
            update_acc_signal.emit(acc_id, False, {"status": f"📥 Pushing Image {idx+1}/{len(selected_images)} for Post {post_index+1}"})
            
            # Using unique names so they don't overwrite each other
            remote_path = f"/sdcard/DCIM/Camera/latest_img_{idx}.jpg"
            push_result = self.ld_manager.run_adb(f'push "{img_path}" {remote_path}', device=appium_name)
            
            if push_result is None:
                update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ ADB push failed for {filename}")
                return False, f"ADB push failed for {filename}"
                
            self.ld_manager.run_adb(
                f'shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{remote_path}',
                device=appium_name
            )
        return True, "Success"
    
    def _select_injected_images_for_post(self, acc_id, ld_name, bot, update_ld_signal, num_images, images_data):
        """Finds, scrolls, and clicks images until num_images is reached."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🛡️ Checking permissions...")
        all_dismiss_buttons = f"{self.allow_btn} | {self.continue_btn}"
        for _ in range(3):
            if bot.exists_xpath(all_dismiss_buttons, timeout=0.5):
                bot.click_xpath(all_dismiss_buttons)
                bot.wait(0.5)
            else:
                break

        update_ld_signal.emit(ld_name, f"[{acc_id}] 🖼️ Aiming to select {num_images} images...")
        bot.wait(3) 
        
        # 1. ENABLE MULTI-SELECT
        if num_images > 1:
            select_multiple_btn = '//android.view.ViewGroup[@content-desc="Select multiple" or contains(@content-desc, "Select Multiple")]'
            if bot.exists_xpath(select_multiple_btn, timeout=3):
                bot.click_xpath(select_multiple_btn)
                bot.wait(1.5)

        # 2. SCAN & CLICK LOOP
        found_centers = [] # Keeps track of what we already clicked
        photo_xpath = '//android.view.ViewGroup[contains(@content-desc, "Photo taken")] | //android.view.ViewGroup[contains(@content-desc, "Photo")]'
        
        # We allow up to 5 scrolls to find enough images
        for scroll_attempt in range(5):
            if len(found_centers) >= num_images:
                break
                
            photo_elements = bot.find_elements(photo_xpath, timeout=3)
            new_found_in_this_pass = 0
            
            for el in photo_elements:
                if len(found_centers) >= num_images: break
                try:
                    bounds = el.get_attribute("bounds")
                    if not bounds: continue
                    coords = [int(n) for n in bounds.replace('[', '').replace(']', ',').split(',') if n]
                    if len(coords) != 4: continue
                        
                    cx, cy = (coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2
                    
                    # Check if we already clicked this unique coordinate (30px margin)
                    if not any(abs(ux - cx) < 30 and abs(uy - cy) < 30 for (ux, uy) in found_centers):
                        bot.tap(cx, cy)
                        bot.wait(0.6)
                        found_centers.append((cx, cy))
                        new_found_in_this_pass += 1
                except Exception: pass
            
            # If we still need more images, scroll down
            if len(found_centers) < num_images:
                bot.scroll_down(speed_ms=1000)
                bot.wait(1.5)
            
        # 3. PROCEED TO COMPOSER
        next_btn = '//android.view.ViewGroup[@content-desc="Next" or contains(@content-desc, "NEXT")]'
        if bot.exists_xpath(next_btn, timeout=3):
            bot.click_xpath(next_btn)
            bot.wait(3)
        else:
            # Fallback if only 1 image selected
            bot.press_back()
            bot.wait(2)

        # 4. LAYOUT OPTIONS
        close_layout_btn = '//android.view.ViewGroup[@content-desc="Close layout options"]'
        if bot.exists_xpath(close_layout_btn, timeout=2):
            update_ld_signal.emit(ld_name, f"[{acc_id}] 🎨 Applying Image Layout...")
            layout_map = {
                "classic": '//android.view.ViewGroup[contains(@content-desc, "grid format, no text or borders")]',
                "column": '//android.view.ViewGroup[contains(@content-desc, "vertical columns")]',
                "banner": '//android.view.ViewGroup[contains(@content-desc, "one top photo")]',
                "frame_layout": '//android.view.ViewGroup[contains(@content-desc, "grid format, with borders")]'
            }
            
            for key, xpath in layout_map.items():
                if images_data.get(key, False) and bot.exists_xpath(xpath, timeout=2):
                    bot.click_xpath(xpath)
                    bot.wait(1.5)
                    break
            bot.click_xpath(close_layout_btn)
            bot.wait(1.5)

        return True
    
    def _add_image_title_and_hashtags(self, acc_id, ld_name, bot, update_ld_signal, images_data, first_image_filename):
        """Generates and types the title and hashtags into the Say Something box."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 📝 Writing Image Title & Hashtags...")
        title_input = '//android.widget.AutoCompleteTextView[contains(@text, "Say something about this photo")] | //android.widget.EditText[contains(@text, "Say something")] | //android.widget.AutoCompleteTextView[contains(@text, "Say something")]'
        
        final_text = ""
        # 1. Title Logic
        if images_data.get("use_tittle_from_image"):
            # Strip extension
            clean_filename = os.path.splitext(first_image_filename)[0]
            final_text += clean_filename + " "
        elif images_data.get("use_fixed_tittle_image"):
            final_text += images_data.get("tittle_image_word", "") + " "
            
        # 2. Hashtag Logic
        if images_data.get("hastag_image"):
            hashtag_pool = images_data.get("image_hastag_word", "")
            if images_data.get("use_fixed_hastag_image"):
                clean_fixed_tags = " ".join([f"#{tag.strip()}" if not tag.strip().startswith("#") else tag.strip() for tag in hashtag_pool.split(",") if tag.strip()])
                final_text += clean_fixed_tags + " "
            elif images_data.get("use_random_hastag_image"):
                final_text += self.general_function.get_random_items_from_string(hashtag_pool, min_items=1, max_items=4, prefix="#", separator=" ")

        clean_final_text = final_text.strip()
        
        # 3. Type it in
        if bot.exists_xpath(title_input, timeout=3):
            bot.type_xpath(title_input, clean_final_text)
            bot.wait(1.5)
            bot.press_back() # hide keyboard
            bot.wait(1)
            
        return clean_final_text

    def _add_feeling_to_image(self, acc_id, ld_name, bot, update_ld_signal, images_data):
        """Adds a feeling to the image post based on JSON data."""
        update_ld_signal.emit(ld_name, f"[{acc_id}] 🎭 Adding Feeling/Activity...")
        feeling_btn = '//android.view.ViewGroup[@content-desc="Feeling/activity"]'
        if bot.exists_xpath(feeling_btn, timeout=3):
            bot.click_xpath(feeling_btn)
            bot.wait(2.5)
        else:
            return

        feeling_map = {
            "feeling_happy_image": "happy",
            "feeling_blessed_image": "blessed",
            "feeling_loved_image": "loved",
            "feeling_sad_image": "sad",
            "feeling_lovely_image": "lovely",
            "feeling_crazy_image": "crazy",
            "feeling_thankful_image": "thankful",
            "feeling_inlove_image": "in love", 
            "feeling_excited_image": "excited"
        }

        selected_feeling = None
        if images_data.get("feeling_random_image"):
            selected_feeling = random.choice(list(feeling_map.values()))
        else:
            for key, desc in feeling_map.items():
                if images_data.get(key):
                    selected_feeling = desc
                    break
        
        if not selected_feeling: selected_feeling = "happy"

        update_ld_signal.emit(ld_name, f"[{acc_id}] 🎭 Selecting feeling: '{selected_feeling}'")
        target_feeling_xpath = f'//android.view.ViewGroup[@content-desc="{selected_feeling}"]'
        
        found = False
        for _ in range(3): 
            if bot.exists_xpath(target_feeling_xpath, timeout=2):
                bot.click_xpath(target_feeling_xpath)
                found = True
                break
            bot.scroll_down(speed_ms=1000)
            bot.wait(1)
            
        if not found: bot.press_back()
        bot.wait(2) 

    def process_posts_images(self, acc_id, ld_name, bot, update_acc_signal, update_ld_signal, dynamic_tabs, tab_bar_xpaths, data_acc, appium_name, stop_event):
        # 1. RETRIEVE SETTINGS & VALIDATE
        data = self.data_manager.get_post_setting_by_id(acc_id)
        if not data: return True, "No Image settings found"
            
        images_data = data.get("post_images", {})
        if not images_data.get("post_image", False): return True, "Image posting is disabled"

        total_posts = images_data.get("total_posts_image", 1)
        images_per_post = images_data.get("total_per_post_image", 1)
        images_path = images_data.get("image_path", "")

        if not os.path.exists(images_path):
            update_acc_signal.emit(acc_id, True, {"status": f"❌ Images folder path invalid"})
            return False, f"Images folder path invalid"

        update_acc_signal.emit(acc_id, False, {"status": f"🎬 Starting Image Posting ({total_posts} posts)"})
        failed_comments = 0
        failed_shares = 0
        posts_count = 0
        
        # 2. MAIN LOOP
        try:
            for post_index in range(total_posts):
                if stop_event.is_set(): return False, "Stopped by user"
                
                # A. REFRESH & SELECT MULTIPLE IMAGES
                local_images = []
                for ext in ('*.jpg', '*.jpeg', '*.png'):
                    local_images.extend(glob.glob(os.path.join(images_path, ext)))
                
                if not local_images:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ No more images in folder. Stopping.")
                    break

                # Safely pick up to the requested number of images
                actual_images_to_pick = min(images_per_post, len(local_images))
                selected_images = random.sample(local_images, actual_images_to_pick)
                first_image_filename = os.path.basename(selected_images[0])
                
                update_acc_signal.emit(acc_id, False, {"status": f"🔄 Image Post ({post_index+1}/{total_posts})"})

                # B. INJECT IMAGES
                success, msg = self._inject_images_via_adb(acc_id, ld_name, appium_name, selected_images, update_acc_signal, update_ld_signal, post_index, total_posts)
                if not success: return False, msg
                bot.wait(1)
                
                # C. NAVIGATE & SELECT (Reusing Video Navigator because UI is identical!)
                if not self._nav_to_video_creator(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, tab_bar_xpaths, stop_event):
                    return False, "Could not navigate to Image creation screen"
                
                if not self._select_injected_images_for_post(acc_id, ld_name, bot, update_ld_signal, actual_images_to_pick, images_data):
                    self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
                    continue

                # =========================================================
                # D. DETAILS (Titles, Tags, Feelings, AI Label, Location)
                # =========================================================
                posted_title = self._add_image_title_and_hashtags(acc_id, ld_name, bot, update_ld_signal, images_data, first_image_filename)

                if images_data.get("use_feeling_image"):
                    self._add_feeling_to_image(acc_id, ld_name, bot, update_ld_signal, images_data)

                if images_data.get("tag_image"):
                    target_tags = random.randint(images_data.get("tag_from_image", 1), images_data.get("tag_to_image", 3))
                    self._tag_people_in_videos(acc_id, ld_name, bot, update_ld_signal, target_tags) # Reuse Video Tag Helper

                if images_data.get("check_in_image") and images_data.get("check_in_image_word"):
                    self._add_location_to_video(acc_id, ld_name, bot, update_ld_signal, images_data.get("check_in_image_word")) # Reuse Video Location Helper

                if images_data.get("ai_label_image"):
                    self._set_ai_label_for_video(acc_id, ld_name, bot, update_ld_signal) # Reuse Video AI Helper

                # =========================================================
                # E. UPLOAD
                # =========================================================
                update_ld_signal.emit(ld_name, f"[{acc_id}] 🚀 Uploading Image Post...")
                post_btn = '//android.view.ViewGroup[@content-desc="POST" or @content-desc="Post"] | //android.widget.Button[contains(@content-desc, "POST")]'
                
         

                # if bot.exists_xpath(post_btn, timeout=2): bot.click_xpath(post_btn)
                # else: bot.tap(int(bot.size['width'] * 0.90), int(bot.size['height'] * 0.08))
                
                update_ld_signal.emit(ld_name, f"[{acc_id}] ⏳ Waiting 20s for image upload to finish...")
                bot.wait(20) 
                
                update_ld_signal.emit(ld_name, f"[{acc_id}] ✅ Image Post {post_index+1} successful!")
                posts_count += 1
                
                # F. MOVE ALL SELECTED FILES TO 'POSTED'
                try:
                    posted_folder = os.path.join(images_path, "posted")
                    if not os.path.exists(posted_folder): os.makedirs(posted_folder)
                    for img_path in selected_images:
                        shutil.move(img_path, os.path.join(posted_folder, os.path.basename(img_path)))
                except Exception as e:
                    update_ld_signal.emit(ld_name, f"[{acc_id}] ⚠️ File move failed: {e}")
                
                # =========================================================
                # G. AUTO-COMMENT 
                # =========================================================
                if images_data.get("comments_image"): 
                    raw_comment = images_data.get("comments_image_word", "")
                    final_comment = ""
                    if raw_comment.strip():
                        if images_data.get("comments_use_random_image"):
                            comment_pool = [c.strip() for c in raw_comment.split(",") if c.strip()]
                            if comment_pool: final_comment = random.choice(comment_pool)
                        elif images_data.get("comments_use_fixed_image"):
                            final_comment = raw_comment.strip()
                            
                        if final_comment:
                            if not self._comment_on_own_post(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, final_comment, posted_title, stop_event):
                                failed_comments += 1

                # =========================================================
                # H. SHARE TO GROUPS
                # =========================================================
                if images_data.get("share_to_group_image"):
                    
                    # Map image-specific keys to the universal keys
                    mapped_data = {
                        "share_to_group_use_by_seleted": images_data.get("share_to_group_use_by_seleted_image", False),
                        "share_to_group_use_by_suggest": images_data.get("share_to_group_use_by_suggest_image", False),
                        "share_to_group_from": images_data.get("share_to_group_from_image", 1),
                        "share_to_group_to": images_data.get("share_to_group_to_image", 1),
                        "groups_to_post": images_data.get("groups_to_post_image", []),
                        
                        "share_to_group_tittle": images_data.get("share_to_group_tittle_image"),
                        "share_to_group_word": images_data.get("share_to_group_word_image", ""),
                        "use_fixed_share_group_tittle": images_data.get("use_fixed_share_group_tittle_image"),
                        "use_random_share_group_tittle": images_data.get("use_random_share_group_tittle_image")
                    }

                    if not self._universal_share_to_groups(acc_id, ld_name, appium_name, bot, update_ld_signal, dynamic_tabs, mapped_data, posted_title, stop_event):
                        failed_shares += 1

                # Reset to Feed for next loop iteration
                self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)

            # FINAL REPORT
            final_msg = f"Successfully posted {posts_count} Image Posts"
            has_failures = (failed_shares > 0 or failed_comments > 0)
            if failed_comments > 0: final_msg += f" | ❌ {failed_comments} Comment Fails"
            if failed_shares > 0: final_msg += f" | ❌ {failed_shares} Share Fails"
            update_acc_signal.emit(acc_id, True, {"status": final_msg})
            return (not has_failures), final_msg

        except Exception as e:
            error_msg = f"Post Image Crash: {str(e)}"
            update_ld_signal.emit(ld_name, f"[{acc_id}] ❌ {error_msg}")
            update_acc_signal.emit(acc_id, True, {"status": f"❌ {error_msg}"})
            self.ensure_on_home(appium_name, bot, tab_bar_xpaths, stop_event)
            return False, error_msg



































