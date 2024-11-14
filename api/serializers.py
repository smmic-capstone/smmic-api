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
        fields = ["device_id","name","latitude","longitude"]
        
class GetUserSKDeviceSerializer(serializers.ModelSerializer):
    sensor_nodes = GetUserSNDeviceSerializer(many=True,read_only=True)

    class Meta:
        model = SinkNode
        fields = ["device_id","name","sensor_nodes","latitude","longitude"]


#Update Device Details
class UpdateSKDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinkNode
        fields= ["name","User","latitude","longitude"]

class UpdateSNDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorNode
        fields = ["name","sink_node","latitude","longitude"]


#Readings
class GetSKReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKReadings
        fields = ['battery_level','timestamp', 'connected_clients', 'total_clients', 'sub_count', 'bytes_sent', 'bytes_received', 'messages_sent', 'messages_received']

class GetSMReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSensorReadings
        fields = ['battery_level','timestamp','soil_moisture','temperature','humidity',]

class CreateSMReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSensorReadings
        fields =  '__all__'

class CreateSKReadingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKReadings
        fields = ['device_id', 'battery_level','timestamp', 'connected_clients', 'total_clients', 'sub_count', 'bytes_sent', 'bytes_received', 'messages_sent', 'messages_received']

class SMSensorAlertsSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()
    class Meta:
        model = SMSensorAlerts
        fields = ['device_id','timestamp','alert_code','data']
        
class TestingforRaspiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['first_name',]





 
