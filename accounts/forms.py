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
            field.widget.attrs.setdefault(
                "class",
                "w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
            )
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
            field.widget.attrs.setdefault(
                "class",
                "w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
            )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "phone", "college", "symbol_no", "reg_no", "citizenship_no"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault(
                "class",
                "w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500",
            )
        self.fields["college"].queryset = College.objects.all()
        self.fields["college"].required = False
        self.fields["college"].empty_label = "— Select college (optional) —"
