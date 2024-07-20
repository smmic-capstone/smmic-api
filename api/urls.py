from django.urls import path,include
from . import views
from djoser import views as djoser_views

urlpatterns =[
    path('djoser/',include('djoser.urls')),
    path('auth/',include('djoser.urls.jwt')),
]