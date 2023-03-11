from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Computer


# Create your views here.

def home(request):
    return HttpResponse("<h1>Sklep</h1>")


def index(request):
    # template = loader.get_template('index.html')
    computers = {"computers": Computer.objects.all()}
    return render(request, 'computers.html', computers)
    # return HttpResponse(template.render(computers))


def computer_detail(request, computer_id):
    computer = Computer.objects.get(pk=computer_id)
    return render(request, 'computer_detail.html', {"computer": computer})
