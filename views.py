from django.shortcuts import redirect
from django.urls import reverse

from .conf import get_setting
from .services import create_feedback, is_feedback_allowed


def get_feedback_context(request):
    show_beta_popup = request.session.get("show_beta", True)
    request.session["show_beta"] = False

    return {
        "show_beta_popup": show_beta_popup,
        "feedback_allowed": is_feedback_allowed(request),
    }


def submit_feedback(request):
    if request.method == "POST":
        message = request.POST.get("feedback") or request.POST.get("message", "")
        if message.strip():
            create_feedback(
                request,
                message.strip(),
                name=request.POST.get("name", ""),
                email=request.POST.get("email", ""),
                rating=request.POST.get("rating") or None,
                category=request.POST.get("category", ""),
                link_type=request.POST.get("link_type", "generic"),
                link_id=request.POST.get("link_id", ""),
            )

    target = get_setting("SUBMIT_REDIRECT")
    if target.startswith("/"):
        return redirect(target)
    try:
        return redirect(reverse(target))
    except Exception:
        return redirect("/")
