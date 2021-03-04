from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from news.models import News, Comment


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    city = forms.CharField(max_length=40, required=False, help_text='Город')
    phone = forms.CharField(max_length=20, required=False, help_text='Номер телефона')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'city', 'phone', 'password1', 'password2')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['news']
