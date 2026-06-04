# nkscoder-django-feedback

[![PyPI](https://img.shields.io/pypi/v/nkscoder-django-feedback?label=PyPI&logo=pypi)](https://pypi.org/project/nkscoder-django-feedback/)
[![Python](https://img.shields.io/pypi/pyversions/nkscoder-django-feedback)](https://pypi.org/project/nkscoder-django-feedback/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![nkscoder](https://img.shields.io/badge/author-Nitesh%20Kumar%20Singh%20(nkscoder)-blue)](https://nkscoder.in)

**Open-source Django feedback plugin by [Nitesh Kumar Singh (nkscoder)](https://nkscoder.in)**

Collect user feedback (authenticated or anonymous), enforce cooldown rules, and review submissions on an **AI analytics dashboard** with charts, sentiment keywords, and auto-generated insights.

| | |
|---|---|
| **Author / Maintainer** | [Nitesh Kumar Singh (nkscoder)](https://nkscoder.in) |
| **Website** | [nkscoder.in](https://nkscoder.in) |
| **GitHub** | [github.com/nkscoder/feedback](https://github.com/nkscoder/feedback) |
| **PyPI** | [`nkscoder-django-feedback`](https://pypi.org/project/nkscoder-django-feedback/) |
| **Meta install** | [`nkscoder[feedback]`](https://pypi.org/project/nkscoder/) on [PyPI @nkscoder](https://pypi.org/user/nkscoder/) |
| **Django app** | `feedback` |
| **Version** | 1.0.2 |
| **License** | [MIT](LICENSE) |

---

## Screenshots

### Feedback form

Embed this form in any Django template (authenticated or guest users, optional rating & category):

![Feedback form — nkscoder-django-feedback](https://raw.githubusercontent.com/nkscoder/feedback/main/docs/screenshots/feedback-form.png)

### AI analytics dashboard

Staff dashboard with charts, sentiment analysis, and auto-generated insights:

![AI Feedback Dashboard — Nitesh Kumar Singh (nkscoder)](https://raw.githubusercontent.com/nkscoder/feedback/main/docs/screenshots/ai-dashboard.png)

> Replace screenshots: add your own PNGs under `docs/screenshots/` after customizing templates in your project.

---

## Table of contents

- [Screenshots](#screenshots)
- [Features](#features)
- [Requirements](#requirements)
- [Install](#install)
- [Quick setup](#quick-setup)
- [Configuration](#configuration)
- [Submit feedback](#submit-feedback-html-form)
- [AI dashboard](#ai-dashboard)
- [SEO & branding templates](#seo--branding-templates)
- [Full documentation](#full-documentation)
- [Troubleshooting](#troubleshooting)
- [About the author](#about-the-author)
- [License](#license)

---

## Features

- **Generic** — works in any Django 4.2+ project; no host-app coupling
- **Authenticated or anonymous** submissions (`user`, `name`, `email`, `session_key`)
- **Star ratings** (1–5), **category**, **source** (page/route), `link_type` / `link_id`
- **Cooldown** per user or anonymous session (`FEEDBACK_COOLDOWN_DAYS`)
- **Django admin** — search, filters, list display
- **AI dashboard** (staff) — trends, ratings, sentiment, insight bullets, Chart.js
- **JSON API** — `/feedback/dashboard/api/` for external tools
- **Optional OpenAI** summaries (`[ai]` extra)
- **SEO-ready pages** — meta tags, Open Graph, JSON-LD (Schema.org), public license page

---

## Requirements

| Package | Version |
|---------|---------|
| Python | 3.10+ |
| Django | 4.2+ |

---

## Install

### From PyPI (recommended)

```bash
pip install nkscoder-django-feedback
```

### Via [nkscoder](https://pypi.org/project/nkscoder/) meta package

```bash
pip install "nkscoder[feedback]"
# or all @nkscoder Django packages:
pip install "nkscoder[all]"
```

### From GitHub

```bash
git clone https://github.com/nkscoder/feedback.git
cd feedback
pip install -e .
```

### Optional: OpenAI insight summaries

```bash
pip install "nkscoder-django-feedback[ai]"
```

---

## Quick setup

### 1. `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ...
    "feedback",
]
```

### 2. Context processor (SEO / branding on dashboard pages)

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                # ...
                "feedback.context_processors.feedback_open_source",
            ],
        },
    },
]
```

### 3. Migrations

```bash
python manage.py migrate feedback
```

### 4. URLs

```python
from django.urls import path, include

urlpatterns = [
    path("feedback/", include("feedback.urls")),
]
```

---

## Configuration

All settings use the `FEEDBACK_` prefix. Defaults are in `feedback/conf.py`.

| Setting | Default | Description |
|---------|---------|-------------|
| `FEEDBACK_COOLDOWN_DAYS` | `7` | Days between submissions (`0` = no limit) |
| `FEEDBACK_REQUIRE_AUTH` | `False` | Login required to submit |
| `FEEDBACK_REQUIRE_EMAIL` | `False` | Email required for guests |
| `FEEDBACK_MESSAGE_MAX_LENGTH` | `5000` | Max message length |
| `FEEDBACK_SUBMIT_REDIRECT` | `"/"` | Path or URL name after submit |
| `FEEDBACK_BASE_TEMPLATE` | `feedback/base.html` | Base template for dashboard |
| `FEEDBACK_LOGIN_URL` | `"login"` | Login URL for staff views |
| `FEEDBACK_DASHBOARD_DAYS` | `30` | Default analytics window |
| `FEEDBACK_OPENAI_API_KEY` | `""` | Optional LLM summaries |
| `FEEDBACK_AUTHOR_NAME` | `Nitesh Kumar Singh` | Template / SEO author |
| `FEEDBACK_AUTHOR_HANDLE` | `nkscoder` | Brand handle |
| `FEEDBACK_GITHUB_URL` | `https://github.com/nkscoder/feedback` | Repo link |
| `FEEDBACK_HOMEPAGE_URL` | `https://nkscoder.in` | Author site |
| `FEEDBACK_SEO_DESCRIPTION` | (see `conf.py`) | Meta description |
| `FEEDBACK_SEO_KEYWORDS` | (see `conf.py`) | Meta keywords |

Example:

```python
FEEDBACK_COOLDOWN_DAYS = 7
FEEDBACK_SUBMIT_REDIRECT = "home"
FEEDBACK_SEO_DESCRIPTION = (
    "Customer feedback for MyApp — powered by nkscoder-django-feedback "
    "by Nitesh Kumar Singh (nkscoder)."
)
```

---

## Submit feedback (HTML form)

![Example feedback form](https://raw.githubusercontent.com/nkscoder/feedback/main/docs/screenshots/feedback-form.png)

**Ready-made template** (Bootstrap 5):

```django
{% include "feedback/submit_form.html" %}
```

Minimal HTML:

```html
<form method="post" action="{% url 'feedback:submit_feedback' %}">
  {% csrf_token %}
  <textarea name="feedback" required placeholder="Your feedback…"></textarea>
  <input name="name" placeholder="Name">
  <input name="email" type="email" placeholder="Email">
  <select name="rating">
    <option value="">Rating</option>
    <option value="5">5 — Excellent</option>
    <option value="4">4</option>
  </select>
  <input name="category" placeholder="Bug / Feature / Praise">
  <button type="submit">Send feedback</button>
</form>
```

**Python helpers:**

```python
from feedback.services import is_feedback_allowed, create_feedback
from feedback.views import get_feedback_context

# Template context
context = {**get_feedback_context(request)}

# Programmatic
create_feedback(request, "Great UX!", category="praise", rating=5)
```

---

## AI dashboard

Staff-only analytics built by **Nitesh Kumar Singh (nkscoder)**.

![AI analytics dashboard](https://raw.githubusercontent.com/nkscoder/feedback/main/docs/screenshots/ai-dashboard.png)

| URL | Name | Access |
|-----|------|--------|
| `/feedback/dashboard/` | `feedback:ai_dashboard` | Staff |
| `/feedback/dashboard/api/?days=30` | `feedback:ai_dashboard_api` | Staff |
| `/feedback/license/` | `feedback:license` | Public (SEO) |

**Default insights:** rule-based (volume, ratings, sentiment keywords, categories).  
**With OpenAI:** `FEEDBACK_OPENAI_API_KEY` + `pip install "nkscoder-django-feedback[ai]"`.

---

## SEO & branding templates

Included for discoverability and attribution:

- `feedback/_seo_head.html` — description, keywords, author, Open Graph, Twitter Card, JSON-LD `SoftwareApplication`
- `feedback/_opensource_footer.html` — links to GitHub, PyPI, License, [nkscoder.in](https://nkscoder.in)
- `feedback/license.html` — public MIT license page

Override copy via `FEEDBACK_SEO_*` and `FEEDBACK_AUTHOR_*` settings.

---

## Full documentation

See **[DOCUMENTATION.md](DOCUMENTATION.md)** for:

- Data model reference
- Services API
- Analytics & AI insight logic
- Admin customization
- Publishing to PyPI

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Empty SEO meta on dashboard | Add `feedback.context_processors.feedback_open_source` |
| `TemplateSyntaxError` on `_seo_head.html` | Same — context processor required |
| Redirect after submit fails | Set `FEEDBACK_SUBMIT_REDIRECT` to a valid path or URL name |
| Guests submit too often | Lower `FEEDBACK_COOLDOWN_DAYS` or set `FEEDBACK_REQUIRE_AUTH` |
| No OpenAI insights | Install `[ai]` extra and set `FEEDBACK_OPENAI_API_KEY` |

---

## About the author

**Nitesh Kumar Singh (nkscoder)** builds reusable Django packages at **[nkscoder.in](https://nkscoder.in)** — including ticket systems, activity monitors, and this feedback plugin.

- **GitHub:** https://github.com/nkscoder  
- **PyPI:** https://pypi.org/user/nkscoder/  
- **LinkedIn:** https://www.linkedin.com/in/nitesh-kumar-singh-897437a2/

For integration help, custom dashboards, or enterprise extensions, visit [https://nkscoder.in](https://nkscoder.in).

---

## License

Copyright © 2020–2026 [Nitesh Kumar Singh (nkscoder)](https://nkscoder.in).

Released under the [MIT License](LICENSE). You may use, copy, modify, and distribute this software with attribution to **Nitesh Kumar Singh (nkscoder)**.

---

## Publish to PyPI

Maintainer: **nkscoder**. See **[PUBLISHING.md](PUBLISHING.md)**.

```bash
pip install build twine
python -m build
twine upload dist/*
```
