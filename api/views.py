from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import *
from.serializers import *
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
    permission_classes = (permissions.AllowAny,)

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
    permission_classes = (permissions.AllowAny,)

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
    permission_classes = (permissions.AllowAny,)

    def patch(self,request,pk):
        data = request.data
        SN_ID = SensorNode.objects.get(SNID = pk)
        serializer = UpdateSNNameSerializer(instance = SN_ID, data = data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


        
