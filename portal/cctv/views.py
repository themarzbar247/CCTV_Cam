from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 

# Create your views here.
def index(request):
    t = loader.get_template('cctv/stream.html')
    return HttpResponse(t.render({"stream_dir":"dave"}, request))