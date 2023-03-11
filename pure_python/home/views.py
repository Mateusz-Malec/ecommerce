from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Computer


# Create your views here.

def home(request):
    return HttpResponse("<h1>Sklep</h1>")


def index(request):
    template = loader.get_template('index.html')
    computers = {"computers" : Computer.objects.all()}
    return HttpResponse(template.render(computers))
