from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


class LoginForm(forms.Form):
    name = forms.CharField(label='User Name')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        name = data.get("name")
        password = data.get("password")
        user = User.objects.filter(username=name)
        if user.exists():
            user = authenticate(request, username=name, password=password)
        if user is None:
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        return data
