from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Computer


# Create your views here.

def home(request):
    computers = {"computers": Computer.objects.all()}
    return render(request, 'index.html', computers)


def computers_(request):
    # template = loader.get_template('index.html')
    computers = {"computers": Computer.objects.all()}
    return render(request, 'computers.html', computers)
    # return HttpResponse(template.render(computers))


def computer_detail(request, c_id):
    # computer = Computer.objects.get(pk=c_id)
    computer = get_object_or_404(Computer, pk=c_id)
    return render(request, 'computer_detail.html', {"computer": computer})
