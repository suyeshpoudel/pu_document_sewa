from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from colleges.models import College

from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "phone",
            "college",
            "symbol_no",
            "reg_no",
            "citizenship_no",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")
        self.fields["name"].label = "Full name"
        self.fields["email"].label = "Email address"
        self.fields["phone"].label = "Phone number"
        self.fields["symbol_no"].label = "Symbol number"
        self.fields["reg_no"].label = "Registration number"
        self.fields["citizenship_no"].label = "Citizenship number"
        self.fields["name"].widget.attrs.setdefault("placeholder", "Your full name")
        self.fields["email"].widget.attrs.setdefault("placeholder", "you@example.com")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "98XXXXXXXX")
        self.fields["email"].widget.attrs.setdefault("autocomplete", "email")
        self.fields["phone"].widget.attrs.setdefault("autocomplete", "tel")
        self.fields["password1"].widget.attrs.setdefault("autocomplete", "new-password")
        self.fields["password2"].widget.attrs.setdefault("autocomplete", "new-password")
        self.fields["college"].queryset = College.objects.all()
        self.fields["college"].required = False
        self.fields["college"].empty_label = "— Select college (optional) —"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")
        self.fields["username"].label = "Email address"
        self.fields["username"].widget.attrs.update(
            {"placeholder": "you@example.com", "autocomplete": "email", "autofocus": True}
        )
        self.fields["password"].widget.attrs.setdefault("autocomplete", "current-password")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "phone", "college", "symbol_no", "reg_no", "citizenship_no"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "input")
        self.fields["name"].label = "Full name"
        self.fields["phone"].label = "Phone number"
        self.fields["symbol_no"].label = "Symbol number"
        self.fields["reg_no"].label = "Registration number"
        self.fields["citizenship_no"].label = "Citizenship number"
        self.fields["name"].widget.attrs.setdefault("placeholder", "Your full name")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "98XXXXXXXX")
        self.fields["phone"].widget.attrs.setdefault("autocomplete", "tel")
        self.fields["college"].queryset = College.objects.all()
        self.fields["college"].required = False
        self.fields["college"].empty_label = "— Select college (optional) —"
