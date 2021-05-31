from django.db.models import query
from django.shortcuts import render
from .models import *
from django.db.models import Count
from django.views import generic
from django.db.models.functions import TruncDate
import os

# Create your views here.
def index(request):
    notification_count = Notification.objects.all().aggregate(Count('notificationId'))
    camera_count = Cameras.objects.all().aggregate(Count('cameraId'))
    unique_rules_count = Alert.objects.all().aggregate(Count('alertId'))
    days_Recorded = Recordings.objects.annotate(date=TruncDate('recordingDate')).values('date').distinct().aggregate(dates=Count('date'))
    cameras_inactive = 4
    rules_inactive = 4
    context = {
        'notification_count' : notification_count['notificationId__count'],
        'camera_count' : camera_count['cameraId__count'],
        'unique_rules_count': unique_rules_count['alertId__count'],
        'days_Recorded' : days_Recorded['dates'],
        'cameras_inactive': cameras_inactive,
        'rules_inactive' : rules_inactive
    }
    return render(request, "pages/index.html", context=context)

# Create your views here.
def cameras(request):
    context = {
    'stream_dir' : next(os.walk('cctv\static\cameras'))[1]
    }
    return render(request, "pages/cam.html", context=context)

def alerts(request):
    return render(request, "pages/alerts.html")

def recordings(request):
    return render(request, "pages/recordings.html")