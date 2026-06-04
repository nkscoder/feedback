#!/usr/bin/env bash
# Set GitHub repo About: description, website, topics — nkscoder/feedback
# Requires: gh auth login (https://cli.github.com/)

set -euo pipefail

REPO="${GITHUB_REPOSITORY:-nkscoder/feedback}"

DESCRIPTION="Open-source Django feedback plugin by Nitesh Kumar Singh (nkscoder). Collect anonymous or authenticated user feedback with ratings, cooldown rules, and an AI analytics dashboard. Install: pip install nkscoder-django-feedback"

HOMEPAGE="https://pypi.org/project/nkscoder-django-feedback/"

TOPICS=(
  django
  feedback
  python
  nkscoder
  nitesh-kumar-singh
  open-source
  django-package
  user-feedback
  analytics
  ai-dashboard
  pypi
  sentiment-analysis
  survey
  django-plugin
  customer-feedback
  django-feedback
  nkscoder-django-feedback
)

if ! command -v gh >/dev/null 2>&1; then
  echo "Install GitHub CLI: brew install gh"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Run: gh auth login"
  exit 1
fi

echo "Updating About for $REPO ..."

CMD=(gh repo edit "$REPO" --description "$DESCRIPTION" --homepage "$HOMEPAGE")
for topic in "${TOPICS[@]}"; do
  CMD+=(--add-topic "$topic")
done

"${CMD[@]}"

echo "Done. Check: https://github.com/${REPO}"
