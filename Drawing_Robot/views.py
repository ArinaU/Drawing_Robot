from django.http import HttpResponse
from django.shortcuts import render
from .services import SVGImageParseService
import requests


def index(request):
    return render(request, 'index.html')


def launch_robot(request):
    if request.method == 'POST':
        file = request.FILES['image']
        coordinates = SVGImageParseService.call(file)
        context = {'coordinates': coordinates}
        # response = requests.get('http://192.168.8.137')
        # return HttpResponse(response)
    return render(request, 'image_uploaded.html', context)
