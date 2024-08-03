from django.urls import path,include
from . import views
from djoser import views as djoser_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns =[
    path('djoser/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('blacklist/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist')
]