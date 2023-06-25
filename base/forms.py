from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User
from django import forms


# class RoomForm(ModelForm):
#     class Meta:
#         model = Room
#         fields = '__all__'
#         exclude = ['host', 'participants']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

        
class UserForm(ModelForm):
    class Meta:
        model = User
        # fields = ['username', 'email']
        fields = ['avatar', 'name', 'username', 'email', 'bio']



class RoomForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    duration_minutes = forms.FloatField(required=False,min_value=0)
    distance = forms.FloatField(required=False, min_value=0)
    # location = forms.CharField(required=False, max_length=100)
    # days = forms.IntegerField(required=False, min_value=0)

    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']
