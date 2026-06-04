"""Feedback analytics and AI-style insight generation (no external API required)."""

import json
import re
from collections import Counter
from datetime import timedelta

from django.db.models import Avg, Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from .models import Feedback

_POSITIVE = {
    "good", "great", "excellent", "love", "helpful", "fast", "easy", "thanks",
    "thank", "awesome", "amazing", "perfect", "nice", "happy", "satisfied",
}
_NEGATIVE = {
    "bad", "slow", "broken", "bug", "error", "issue", "problem", "hate",
    "terrible", "awful", "difficult", "confusing", "frustrated", "disappointed",
    "poor", "worst", "fail", "failed",
}
_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of",
    "is", "it", "this", "that", "with", "was", "are", "be", "have", "has", "had",
    "i", "we", "you", "my", "our", "your", "not", "no", "so", "as", "from",
}


def _period_qs(days=None):
    qs = Feedback.objects.all()
    if days:
        qs = qs.filter(submitted_at__gte=timezone.now() - timedelta(days=days))
    return qs


def _sentiment_label(text):
    words = set(re.findall(r"[a-z']+", (text or "").lower()))
    pos = len(words & _POSITIVE)
    neg = len(words & _NEGATIVE)
    if pos > neg:
        return "positive"
    if neg > pos:
        return "negative"
    return "neutral"


def _top_keywords(messages, limit=12):
    tokens = []
    for msg in messages:
        for word in re.findall(r"[a-z]{3,}", (msg or "").lower()):
            if word not in _STOPWORDS:
                tokens.append(word)
    return Counter(tokens).most_common(limit)


def _pct_change(current, previous):
    if not previous:
        return 100.0 if current else 0.0
    return round(((current - previous) / previous) * 100, 1)


def build_ai_insights(stats):
    """Rule-based insight bullets (works offline; optional OpenAI in ai_summary)."""
    insights = []

    total = stats["total_count"]
    if total == 0:
        return ["No feedback submitted yet. Encourage users with an in-app prompt or email survey."]

    week = stats["last_7_days"]
    prev_week = stats["prev_7_days"]
    change = _pct_change(week, prev_week)
    if change > 10:
        insights.append(f"Feedback volume is up {change}% vs the previous 7 days ({week} submissions).")
    elif change < -10:
        insights.append(f"Feedback volume dropped {abs(change)}% vs the previous 7 days — check for UX friction.")
    else:
        insights.append(f"Feedback volume is stable ({week} submissions in the last 7 days).")

    avg = stats["avg_rating"]
    if avg:
        if avg >= 4:
            insights.append(f"Average rating is strong ({avg}/5). Highlight positive themes in release notes.")
        elif avg <= 2.5:
            insights.append(f"Average rating is low ({avg}/5). Prioritize top negative categories and sources.")
        else:
            insights.append(f"Average rating is moderate ({avg}/5). Focus on recurring complaints in messages.")

    sent = stats["sentiment_counts"]
    dominant = max(sent, key=sent.get) if sent else "neutral"
    if sent.get("negative", 0) > sent.get("positive", 0):
        insights.append("Sentiment skews negative — review recent messages and assign owners by category.")
    elif dominant == "positive":
        insights.append("Sentiment is mostly positive — consider showcasing testimonials from top-rated feedback.")

    if stats["anonymous_count"] > stats["authenticated_count"]:
        insights.append("Most feedback is anonymous — ensure name/email fields are visible if you need follow-up.")

    top_cat = stats["top_categories"]
    if top_cat:
        insights.append(f"Top category: «{top_cat[0][0]}» ({top_cat[0][1]} items). Triage this area first.")

    top_src = stats["top_sources"]
    if top_src and top_src[0][0]:
        insights.append(f"Most feedback comes from «{top_src[0][0]}» — optimize that page or flow.")

    keywords = stats["top_keywords"]
    if keywords:
        terms = ", ".join(w for w, _ in keywords[:5])
        insights.append(f"Frequent terms in messages: {terms}.")

    return insights[:8]


def try_openai_summary(insights, stats):
    """Optional LLM summary when FEEDBACK_OPENAI_API_KEY is set."""
    from .conf import get_setting

    api_key = get_setting("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except ImportError:
        return None

    prompt = (
        "Summarize this Django app feedback dashboard in 3 short bullet points for a product manager.\n"
        f"Stats: {json.dumps({k: v for k, v in stats.items() if k != 'recent_feedback'})}\n"
        f"Insights: {insights}"
    )
    try:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=get_setting("OPENAI_MODEL"),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
        )
        text = (resp.choices[0].message.content or "").strip()
        return [line.lstrip("-• ").strip() for line in text.split("\n") if line.strip()][:5]
    except Exception:
        return None


def get_dashboard_context(days=30):
    now = timezone.now()
    qs = _period_qs(days)
    all_time = Feedback.objects.count()

    last_7 = _period_qs(7).count()
    prev_7 = Feedback.objects.filter(
        submitted_at__gte=now - timedelta(days=14),
        submitted_at__lt=now - timedelta(days=7),
    ).count()

    avg_rating = qs.filter(rating__isnull=False).aggregate(v=Avg("rating"))["v"]
    avg_rating = round(avg_rating, 2) if avg_rating is not None else None

    rating_rows = (
        qs.filter(rating__isnull=False)
        .values("rating")
        .annotate(c=Count("id"))
        .order_by("rating")
    )
    rating_labels = [str(r["rating"]) for r in rating_rows]
    rating_values = [r["c"] for r in rating_rows]

    category_rows = (
        qs.exclude(category="")
        .values("category")
        .annotate(c=Count("id"))
        .order_by("-c")[:10]
    )
    category_labels = [r["category"] or "Uncategorized" for r in category_rows]
    category_values = [r["c"] for r in category_rows]

    source_rows = (
        qs.exclude(source="")
        .values("source")
        .annotate(c=Count("id"))
        .order_by("-c")[:10]
    )
    source_labels = [r["source"] for r in source_rows]
    source_values = [r["c"] for r in source_rows]

    daily_rows = (
        qs.filter(submitted_at__gte=now - timedelta(days=min(days, 14)))
        .annotate(day=TruncDate("submitted_at"))
        .values("day")
        .annotate(c=Count("id"))
        .order_by("day")
    )
    trend_labels = [str(r["day"]) for r in daily_rows]
    trend_values = [r["c"] for r in daily_rows]

    messages = list(qs.order_by("-submitted_at").values_list("message", flat=True)[:200])
    sentiment_counts = Counter(_sentiment_label(m) for m in messages)

    stats = {
        "total_count": all_time,
        "period_count": qs.count(),
        "last_7_days": last_7,
        "prev_7_days": prev_7,
        "avg_rating": avg_rating,
        "authenticated_count": qs.filter(user__isnull=False).count(),
        "anonymous_count": qs.filter(user__isnull=True).count(),
        "sentiment_counts": dict(sentiment_counts),
        "top_categories": [(r["category"], r["c"]) for r in category_rows[:5]],
        "top_sources": [(r["source"], r["c"]) for r in source_rows[:5]],
        "top_keywords": _top_keywords(messages),
    }

    rule_insights = build_ai_insights(stats)
    llm_insights = try_openai_summary(rule_insights, stats)

    return {
        "stats": stats,
        "ai_insights": llm_insights or rule_insights,
        "ai_insights_source": "openai" if llm_insights else "rules",
        "rating_labels_json": json.dumps(rating_labels),
        "rating_values_json": json.dumps(rating_values),
        "category_labels_json": json.dumps(category_labels),
        "category_values_json": json.dumps(category_values),
        "source_labels_json": json.dumps(source_labels),
        "source_values_json": json.dumps(source_values),
        "trend_labels_json": json.dumps(trend_labels),
        "trend_values_json": json.dumps(trend_values),
        "sentiment_labels_json": json.dumps(list(sentiment_counts.keys())),
        "sentiment_values_json": json.dumps(list(sentiment_counts.values())),
        "recent_feedback": qs.select_related("user").order_by("-submitted_at")[:25],
        "period_days": days,
    }
