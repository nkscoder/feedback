# Publishing nkscoder-django-feedback to PyPI

**Maintainer:** [Nitesh Kumar Singh (nkscoder)](https://nkscoder.in)  
**Package:** `nkscoder-django-feedback`  
**PyPI profile:** https://pypi.org/user/nkscoder/  
**GitHub:** https://github.com/nkscoder/feedback

---

## One-time setup

1. Create an API token: https://pypi.org/manage/account/token/  
   Scope: entire account or project `nkscoder-django-feedback`.

2. On GitHub **nkscoder/feedback** → Settings → Secrets → Actions → add:
   - `PYPI_API_TOKEN` = `pypi-...`

---

## Local publish

```bash
cd /path/to/feedback
python -m pip install --upgrade pip build twine

export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxxxxxxx   # your token

python -m build
twine upload --non-interactive dist/*
```

---

## GitHub Actions

1. Bump version in `pyproject.toml` and `feedback/__init__.py` (currently **1.0.1**).
2. Commit and push to `main`.
3. Create a GitHub **Release** (tag e.g. `v1.0.1`) — workflow publishes on `release: published`.
4. Or: Actions → **Publish Python Package** → **Run workflow**.

---

## Verify

```bash
pip install nkscoder-django-feedback==1.0.1
pip show nkscoder-django-feedback
```

Check PyPI page title and description mention **Nitesh Kumar Singh** and **nkscoder**.

---

## Version checklist

- [ ] `pyproject.toml` → `[project].version`
- [ ] `feedback/__init__.py` → `__version__`
- [ ] `README.md` version table
- [ ] `DOCUMENTATION.md` if version cited
- [ ] Git tag `vX.Y.Z`
- [ ] GitHub release notes (author: nkscoder)
