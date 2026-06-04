from django.urls import path

from . import dashboard_views
from .views import submit_feedback

app_name = "feedback"

urlpatterns = [
    path("submit/", submit_feedback, name="submit_feedback"),
    path("dashboard/", dashboard_views.ai_dashboard, name="ai_dashboard"),
    path("dashboard/api/", dashboard_views.ai_dashboard_api, name="ai_dashboard_api"),
]
