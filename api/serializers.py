from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.response import Response
UserModel = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserModel
        fields=('UID','first_name','last_name','province','city','barangay','zone','zip_code','email','password')

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = ('UID','first_name','last_name','province','city','barangay','zone','zip_code','email','password','profilepic')
 
