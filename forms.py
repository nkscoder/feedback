from django import forms

from .conf import get_setting
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "message", "rating", "category"]
        widgets = {
            "message": forms.Textarea(
                attrs={
                    "placeholder": "Enter your feedback...",
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "rating": forms.Select(attrs={"class": "form-select"}),
            "category": forms.TextInput(attrs={"class": "form-control", "placeholder": "Category (optional)"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        max_len = get_setting("MESSAGE_MAX_LENGTH")
        self.fields["message"].max_length = max_len

        if user and user.is_authenticated:
            self.fields["name"].required = False
            self.fields["email"].required = False
        elif get_setting("REQUIRE_EMAIL"):
            self.fields["email"].required = True

    def clean_message(self):
        message = self.cleaned_data["message"]
        max_len = get_setting("MESSAGE_MAX_LENGTH")
        if len(message) > max_len:
            raise forms.ValidationError(f"Message must be at most {max_len} characters.")
        return message
