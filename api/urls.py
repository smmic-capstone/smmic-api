from django.urls import path,include
from . import views
from djoser import views as djoser_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path('djoser/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('updateuserdetails/<str:pk>',views.UpdateUserDetailsView.as_view(),name='updateuserdetails'),
    path('getuserSKdevices/<str:pk>',views.GetUserSKDeviceView.as_view(),name='userSKDevices'),
    path('updateuserSKdevicesname/<str:pk>',views.UpdateSKNameView.as_view(),name='updateSKname'),
    path('updateuserSNdevicesname/<str:pk>',views.UpdateSNNameView.as_view(),name='updateSNname'),
    path('getSKreadings/',views.GetSKReadingsViews.as_view(),name='getSKreadings'),
    path('getSNreadings/',views.GetSNReadingsView.as_view(),name='getSNreadings'),
    path('raspiTesting/',views.TestingforRaspiViews.as_view(),name='raspiTesting'),
    path('blacklist/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist')
]