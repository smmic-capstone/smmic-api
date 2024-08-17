from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import *
from.serializers import *
from django.shortcuts import get_object_or_404
# Create your views here.

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

#User Update Details
class UpdateUserDetailsView(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def put(self,request,pk):
        data = request.data
        userID = CustomUser.objects.get(UID = pk)
        serializer = UpdateUserDetailsSerializer(instance = userID, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#Get All Devices on User
class GetUserSKDeviceView(APIView):
    permission_classes = (permissions.AllowAny,) #debug
    
    def get(self,request,pk):
        userID = CustomUser.objects.get(UID = pk)
        userSKDevice = SinkNode.objects.filter(User = userID).prefetch_related('sensor_nodes')
        serializer = GetUserSKDeviceSerializer(userSKDevice, many=True)
        return Response(serializer.data)
    
#Update Sink Node Name
class UpdateSKNameView(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def patch(self,request,pk):
        data = request.data
        SK_ID = SinkNode.objects.get(SKID = pk)
        serializer = UpdateSKNameSerializer(instance = SK_ID, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Update Sensor Node Name
class UpdateSNNameView(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def patch(self,request,pk):
        data = request.data
        SN_ID = SensorNode.objects.get(SNID = pk)
        serializer = UpdateSNNameSerializer(instance = SN_ID, data = data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
#Readings Views
class GetSKReadingsViews(APIView):
    permission_classes = (permissions.AllowAny,) #Debug

    def get(self,request):
        sink_node_id = request.headers.get('Sink')

        print(f"Received SinkNode_ID: {request.headers.get('Sink')}")

        if not sink_node_id:
            return Response({'error':'Sink Node ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        sink_node = get_object_or_404(SinkNode,SKID = sink_node_id)
        readings = SKReadings.objects.filter(Sink_Node = sink_node).order_by('-timestamp')

        serializer = GetSKReadingsSerializer(readings,many = True)
        return Response(serializer.data)
    
class GetSNReadingsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self,request):
        sensor_node_id = request.headers.get('Sensor')

        if not sensor_node_id:
            return Response({'error':'Sensor Node ID is required'},status=status.HTTP_400_BAD_REQUEST)
        
        sensor_node = get_object_or_404(SensorNode,SNID = sensor_node_id)
        readings = SNReadings.objects.filter(Sensor_Node = sensor_node).order_by('-timestamp')

        serializer = GetSNReadingsSerializer(readings, many=True)
        return Response(serializer.data)


        
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
        