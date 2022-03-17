from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    #sutvarkyt failu kelima
    img = serializers.FileField(source='', read_only = True)

    class Meta:
        model = Image
        fields = '__all__'