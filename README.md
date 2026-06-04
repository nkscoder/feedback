# nkscoder-django-feedback

**Author:** [Nitesh Kumar Singh (nkscoder)](https://nkscoder.in)

Generic, open-source Django feedback app for **any Django project** — authenticated or anonymous users, cooldown rules, and an **AI analytics dashboard** (rule-based insights + optional OpenAI summaries).

| | |
|---|---|
| **PyPI package** | `nkscoder-django-feedback` |
| **Django app** | `feedback` |
| **Version** | 1.0.0 |
| **License** | MIT |
| **Repository** | https://github.com/nkscoder/feedback |

---

## Features

- Submit feedback as logged-in users or guests (name / email)
- Configurable cooldown (`FEEDBACK_COOLDOWN_DAYS`)
- Star ratings (1–5), categories, page source, generic `link_type` / `link_id`
- Django admin list & search
- **AI dashboard** (`/feedback/dashboard/`) — charts, sentiment, trend, auto-generated insights
- JSON API for dashboards (`/feedback/dashboard/api/`)
- Optional OpenAI summaries (`pip install nkscoder-django-feedback[ai]`)

---

## Requirements

| Package | Version |
|---------|---------|
| Python | 3.10+ |
| Django | 4.2+ |

---

## Install

### From PyPI

```bash
pip install nkscoder-django-feedback
```

### From GitHub

```bash
git clone https://github.com/nkscoder/feedback.git
cd feedback
pip install -e .
```

### Optional: OpenAI summaries

```bash
pip install "nkscoder-django-feedback[ai]"
```

---

## Quick setup

### 1. Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    # ...
    "feedback",
]
```

### 2. Run migrations

```bash
python manage.py migrate feedback
```

### 3. Include URLs

```python
# project/urls.py
from django.urls import path, include

urlpatterns = [
    # ...
    path("feedback/", include("feedback.urls")),
]
```

### 4. Settings (optional)

```python
# Cooldown & submission
FEEDBACK_COOLDOWN_DAYS = 7          # 0 = no limit
FEEDBACK_REQUIRE_AUTH = False
FEEDBACK_REQUIRE_EMAIL = False
FEEDBACK_MESSAGE_MAX_LENGTH = 5000
FEEDBACK_SUBMIT_REDIRECT = "/"      # or URL name e.g. "home"

# AI dashboard
FEEDBACK_BASE_TEMPLATE = "feedback/base.html"
FEEDBACK_LOGIN_URL = "login"
FEEDBACK_DASHBOARD_DAYS = 30

# Optional OpenAI (needs [ai] extra)
FEEDBACK_OPENAI_API_KEY = ""        # or env var via django-environ
FEEDBACK_OPENAI_MODEL = "gpt-4o-mini"
```

---

## Submit feedback (HTML form)

```html
<form method="post" action="{% url 'feedback:submit_feedback' %}">
  {% csrf_token %}
  <textarea name="feedback" required></textarea>
  <input name="name" placeholder="Name">
  <input name="email" type="email" placeholder="Email">
  <select name="rating">
    <option value="">Rating</option>
    <option value="5">5</option>
    <option value="4">4</option>
  </select>
  <input name="category" placeholder="Bug / Feature / Other">
  <button type="submit">Send feedback</button>
</form>
```

In views/templates, expose whether submission is allowed:

```python
from feedback.services import is_feedback_allowed

def my_view(request):
    return render(request, "page.html", {
        "feedback_allowed": is_feedback_allowed(request),
    })
```

Or use the bundled helper:

```python
from feedback.views import get_feedback_context

context = {**get_feedback_context(request)}
```

Programmatic create:

```python
from feedback.services import create_feedback

create_feedback(request, "Love the new UI!", category="praise", rating=5)
```

---

## AI dashboard

Staff-only page with Chart.js analytics and insight bullets.

| URL | Name |
|-----|------|
| `/feedback/dashboard/` | `feedback:ai_dashboard` |
| `/feedback/dashboard/api/?days=30` | `feedback:ai_dashboard_api` |

**Insights (default):** rule-based analysis — volume trends, ratings, sentiment keywords, top categories/sources.

**With OpenAI:** set `FEEDBACK_OPENAI_API_KEY` and install `[ai]` extra for LLM-written summary bullets.

---

## Project layout

```
feedback/
├── __init__.py          # version
├── models.py
├── services.py
├── analytics.py         # AI insights & chart data
├── dashboard_views.py
├── conf.py
├── urls.py
├── templates/feedback/
│   ├── base.html
│   └── ai_dashboard.html
├── migrations/
├── pyproject.toml
└── README.md
```

---

## Publish to PyPI

See **[PUBLISHING.md](PUBLISHING.md)**.

```bash
pip install build twine
python -m build
twine upload dist/*
```

GitHub Actions workflow: `.github/workflows/publish.yml` (secret `PYPI_API_TOKEN`).

---

## Links

- **PyPI:** https://pypi.org/project/nkscoder-django-feedback/
- **Author:** https://nkscoder.in
- **GitHub:** https://github.com/nkscoder

---

## License

MIT — see [LICENSE](LICENSE).
