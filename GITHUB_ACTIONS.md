# GitHub Actions — nkscoder-django-feedback

**Author:** [Nitesh Kumar Singh (nkscoder)](https://nkscoder.in)  
**Repository:** https://github.com/nkscoder/feedback

---

## Workflows

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **Django CI** | `.github/workflows/django.yml` | push, PR | Test on Python 3.10–3.12 + build wheel |
| **Python package** | `.github/workflows/python-package.yml` | push, PR | Matrix test + package build |
| **Pylint** | `.github/workflows/pylint.yml` | push, PR | Lint Python sources |
| **Publish Python Package** | `.github/workflows/publish-pypi.yml` | release, manual | Upload to PyPI |

These match GitHub’s suggested workflows for **Django**, **Python application**, **Pylint**, and **Publish Python Package**.

> **Not used:** Jekyll (static site only) and Anaconda (this package uses pip/PyPI like your other `@nkscoder` Django apps).

---

## One-time setup

### 1. Enable Actions

GitHub → **Actions** → enable workflows for this repo.

### 2. PyPI secret (for publish workflow)

1. Create token: https://pypi.org/manage/account/token/
2. GitHub → **Settings** → **Secrets and variables** → **Actions**
3. New secret: `PYPI_API_TOKEN` = `pypi-...`

### 3. Optional: PyPI environment

For `publish-pypi.yml` environment protection:

- **Settings** → **Environments** → **pypi** → add required reviewers (optional)

---

## Run manually

**Actions** tab → pick workflow → **Run workflow** → branch `main`.

---

## Local same as CI

```bash
pip install -e ".[dev]"
python ci/manage.py migrate --run-syncdb
python ci/manage.py test feedback.tests
python -m build
pylint models.py views.py services.py analytics.py  # see pylint.yml
```

---

## Badges (README)

```markdown
![Django CI](https://github.com/nkscoder/feedback/actions/workflows/django.yml/badge.svg)
![Python package](https://github.com/nkscoder/feedback/actions/workflows/python-package.yml/badge.svg)
![Pylint](https://github.com/nkscoder/feedback/actions/workflows/pylint.yml/badge.svg)
```

---

MIT · Nitesh Kumar Singh (nkscoder)
