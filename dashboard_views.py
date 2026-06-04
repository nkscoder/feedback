import json

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .analytics import get_dashboard_context
from .conf import get_setting

staff_required = user_passes_test(lambda u: u.is_active and (u.is_staff or u.is_superuser))


def _login_required(view):
    return login_required(login_url=get_setting("LOGIN_URL"))(view)


@_login_required
@staff_required
def ai_dashboard(request):
    try:
        days = int(request.GET.get("days", get_setting("DASHBOARD_DAYS")))
    except (TypeError, ValueError):
        days = get_setting("DASHBOARD_DAYS")
    days = days if days in (7, 14, 30, 90, 365) else get_setting("DASHBOARD_DAYS")

    context = get_dashboard_context(days=days)
    context["base_template"] = get_setting("BASE_TEMPLATE")
    context["active_tab"] = "feedback_ai_dashboard"
    return render(request, "feedback/ai_dashboard.html", context)


@_login_required
@staff_required
@require_GET
def ai_dashboard_api(request):
    """JSON API for charts and insights (SPA or external tools)."""
    try:
        days = int(request.GET.get("days", get_setting("DASHBOARD_DAYS")))
    except (TypeError, ValueError):
        days = get_setting("DASHBOARD_DAYS")

    ctx = get_dashboard_context(days=days)
    return JsonResponse(
        {
            "stats": ctx["stats"],
            "ai_insights": ctx["ai_insights"],
            "ai_insights_source": ctx["ai_insights_source"],
            "charts": {
                "ratings": {
                    "labels": json.loads(ctx["rating_labels_json"]),
                    "values": json.loads(ctx["rating_values_json"]),
                },
                "categories": {
                    "labels": json.loads(ctx["category_labels_json"]),
                    "values": json.loads(ctx["category_values_json"]),
                },
                "sources": {
                    "labels": json.loads(ctx["source_labels_json"]),
                    "values": json.loads(ctx["source_values_json"]),
                },
                "trend": {
                    "labels": json.loads(ctx["trend_labels_json"]),
                    "values": json.loads(ctx["trend_values_json"]),
                },
                "sentiment": {
                    "labels": json.loads(ctx["sentiment_labels_json"]),
                    "values": json.loads(ctx["sentiment_values_json"]),
                },
            },
        }
    )
