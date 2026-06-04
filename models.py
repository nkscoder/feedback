from django.conf import settings
from django.db import models


class Feedback(models.Model):
    """Generic feedback entry — authenticated or anonymous."""

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedback_entries",
    )
    name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        null=True,
        blank=True,
    )
    category = models.CharField(max_length=64, blank=True)
    source = models.CharField(
        max_length=255,
        blank=True,
        help_text="Page, feature, or route where feedback was submitted.",
    )
    link_type = models.CharField(max_length=64, blank=True, default="generic", db_index=True)
    link_id = models.CharField(max_length=255, blank=True, db_index=True)
    extra_data = models.JSONField(null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, db_index=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "feedback"
        verbose_name_plural = "feedback"

    def __str__(self):
        return f"Feedback from {self.submitter_display}"

    @property
    def submitter_display(self):
        if self.user_id:
            return str(self.user)
        if self.name:
            return self.name
        if self.email:
            return self.email
        return "Anonymous"
