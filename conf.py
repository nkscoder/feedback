"""Configurable settings for the generic feedback package."""

from django.conf import settings


DEFAULTS = {
    "COOLDOWN_DAYS": 7,
    "REQUIRE_AUTH": False,
    "REQUIRE_EMAIL": False,
    "MESSAGE_MAX_LENGTH": 5000,
    "BASE_TEMPLATE": "feedback/base.html",
    "LOGIN_URL": "login",
    "SUBMIT_REDIRECT": "/",
    "DASHBOARD_DAYS": 30,
    "ENABLE_AI_DASHBOARD": True,
    "OPENAI_API_KEY": "",
    "OPENAI_MODEL": "gpt-4o-mini",
    "LINK_TYPES": [
        ("generic", "Generic"),
        ("page", "Page"),
        ("feature", "Feature"),
    ],
}


def get_setting(name):
    key = f"FEEDBACK_{name}"
    if hasattr(settings, key):
        return getattr(settings, key)
    return DEFAULTS[name]
