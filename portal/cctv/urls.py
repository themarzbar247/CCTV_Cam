from django.urls import path
from . import views

urlpatterns = [
    path('home', views.Stats.as_view(), name='index'),
    path('cam', views.cam, name='cam'),
    path('alerts', views.alerts, name='alerts'),
    path('recordings', views.recordings, name='recordings')
]