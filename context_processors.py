"""Template context for branding and SEO (Nitesh Kumar Singh / nkscoder)."""

from pathlib import Path

from django.urls import reverse

from .conf import get_setting


def feedback_open_source(request):
    author_name = get_setting("AUTHOR_NAME")
    author_handle = get_setting("AUTHOR_HANDLE")
    package_name = get_setting("PACKAGE_NAME")
    seo_site = get_setting("SEO_SITE_NAME")
    path = getattr(request, "path", "") or ""
    page_title = path.strip("/").replace("/", " ").title() or "Feedback"
    seo_title = f"{page_title} — {seo_site} | {author_name} ({author_handle})"

    license_url = ""
    try:
        license_url = request.build_absolute_uri(reverse("feedback:license"))
    except Exception:
        license_url = get_setting("GITHUB_URL") + "/blob/main/LICENSE"

    canonical = ""
    try:
        canonical = request.build_absolute_uri()
    except Exception:
        canonical = get_setting("HOMEPAGE_URL")

    license_text = ""
    license_path = Path(__file__).resolve().parent / "LICENSE"
    if license_path.is_file():
        license_text = license_path.read_text(encoding="utf-8")

    return {
        "feedback_author_name": author_name,
        "feedback_author_handle": author_handle,
        "feedback_github_url": get_setting("GITHUB_URL"),
        "feedback_homepage_url": get_setting("HOMEPAGE_URL"),
        "feedback_pypi_url": get_setting("PYPI_URL"),
        "feedback_package_name": package_name,
        "feedback_package_version": get_setting("PACKAGE_VERSION"),
        "feedback_seo_site_name": seo_site,
        "feedback_seo_title": seo_title,
        "feedback_seo_description": get_setting("SEO_DESCRIPTION"),
        "feedback_seo_keywords": get_setting("SEO_KEYWORDS"),
        "feedback_canonical_url": canonical,
        "feedback_license_url": license_url,
        "feedback_license_text": license_text,
    }
