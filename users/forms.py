# users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  # Thêm trường email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# users/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    pass
