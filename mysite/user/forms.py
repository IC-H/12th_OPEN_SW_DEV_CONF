import unicodedata
from django.conf import settings
from django import forms
from user.auth import Auth
from common.models import User
from django.contrib.auth.hashers import check_password


class EmailField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': "비밀번호가 일치하지 않습니다.",
    }
    password1 = forms.CharField(
        label = "비밀번호",
        strip = False,
        widget = forms.PasswordInput,
    )
    password2 = forms.CharField(
        label = "비밀번호 확인",
        widget = forms.PasswordInput,
        strip = False,
    )

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': EmailField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code = 'password_mismatch',
            )
        return password2

    def save(self, commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data["password1"])
        user.set_datetime()
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    email = EmailField(
        widget = forms.TextInput(attrs={'autofocus': True}), 
        label = "Email"
        )
    password = forms.CharField(
        label = "비밀번호",
        strip = False,
        widget = forms.PasswordInput,
        )
    error_messages = {
        'invalid_login': "이메일와 비밀번호를 다시 확인해 주십시오.",
    }

    def __init__(self, request = None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')   ### 이메일과 비밀번호를 받음

        if email is not None and password is not None:
            self.user_cache = Auth.authenticate(self.request, email = email, password = password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code = 'invalid_login',
                    )
            return self.cleaned_data

    def get_user(self):
        return self.user_cache