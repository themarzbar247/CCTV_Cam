from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader 

# Create your views here.
def index(request):

    #t = loader.get_template('cctv/index.html')
    #t.render({"stream_dir":"dave"})
    return HttpResponse(request, "index.html")