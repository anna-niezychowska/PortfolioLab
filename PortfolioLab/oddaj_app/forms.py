from django.contrib.auth.forms import UserChangeForm
from oddaj_app.models import User
from django import forms


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
