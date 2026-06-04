# nkscoder-django-feedback — Documentation

**Package:** `nkscoder-django-feedback`  
**Author:** [Nitesh Kumar Singh (nkscoder)](https://nkscoder.in)  
**Repository:** https://github.com/nkscoder/feedback  
**PyPI:** https://pypi.org/project/nkscoder-django-feedback/

---

## Overview

`nkscoder-django-feedback` is a self-contained Django application for collecting and analyzing user feedback. It is designed by **Nitesh Kumar Singh** under the **nkscoder** brand as a plug-and-play module for any Django project.

### Screenshots

| UI | Preview |
|----|---------|
| Feedback form | ![Form](../docs/screenshots/feedback-form.png) |
| AI dashboard | ![Dashboard](../docs/screenshots/ai-dashboard.png) |

See [docs/screenshots/README.md](docs/screenshots/README.md) to replace with captures from your project.

---

## Installation reference

```bash
pip install nkscoder-django-feedback
```

Add to `INSTALLED_APPS`, run migrations, include URLs, and register the context processor (see [README.md](README.md)).

---

## URL routes

| Path | View name | Description |
|------|-----------|-------------|
| `submit/` | `feedback:submit_feedback` | POST endpoint for form submissions |
| `dashboard/` | `feedback:ai_dashboard` | Staff AI analytics UI |
| `dashboard/api/` | `feedback:ai_dashboard_api` | JSON stats & chart data |
| `license/` | `feedback:license` | Public MIT license (SEO) |

---

## Data model: `Feedback`

| Field | Type | Notes |
|-------|------|-------|
| `user` | FK → `AUTH_USER_MODEL`, nullable | Authenticated submitter |
| `name` | `CharField` | Guest name |
| `email` | `EmailField` | Guest email |
| `message` | `TextField` | Required feedback body |
| `rating` | `1–5`, optional | Star rating |
| `category` | `CharField` | e.g. bug, feature, praise |
| `source` | `CharField` | Page or route identifier |
| `link_type` | `CharField` | Generic link type (default `generic`) |
| `link_id` | `CharField` | External record id |
| `extra_data` | `JSONField` | Custom metadata |
| `session_key` | `CharField` | Anonymous cooldown key |
| `submitted_at` | `DateTimeField` | Auto timestamp |

**Property:** `submitter_display` — user name, guest name, email, or `"Anonymous"`.

---

## Services API (`feedback.services`)

### `is_feedback_allowed(request) -> bool`

Returns whether the current user or session may submit again (respects `FEEDBACK_COOLDOWN_DAYS` and `FEEDBACK_REQUIRE_AUTH`).

### `get_last_feedback(request) -> Feedback | None`

Latest submission for the current user or anonymous session.

### `create_feedback(request, message, **extra) -> Feedback | None`

Creates a row if cooldown allows. Optional kwargs: `name`, `email`, `rating`, `category`, `source`, `link_type`, `link_id`, `extra_data`.

### `build_feedback_kwargs(request, message, **extra) -> dict`

Builds model kwargs without saving (for custom flows).

---

## Forms (`feedback.forms.FeedbackForm`)

Model form for `name`, `email`, `message`, `rating`, `category`. Respects `FEEDBACK_MESSAGE_MAX_LENGTH` and `FEEDBACK_REQUIRE_EMAIL`.

---

## Analytics (`feedback.analytics`)

### `get_dashboard_context(days=30) -> dict`

Returns template context for the AI dashboard:

- Counts, average rating, auth vs anonymous split
- Chart JSON (`rating_*`, `category_*`, `source_*`, `trend_*`, `sentiment_*`)
- `ai_insights` — list of insight strings
- `ai_insights_source` — `"rules"` or `"openai"`
- `recent_feedback` — queryset for table

### `build_ai_insights(stats) -> list[str]`

Rule-based insight bullets (no API key required).

### `try_openai_summary(insights, stats) -> list[str] | None`

Optional LLM summary when `openai` is installed and `FEEDBACK_OPENAI_API_KEY` is set.

---

## Configuration (`FEEDBACK_*`)

Defined in `feedback/conf.py`. Override in Django `settings.py`.

**Branding & SEO (Nitesh Kumar Singh / nkscoder):**

| Key | Purpose |
|-----|---------|
| `AUTHOR_NAME` | Full name in templates & meta |
| `AUTHOR_HANDLE` | `nkscoder` handle |
| `GITHUB_URL` | Source repository |
| `HOMEPAGE_URL` | https://nkscoder.in |
| `PYPI_URL` | PyPI project page |
| `PACKAGE_NAME` | `nkscoder-django-feedback` |
| `SEO_SITE_NAME` | Browser / OG site title |
| `SEO_DESCRIPTION` | Meta description |
| `SEO_KEYWORDS` | Meta keywords |

---

## Context processor

`feedback.context_processors.feedback_open_source` injects branding and SEO variables into every template:

- `feedback_author_name`, `feedback_author_handle`
- `feedback_seo_title`, `feedback_seo_description`, `feedback_seo_keywords`
- `feedback_canonical_url`, `feedback_license_url`, `feedback_license_text`
- `feedback_github_url`, `feedback_pypi_url`, `feedback_homepage_url`
- `feedback_package_name`, `feedback_package_version`

Required for `feedback/base.html`, `_seo_head.html`, and `_opensource_footer.html`.

---

## Admin

`FeedbackAdmin` lists submitter, category, rating, message preview, source, link type, and submitted time. Search: name, email, message, category, user username.

---

## SEO implementation

1. **HTML meta** — description, keywords, author, robots, canonical
2. **Open Graph** — `og:title`, `og:description`, `og:url`, `og:site_name`
3. **Twitter Card** — summary card with creator `@nkscoder`
4. **JSON-LD** — `SoftwareApplication` with author `Nitesh Kumar Singh` / `nkscoder`
5. **Public `/feedback/license/`** — indexable license page with copyright
6. **Footer** — attribution links to GitHub, PyPI, nkscoder.in

Customize via `FEEDBACK_SEO_*` settings for your product name while keeping author attribution.

---

## Testing

```bash
python manage.py test feedback
```

---

## Versioning

- Package version: `feedback/__init__.py` → `__version__`
- PyPI: `pyproject.toml` → `[project].version`
- Keep both in sync before release.

---

## Support & attribution

Maintained by **Nitesh Kumar Singh (nkscoder)**.

When documenting or blogging about this package, please link:

- Author: https://nkscoder.in  
- GitHub: https://github.com/nkscoder/feedback  
- PyPI: https://pypi.org/project/nkscoder-django-feedback/

---

## License

MIT — Copyright © 2020–2026 Nitesh Kumar Singh (nkscoder). See [LICENSE](LICENSE).
