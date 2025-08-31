from typing import Any
from django import forms

from django.contrib.auth import get_user_model
from .models import Room, Movie


User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self) -> dict[str, Any]:

        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', 'Пароли не совпадают')
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', 'password']  # ДОБАВИТЬ MOVIE_ID

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)


class RoomFilterForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Поиск по названию'}), required=False)
