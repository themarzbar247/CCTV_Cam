from django.db.models import query
from CCTV_Cam.portal.cctv.models import Notification
from django.shortcuts import render
from django.http import HttpResponse, request, response
from django.template import loader 
from django.views import generic
import os

# Create your views here.
class Stats(generic.ListView):
    model = Notification
    context_obj_name = 'notification_list'

# Create your views here.
def cam(request):
    context = {
    'stream_dir' : next(os.walk('cctv\static\cameras'))[1],
    'dict_values' : {'a':1, 'b':2, 'c':3}

    }
    print(context['stream_dir'])
    return render(request, "pages/cam.html", context=context)

def alerts(request):
    return render(request, "pages/alerts.html")

def recordings(request):
    return render(request, "pages/recordings.html")