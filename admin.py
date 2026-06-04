from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "submitter_display",
        "category",
        "rating",
        "content_short",
        "source",
        "link_type",
        "submitted_at",
    )
    search_fields = ("name", "email", "message", "category", "source", "user__username")
    list_filter = ("category", "rating", "link_type", "submitted_at")
    readonly_fields = ("submitted_at",)
    ordering = ("-submitted_at",)

    def content_short(self, obj):
        if len(obj.message) > 50:
            return obj.message[:50] + "..."
        return obj.message

    content_short.short_description = "Message"
