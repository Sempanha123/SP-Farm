"""Unit tests for localization and translation dictionaries."""

from spfarm.shared.i18n import I18nManager, t


def test_i18n_translation_english_default() -> None:
    mgr = I18nManager(default_lang="en")
    assert mgr.translate("route.dashboard") == "Dashboard"
    assert mgr.translate("route.accounts") == "Accounts"
    assert mgr.translate("action.save") == "Save Changes"
    assert mgr.translate("status.ready") == "Ready"


def test_i18n_translation_khmer() -> None:
    mgr = I18nManager(default_lang="km")
    assert mgr.translate("route.dashboard") == "ផ្ទាំងគ្រប់គ្រង"
    assert mgr.translate("route.accounts") == "គណនី"
    assert mgr.translate("action.save") == "រក្សាទុក"
    assert mgr.translate("status.ready") == "រួចរាល់"


def test_i18n_fallback_on_unknown_key_or_language() -> None:
    mgr = I18nManager(default_lang="en")
    assert mgr.translate("nonexistent.key", default="Custom Default") == "Custom Default"
    assert mgr.translate("nonexistent.key") == "nonexistent.key"

    # Unsupported lang falls back to english
    mgr.set_language("fr")
    assert mgr.translate("route.dashboard") == "Dashboard"


def test_global_t_helper() -> None:
    assert t("app.title") == "SP-Farm V2"
