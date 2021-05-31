from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='index'),
    path('cameras', views.cameras, name='cameras'),
    path('alerts', views.alerts, name='alerts'),
    path('recordings', views.recordings, name='recordings')
]