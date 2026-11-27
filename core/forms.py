from django import forms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.password_validation import validate_password

from core.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        self.user = auth.authenticate(username=username, password=password)
        if self.user is None:
            raise forms.ValidationError("Invalid username or password.")
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 20:
            raise forms.ValidationError("Username must be less than 20 characters.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) > 50:
            raise forms.ValidationError("Password must be less than 50 characters.")
        return password


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    repeat_password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    nickname = forms.CharField(max_length=20)
    avatar = forms.ImageField(required=False)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise forms.ValidationError("Passwords do not match.")
        return self.cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) > 50:
            raise forms.ValidationError("Password must be less than 50 characters.")
        validate_password(password)
        return password


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        profile = Profile(user=user, nickname=self.cleaned_data['nickname'])
        if self.cleaned_data.get('avatar'):
            profile.avatar = self.cleaned_data['avatar']
        profile.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar']

