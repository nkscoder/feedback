from datetime import timedelta

from django.utils import timezone

from .conf import get_setting
from .models import Feedback


def _cooldown_delta():
    days = get_setting("COOLDOWN_DAYS")
    if not days:
        return None
    return timedelta(days=days)


def _submitter_filter(request):
    if request.user.is_authenticated:
        return {"user": request.user}
    if not request.session.session_key:
        request.session.create()
    return {"session_key": request.session.session_key, "user__isnull": True}


def get_last_feedback(request):
    return Feedback.objects.filter(**_submitter_filter(request)).order_by("-submitted_at").first()


def is_feedback_allowed(request):
    if get_setting("REQUIRE_AUTH") and not request.user.is_authenticated:
        return False

    cooldown = _cooldown_delta()
    if not cooldown:
        return True

    last = get_last_feedback(request)
    if not last:
        return True
    return timezone.now() - last.submitted_at >= cooldown


def build_feedback_kwargs(request, message, **extra):
    kwargs = {
        "message": message,
        "source": extra.pop("source", "") or request.path,
        "category": extra.pop("category", ""),
        "rating": extra.pop("rating", None),
        "link_type": extra.pop("link_type", "generic"),
        "link_id": extra.pop("link_id", ""),
        "extra_data": extra.pop("extra_data", None),
    }

    if request.user.is_authenticated:
        kwargs["user"] = request.user
        kwargs["name"] = extra.pop("name", "") or getattr(request.user, "get_full_name", lambda: "")() or ""
        kwargs["email"] = extra.pop("email", "") or getattr(request.user, "email", "") or ""
    else:
        kwargs["name"] = extra.pop("name", "")
        kwargs["email"] = extra.pop("email", "")
        if not request.session.session_key:
            request.session.create()
        kwargs["session_key"] = request.session.session_key

    kwargs.update(extra)
    return kwargs


def _parse_rating(value):
    if value in (None, ""):
        return None
    try:
        rating = int(value)
    except (TypeError, ValueError):
        return None
    return rating if 1 <= rating <= 5 else None


def create_feedback(request, message, **extra):
    if get_setting("REQUIRE_EMAIL") and not request.user.is_authenticated:
        if not extra.get("email"):
            return None

    if not is_feedback_allowed(request):
        return None

    extra["rating"] = _parse_rating(extra.get("rating"))
    return Feedback.objects.create(**build_feedback_kwargs(request, message, **extra))
