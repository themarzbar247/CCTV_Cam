from django.shortcuts import render
from django.http import HttpResponse, request, response
from django.template import loader 
from django.views import generic
import os

# Create your views here.
def index(request):
    return render(request, "index.html")

# Create your views here.
def cctv(request):
    context = {
    'stream_dir' : next(os.walk('cctv\static\cameras'))[1],
    'dict_values' : {'a':1, 'b':2, 'c':3}

    }
    return render(request, "cctv/stream.html", context=context)
