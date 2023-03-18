from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .forms import FilterFormDesktops
from .models import Computer, Desktop, Laptop


# Create your views here.

def home(request):
    computers = {"computers": Computer.objects.all()}
    return render(request, 'index.html', computers)


def computers_(request):
    # template = loader.get_template('index.html')
    # computers = {"computers": Computer.objects.all()}

    filter_form = FilterFormDesktops(request.GET)
    desktops = Desktop.objects.all()

    if filter_form.is_valid():
        ram = filter_form.cleaned_data.get('ram')
        system = filter_form.cleaned_data.get('system')
        if ram:
            desktops = desktops.filter(ram__=ram)
        if system:
            desktops = desktops.filter(system__in=system)

    if not any(filter_form.data.values()):
        desktops = Desktop.objects.all()

    context = {
            'desktops': desktops,
            'filter_form': filter_form,
        }

    return render(request, 'products.html', context)


# return HttpResponse(template.render(computers))

def laptops(request):
    # template = loader.get_template('index.html')
    # computers = {"computers": Computer.objects.all()}

    # filter_form = FilterForm(request.GET)
    laptops = Laptop.objects.all()
    # products.extends(laptops)

    # if filter_form.is_valid():
    #     ram = filter_form.cleaned_data.get('ram')
    #     system = filter_form.cleaned_data.get('system')
    #     if ram:
    #         laptops = laptops.filter(ram__=ram)
    #     if system:
    #         laptops = laptops.filter(system__in=system)
    #
    # if not any(filter_form.data.values()):
    #     laptops = Laptop.objects.all()
    #     # products.extends(laptops)

    context = {
        'laptops': laptops,
        #'filter_form': filter_form,
    }

    return render(request, 'products.html', context)


def details(request, c_id):
    # computer = Computer.objects.get(pk=c_id)
    computer = get_object_or_404(Computer, pk=c_id)
    return render(request, 'product_detail.html', {"product": computer})
