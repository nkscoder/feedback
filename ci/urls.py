from django.urls import include, path

urlpatterns = [
    path("feedback/", include("feedback.urls")),
]
