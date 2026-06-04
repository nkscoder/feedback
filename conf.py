"""Configurable settings for nkscoder-django-feedback.

Author: Nitesh Kumar Singh (nkscoder) — https://nkscoder.in
"""

from django.conf import settings

from . import __version__


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
    "GITHUB_URL": "https://github.com/nkscoder/feedback",
    "HOMEPAGE_URL": "https://nkscoder.in",
    "PYPI_URL": "https://pypi.org/project/nkscoder-django-feedback/",
    "AUTHOR_NAME": "Nitesh Kumar Singh",
    "AUTHOR_HANDLE": "nkscoder",
    "PACKAGE_NAME": "nkscoder-django-feedback",
    "PACKAGE_VERSION": __version__,
    "SEO_SITE_NAME": "nkscoder Django Feedback",
    "SEO_DESCRIPTION": (
        "nkscoder-django-feedback — open-source Django user feedback plugin by "
        "Nitesh Kumar Singh (nkscoder): anonymous or authenticated submissions, "
        "ratings, cooldown rules, and an AI analytics dashboard for any Django project."
    ),
    "SEO_KEYWORDS": (
        "nkscoder-django-feedback,django feedback,user feedback,survey,analytics,"
        "ai dashboard,Nitesh Kumar Singh,nkscoder,open source,customer feedback,"
        "django plugin,feedback form,sentiment analysis"
    ),
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
