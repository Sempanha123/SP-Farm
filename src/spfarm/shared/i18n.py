"""Localization skeleton supporting English and Khmer (ភាសាខ្មែរ)."""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        # App Branding & Shell
        "app.title": "SP-Farm V2",
        "app.tagline": "Cute & Powerful Operations Platform",
        "command_palette.placeholder": "Type a command or jump to screen... (Ctrl+K)",
        "search.global": "Global search...",
        # Routes
        "route.dashboard": "Dashboard",
        "route.accounts": "Accounts",
        "route.pages": "Pages",
        "route.groups": "Groups",
        "route.devices": "Devices",
        "route.device_pool": "Device Pool",
        "route.apps": "Apps",
        "route.content": "Content",
        "route.campaigns": "Campaigns",
        "route.scheduler": "Scheduler",
        "route.jobs": "Jobs",
        "route.actions": "Actions",
        "route.providers": "Providers",
        "route.activity": "Activity & Logs",
        "route.analytics": "Analytics",
        "route.backups": "Backups",
        "route.settings": "Settings",
        # Common Actions
        "action.save": "Save Changes",
        "action.cancel": "Cancel",
        "action.refresh": "Refresh",
        "action.delete": "Delete",
        "action.edit": "Edit",
        "action.pause": "Pause",
        "action.resume": "Resume",
        "action.clear": "Clear",
        "action.search": "Search",
        "action.close": "Close",
        "action.apply": "Apply",
        # Status
        "status.ready": "Ready",
        "status.running": "Running",
        "status.offline": "Offline",
        "status.error": "Error",
        "status.warning": "Warning",
        "status.cooldown": "Cooldown",
        "status.active": "Active",
    },
    "km": {
        # App Branding & Shell
        "app.title": "SP-Farm V2",
        "app.tagline": "ប្រព័ន្ធប្រតិបត្តិការទំនើប និងងាយស្រួល",
        "command_palette.placeholder": "វាយពាក្យបញ្ជា ឬចូលទៅកាន់ទំព័រ... (Ctrl+K)",
        "search.global": "ស្វែងរកទូទៅ...",
        # Routes
        "route.dashboard": "ផ្ទាំងគ្រប់គ្រង",
        "route.accounts": "គណនី",
        "route.pages": "ទំព័រ (Pages)",
        "route.groups": "ក្រុម (Groups)",
        "route.devices": "ឧបករណ៍",
        "route.device_pool": "បណ្តុំឧបករណ៍ (Pool)",
        "route.apps": "កម្មវិធី (Apps)",
        "route.content": "មាតិកា",
        "route.campaigns": "យុទ្ធនាការ",
        "route.scheduler": "កាលវិភាគ",
        "route.jobs": "ការងារស្វ័យប្រវត្ត",
        "route.actions": "សកម្មភាព",
        "route.providers": "អ្នកផ្គត់ផ្គង់",
        "route.activity": "កំណត់ហេតុ និងសកម្មភាព",
        "route.analytics": "ការវិភាគ",
        "route.backups": "ការបម្រុងទុក",
        "route.settings": "ការកំណត់",
        # Common Actions
        "action.save": "រក្សាទុក",
        "action.cancel": "បោះបង់",
        "action.refresh": "ផ្ទុកឡើងវិញ",
        "action.delete": "លុប",
        "action.edit": "កែប្រែ",
        "action.pause": "ផ្អាក",
        "action.resume": "បន្ត",
        "action.clear": "សម្អាត",
        "action.search": "ស្វែងរក",
        "action.close": "បិទ",
        "action.apply": "អនុវត្ត",
        # Status
        "status.ready": "រួចរាល់",
        "status.running": "កំពុងដំណើរការ",
        "status.offline": "ក្រៅបណ្តាញ",
        "status.error": "កំហុស",
        "status.warning": "ការព្រមាន",
        "status.cooldown": "រង់ចាំសម្រាក",
        "status.active": "សកម្ម",
    },
}


class I18nManager:
    """Thread-safe localization string registry."""

    def __init__(self, default_lang: str = "en") -> None:
        self._current_lang = default_lang

    @property
    def current_language(self) -> str:
        return self._current_lang

    def set_language(self, lang_code: str) -> None:
        if lang_code in TRANSLATIONS:
            self._current_lang = lang_code
        else:
            logger.warning("Unsupported language code: %s; falling back to 'en'", lang_code)
            self._current_lang = "en"

    def translate(self, key: str, default: Optional[str] = None) -> str:
        lang_dict = TRANSLATIONS.get(self._current_lang, TRANSLATIONS["en"])
        if key in lang_dict:
            return lang_dict[key]
        # Fallback to English
        if key in TRANSLATIONS["en"]:
            return TRANSLATIONS["en"][key]
        return default if default is not None else key


# Global singleton instance
i18n = I18nManager()


def t(key: str, default: Optional[str] = None) -> str:
    """Convenience translation function."""
    return i18n.translate(key, default)
