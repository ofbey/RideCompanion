from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField
from base.models import Room
from django.contrib.auth.models import User

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

