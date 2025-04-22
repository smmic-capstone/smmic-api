from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import *
from.serializers import *
from django.shortcuts import get_object_or_404
from typing import Any
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .tasks import *
import pusher
import json
from django.contrib.auth.tokens import default_token_generator
from djoser.serializers import PasswordResetConfirmSerializer

# Create your views here.
pusher_client = pusher.Pusher(
    app_id="1897218",
    key="d0f649dd91498f8916b8",
    secret = "0b36637c07e16532abc9",
    cluster = "ap3",
    ssl=True
)

#BlackList and Refresh Token
class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,) 
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT, data={"refresh_token":refresh_token, "blacklisted":True})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class PasswordResetConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    token_generator = default_token_generator
    

    def get(self, request, uid, token):
        print(request.data)
        """Render the password reset form with UID and token embedded in the form."""
        return render(request, 'email/reset_password_confirm.html', {'uid': uid, 'token': token})
#User Update Details
class UpdateUserDetailsView(APIView):
    permission_classes = (permissions.IsAuthenticated,) #Debug

    def put(self,request):
        data = request.data
        userID = request.headers.get('UID')

        if not userID:
            return Response({'error':'UID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.get(UID = userID)
        serializer = UpdateUserDetailsSerializer(user, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#Create


#Get All Devices on User
class GetUserSKDeviceView(APIView):
    permission_classes = (permissions.AllowAny,) #debug
    
    def get(self,request):
        userID = request.headers.get('UID')

        if not userID:
            return Response({'error':'UID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.get(UID = userID)

        userSKDevice = SinkNode.objects.filter(User = user).prefetch_related('sensor_nodes')
        serializer = GetUserSKDeviceSerializer(userSKDevice, many=True)

        return Response(serializer.data)
    
#Update Sink Node Name
class UpdateSKNameView(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def patch(self,request):
        data = request.data
        SK_ID = request.headers.get('Sink')

        if not SK_ID:
            return Response({'error':'Sink Node ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        sink_node = SinkNode.objects.get(device_id = SK_ID)
        serializer = UpdateSKDeviceSerializer(sink_node, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Update Sensor Node Name
class UpdateSNNameView(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def patch(self,request):
        data = request.data
        SN_ID = request.headers.get('Sensor')

        if not SN_ID:
            return Response({'error':'Sensor Node ID required'},status=status.HTTP_400_BAD_REQUEST)
        
        sensor_node = SensorNode.objects.get(device_id = SN_ID)
        serializer = UpdateSNDeviceSerializer(sensor_node, data = data)

        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#Get Only  One Reading Views
class GetSKReadingViews(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def get(self,request):
        sink_node_id = request.headers.get('Sink')

        print(f"Received SinkNode_ID: {request.headers.get('Sink')}")

        if not sink_node_id:
            return Response({'error':'Sink Node ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        sink_node = get_object_or_404(SinkNode,device_id = sink_node_id)
        readings = SKReadings.objects.filter(device_id = sink_node).order_by('-timestamp')[:1]

        serializer = GetSKReadingsSerializer(readings,many = True)
        return Response(serializer.data)

#Get 15 Latest Readings Views
class GetSNReadingView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        sensor_node_id = request.headers.get('Sensor')

        if not sensor_node_id:
            return Response({'error':'Sensor Node ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        sensor_node = get_object_or_404(SensorNode,device_id = sensor_node_id)
        readings = SMSensorReadings.objects.filter(device_id = sensor_node).order_by('-timestamp')[:1]

        serializer = GetSMReadingsSerializer(readings, many=True)
        return Response(serializer.data)

class GetSKReadingsViews(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def get(self,request):
        sink_node_id = request.headers.get('Sink')

        print(f"Received SinkNode_ID: {request.headers.get('Sink')}")

        if not sink_node_id:
            return Response({'error':'Sink Node ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        sink_node = get_object_or_404(SinkNode, device_id = sink_node_id)
        readings = SKReadings.objects.filter(device_id = sink_node).order_by('-timestamp')[:15]

        serializer = GetSKReadingsSerializer(readings,many = True)
        return Response(serializer.data)
    
class GetSMReadingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        sensor_node_id = request.headers.get('Sensor')

        if not sensor_node_id:
            return Response({'error':'Sensor Node ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        sensor_node = get_object_or_404(SensorNode, device_id = sensor_node_id)
        readings = SMSensorReadings.objects.filter(device_id = sensor_node).order_by('-timestamp')[:15]

        serializer = GetSMReadingsSerializer(readings, many=True)
        return Response(serializer.data)

class CreateSKReadingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self,request):
        data = request.data
        serializer = CreateSKReadingsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message = serializer.data

            if 'device_id' in  message:
                message['device_id'] = str(message['device_id'])

            pusher_client.trigger(
                channels= 'sink_readings',
                event_name= 'sink_reading_message',
                data = json.dumps({
                    'message' : message
                })
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "sink_readings",
                {
                    'type' : 'sink_reading_messages',
                    'message' : serializer.data 
                }
            )
            return Response({**serializer.data},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateSensorReadingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        sensor_type = request.data.get('sensor_type')
        data = request.data
        serializer : Any | None = None
        
        if sensor_type == 'soil_moisture':
            serializer = CreateSMReadingsSerializer(data = data)
        else:
            return Response(f'Unregistered sensor type: {request.data}', status=status.HTTP_400_BAD_REQUEST)
        
    
        if serializer:
            if serializer.is_valid():
                serializer.save()

                message = serializer.data
                if 'device_id' in  message:
                    message['device_id'] = str(message['device_id'])

                pusher_client.trigger(
                channels= 'sensor_readings',
                event_name= 'sensor_reading_message',
                data = json.dumps({
                    'message' : message
                    })
                )

                pusher_client.trigger(
                channels= 'user_commands',
                event_name= 'interval',
                data = {
                    'message' : 69,
                    "data" : {
                        'interval':15
                    }
                    
                    }
                )

                

                return Response({**serializer.data},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class SMSensorAlertsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        sensor_type = request.data.get('sensor_type')
        serializer : Any | None = None

        if sensor_type == 'soil_moisture':
            serializer = SMSensorAlertsSerializer(data = data)
        else:
            return Response(f'Unregistered sensor type: {request.data}', status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():

            serializer.save()

            device_id = serializer.data['device_id']
            alert_code = serializer.data['alert_code']

            if(alert_code == 42):
                soil_moisture = serializer.data['data']['soil_moisture']
                send_notifications(device_id=device_id, soil_moisture=soil_moisture)

            message = serializer.data
            if 'device_id' in  message:
                    message['device_id'] = str(message['device_id'])

            
            pusher_client.trigger(
                channels= 'sensor_alerts',
                event_name= 'sensor_alerts_message',
                data = json.dumps({
                    'message' : message
                })
            )

            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class PusherAuthentication(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self,request):
        socket_id = request.data['socket_id']
        channel_name = request.data['channel_name']

        print(socket_id)
        print(channel_name)

        try:
            auth  = pusher_client.authenticate(
            channel=channel_name,
            socket_id=socket_id)
            return Response(json.dumps(auth))
        except:
            return Response({"error" : "Invalid Request"},status=status.HTTP_400_BAD_REQUEST)

# get channel name, authorization token and socket id from frontend, and then return auth then what?
        

        
        
#kuha ug latest nga isa kabook
#kuha ug data from latest to 15th nga latest
#butang ug post data nila SK ug Sensor
        
#Testing for Raspi

class TestingforRaspiViews(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        user_id = request.headers.get('UID')

        print(user_id)

        if not user_id:
            return Response({'error':'User ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        user = CustomUser.objects.get(UID = user_id)
        serializer = TestingforRaspiSerializer(user)

        return Response(serializer.data)
    
class HealthCheck(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response({"status":"OK"}, status=status.HTTP_200_OK)
    

class GetAllSensorNoAuthView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        date = self.request.query_params.get('date')
        sensor_node_id = request.headers.get('Sensor')
        limit = int(request.query_params.get('limit',10))


        if not sensor_node_id:
            return Response({'error' : 'Sensor Node ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        sensor_node = get_object_or_404(SensorNode,device_id = sensor_node_id)
        readingsByDate = SMSensorReadings.objects.filter(device_id = sensor_node,timestamp__date = date).order_by('-timestamp')[:limit]

        serializer = GetSMReadingsNoAuthSerializer(readingsByDate, many=True)

        return Response(serializer.data)
    
        