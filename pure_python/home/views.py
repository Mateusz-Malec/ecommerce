from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .forms import FilterFormDesktops, FilterFormLaptops
from .models import Computer, Desktop, Laptop
from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth

# Create your views here.

def home(request):
    computers = {"computers": Computer.objects.all()}
    return render(request, 'index.html', computers)

def isAuthenticated(request, default_view):
    context = {}
    if request.user.is_authenticated:
        context['userStatus'] = 'zalogowany'
        return default_view
    else:
        context['userStatus'] = 'niezalogowany'
        return render(request, 'login.html', context)

def computers_(request):
    # template = loader.get_template('index.html')
    # computers = {"computers": Computer.objects.all()}
    filter_form = FilterFormDesktops(request.GET)
    desktops = Desktop.objects.all()

    if filter_form.is_valid():
        ram = filter_form.cleaned_data.get('ram')
        system = filter_form.cleaned_data.get('system')
        if ram:
            desktops = desktops.filter(ram__in=ram)
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
    #laptops = Laptop.objects.all()
    # products.extends(laptops)

    filter_form = FilterFormLaptops(request.GET)
    laptops = Laptop.objects.all()

    if filter_form.is_valid():
        ram = filter_form.cleaned_data.get('ram')
        system = filter_form.cleaned_data.get('system')
        if ram:
            laptops = laptops.filter(ram__in=ram)
        if system:
            laptops = laptops.filter(system__in=system)

    if not any(filter_form.data.values()):
        laptops = Laptop.objects.all()

    context = {
        'laptops': laptops,
        'filter_form': filter_form,
    }
    #just for example how to use authenthication
    return isAuthenticated(request, render(request, 'products.html', context))


def details(request, c_id):
    # computer = Computer.objects.get(pk=c_id)
    computer = get_object_or_404(Computer, pk=c_id)
    return render(request, 'product_detail.html', {"product": computer})

def signup_page(request):
    context = {}
    if request.method == 'POST':
        # Request for sign up
        # Check if user is available
        try:
            user = User.objects.get(username=request.POST['username'])
            context['error'] = 'Podana nazwa użytkownika już istnieje! Proszę podać inną nazwę użytkownika.'
            return render(request, 'signup.html', context)
        except User.DoesNotExist:
            # Check if the password1 is equal to the password2
            if request.POST['password1'] != request.POST['password2']:
                context['error'] = 'Podane hasła nie są takie same! Proszę wprowadzić identyczne hasła.'
                return render(request, 'signup.html', context)
            else:
                # Create new user
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # Automatic login after signing up
                auth.login(request, user)
                # Go to home page
                return redirect('home')
    else:
        return render(request, 'signup.html', context)
def login_page(request):
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'] ,password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Podane hasło lub login są błędne! Podaj poprawne dane.'
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
