from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from accounts.models import User
# from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['email', 'first_name', 'last_name', 'username', ]
        model = User

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_email(self):
        data = self.cleaned_data.get("email")
        if data:
            qs = User.objects.filter(email=data)
            if qs.exists():
                raise ValidationError('already exists')
        return data


# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
