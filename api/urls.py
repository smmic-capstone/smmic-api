from django.urls import path,include
from . import views
from djoser import views as djoser_views
from rest_framework_simplejwt.views import TokenRefreshView
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

urlpatterns = [
    path('djoser/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('updateuserdetails/',views.UpdateUserDetailsView.as_view(),name='updateuserdetails'),
    path('getuserSKdevices/',views.GetUserSKDeviceView.as_view(),name='userSKDevices'),
    path('updateuserSKdevicesname/',views.UpdateSKNameView.as_view(),name='updateSKname'),
    path('updateuserSNdevicesname/',views.UpdateSNNameView.as_view(),name='updateSNname'),
    path('getSKreading/',views.GetSKReadingViews.as_view(),name='getSKreadings'),
    path('getSNreading/',views.GetSNReadingView.as_view(),name='getSNreadings'),
    path('getSKreadings/',views.GetSKReadingsViews.as_view(),name='getSKreadings'),
    path('getSNreadings/',views.GetSMReadingsView.as_view(),name='getSNreadings'),
    path('createSensorReadings/',views.CreateSensorReadingsView.as_view(),name='createSNreadings'),
    path('createSKreadings/',views.CreateSKReadingsView.as_view(),name='createSKreadings'),
    path('raspiTesting/',views.TestingforRaspiViews.as_view(),name='raspiTesting'),
    path('SNAlerts/', views.SMSensorAlertsView.as_view(),name = 'SNalerts'),
    path('blacklist/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    path('health/', views.HealthCheck.as_view(), name='healthCheck'),

    path('devices/', FCMDeviceAuthorizedViewSet.as_view({'post':'create'}), name='create_fcm_device')
]