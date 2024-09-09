from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.response import Response
UserModel = get_user_model()

#User Serializers
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserModel
        fields=('UID','first_name','last_name','province','city','barangay','zone','zip_code','email','password')

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = UserModel
        fields = ('UID','first_name','last_name','province','city','barangay','zone','zip_code','email','password','profilepic')

class UpdateUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name','last_name','province','city','barangay','zone','zip_code', 'email','password','profilepic'] #temporary first_name only for testing purposes

#Get All Devices
class GetUserSNDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorNode
        fields = ["SNID","SensorNode_Name","latitude","longitude"]
        
class GetUserSKDeviceSerializer(serializers.ModelSerializer):
    sensor_nodes = GetUserSNDeviceSerializer(many=True,read_only=True)

    class Meta:
        model = SinkNode
        fields = ["SKID","SK_Name","sensor_nodes","latitude","longitude"]

#Update Device Name
class UpdateSKNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinkNode
        fields= ['SK_Name',"latitude","longitude"]

class UpdateSNNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorNode
        fields = ['SensorNode_Name',"latitude","longitude"]


#Readings
class GetSKReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKReadings
        fields = ['battery_level','timestamp',]

class GetSNReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNReadings
        fields = ['battery_level','timestamp','soil_moisture','temperature','humidity',]

class CreateSNReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNReadings
        fields =  '__all__'

class CreateSKReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKReadings
        fields = '__all__'

class TestingforRaspiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name',]



 
