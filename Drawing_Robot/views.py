from django.shortcuts import render
from .services import SVGImageParseService


def index(request):
    return render(request, 'index.html')


def launch_robot(request):
    if request.method == 'POST':
        file = request.FILES['image']
        coordinates = SVGImageParseService.call(file)
        context = {'coordinates': coordinates}
    return render(request, 'image_uploaded.html', context)
