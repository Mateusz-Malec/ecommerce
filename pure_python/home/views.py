from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Desktop


# Create your views here.

def home(request):
    desktops = {"desktops": Desktop.objects.all()}
    return render(request, 'index.html', desktops)


def desktops_(request):
    # template = loader.get_template('index.html')
    desktops = {"desktops": Desktop.objects.all()}
    return render(request, 'desktop.html', desktops)
    # return HttpResponse(template.render(computers))


def desktop_detail(request, c_id):
    # computer = Computer.objects.get(pk=c_id)
    desktop = get_object_or_404(Desktop, pk=c_id)
    return render(request, 'desktop_detail.html', {"desktop": desktop})
