from typing import Any
from django.contrib.auth.forms import (
    UserCreationForm,
    PasswordChangeForm as AuthPasswordChangeForm,
)
from django.forms import ValidationError
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password1(self) -> str:
        old_password = self.cleaned_data.get("old_password")
        new_password1 = self.cleaned_data.get("new_password1")
        if old_password == new_password1:
            raise ValidationError("same password")
        return new_password1


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "avatar",
            "first_name",
            "last_name",
            "website_url",
            "bio",
            "phone_number",
            "gender",
        ]


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
        ]
        model = User

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True

    def clean_email(self):
        data = self.cleaned_data.get("email")
        if data:
            qs = User.objects.filter(email=data)
            if qs.exists():
                raise ValidationError("already exists")
        return data


# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
