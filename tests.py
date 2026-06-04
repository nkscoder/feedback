from datetime import timedelta
from unittest.mock import MagicMock

from django.contrib.sessions.backends.db import SessionStore
from django.test import RequestFactory, TestCase
from django.utils import timezone

from feedback.analytics import build_ai_insights, get_dashboard_context
from feedback.models import Feedback
from feedback.services import is_feedback_allowed


class FeedbackModelTests(TestCase):
    def test_submitter_display_anonymous(self):
        fb = Feedback(message="Hello")
        self.assertEqual(fb.submitter_display, "Anonymous")

    def test_submitter_display_name(self):
        fb = Feedback(name="Ada", message="Hi")
        self.assertEqual(fb.submitter_display, "Ada")


class AnalyticsTests(TestCase):
    def test_build_ai_insights_empty(self):
        insights = build_ai_insights({"total_count": 0})
        self.assertTrue(insights)
        self.assertIn("No feedback", insights[0])

    def test_dashboard_context_with_data(self):
        Feedback.objects.create(message="great app love it", rating=5, category="ui")
        ctx = get_dashboard_context(days=30)
        self.assertEqual(ctx["stats"]["total_count"], 1)
        self.assertTrue(ctx["ai_insights"])


class ServicesTests(TestCase):
    def _anonymous_request(self, session_key="abc123"):
        request = RequestFactory().get("/")
        request.user = MagicMock(is_authenticated=False)
        session = SessionStore(session_key=session_key)
        if not session.session_key:
            session.create()
        request.session = session
        return request

    def test_feedback_allowed_no_cooldown_when_no_prior(self):
        request = self._anonymous_request()
        self.assertTrue(is_feedback_allowed(request))

    def test_feedback_blocked_within_cooldown(self):
        request = self._anonymous_request()
        session_key = request.session.session_key

        Feedback.objects.create(
            message="first",
            session_key=session_key,
            submitted_at=timezone.now() - timedelta(days=1),
        )
        self.assertFalse(is_feedback_allowed(request))
