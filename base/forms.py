from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room, User
from django import forms


# class RoomForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = '__all__'
#         exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        # fields = ['avatar', 'name', 'username', 'email', 'bio']



class RoomForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    duration_minutes = forms.FloatField(min_value=0)
    distance = forms.FloatField(required=False, min_value=0)

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
