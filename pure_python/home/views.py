from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.sessions.backends.cache import SessionStore
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import FilterFormDesktops, FilterFormLaptops, UpdateUserForm
from .models import Computer, Desktop, Laptop, Cart, Product, CartItem
from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


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
    # laptops = Laptop.objects.all()
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
    # just for example how to use authenthication
    return render(request, 'products.html', context)
    # return isAuthenticated(request, render(request, 'products.html', context))


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
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Podane hasło lub login są błędne! Podaj poprawne dane.'
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')


def logout_page(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('home')


@login_required(login_url='/login/')
def user_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            return redirect(to='home')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'user_profile.html', {'user_form': user_form})


# def cart_view(request):
#     session_id = request.session.session_key or SessionStore().session_key
#     cart = Cart.objects.get_or_create(user=request.user)
#     cart_items = cart.products.all()
#     total_price = sum(item.price for item in cart_items)
#     context = {'cart_items': cart_items, 'total_price': total_price}
#     return render(request, 'cart.html', context)


def cart_view(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        if not created:
            cart_items = cart.products.all()
            # cart_items.save()
    else:
        session_id = request.session.session_key or SessionStore().session_key
        user = User.objects.get(username='user')
        cart, created = Cart.objects.get_or_create(user=user)
        if not created:
            cart_items = cart.products.all()
    # cart_items = cart.products.all()
    total_price = sum(item.price for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'cart.html', context)


def add_to_cart(request, p_id):
    product = get_object_or_404(Product, pk=p_id)
    cart, __ = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product=product)
    # cart, created = CartItem.objects.get_or_create(cart=cart, product=product)
    return redirect('cart')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password-reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')
