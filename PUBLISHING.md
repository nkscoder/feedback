# Publishing nkscoder-django-feedback to PyPI

**Package:** `nkscoder-django-feedback`  
**PyPI profile:** https://pypi.org/user/nkscoder/

---

## One-time setup

1. Create an API token: https://pypi.org/manage/account/token/  
   Scope: entire account (or project-scoped for `nkscoder-django-feedback`).

2. On GitHub repo **nkscoder/feedback** → Settings → Secrets → Actions → add:
   - `PYPI_API_TOKEN` = `pypi-...`

---

## Local publish

```bash
cd /path/to/feedback
python -m pip install --upgrade pip build twine

export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-xxxxxxxx   # your token

python -m build
twine upload dist/*
```

---

## GitHub Actions

1. Bump version in `pyproject.toml` and `feedback/__init__.py`.
2. Commit and push to `main`.
3. Create a GitHub **Release** (tag e.g. `v1.0.0`) — workflow publishes on `release: published`.
4. Or: Actions → **Publish to PyPI** → **Run workflow**.

---

## Verify

```bash
pip install nkscoder-django-feedback==1.0.0
pip show nkscoder-django-feedback
```

---

## Version checklist

- [ ] `pyproject.toml` → `[project].version`
- [ ] `feedback/__init__.py` → `__version__`
- [ ] `README.md` version table
- [ ] Git tag `vX.Y.Z`
- [ ] GitHub release notes
