import locale
import uuid
from datetime import date, datetime
from io import BytesIO

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sessions.backends.cache import SessionStore
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph

from requests import Response

from .forms import FilterFormLaptops, FilterFormDesktops, UpdateUserForm
from .models import Computer, Desktop, Laptop, Cart, Product
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    total_quantity = request.session.get('total_quantity')
    computers = Computer.objects.all()
    return render(request, 'index.html', {'computers': computers, 'total_quantity': total_quantity})


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
    else:
        session_id = request.session.session_key or SessionStore().session_key
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['session_id'] = session_id
        cart, created = Cart.objects.get_or_create(session_id=session_id, user=None)

    cart_items = cart.cartitem_set.all()
    total_price = sum(item.price for item in cart_items)
    total_quantity = sum(item.quantity for item in cart_items)
    request.session['total_quantity'] = total_quantity
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity
    }
    return render(request, 'cart.html', context)


def add_to_cart(request, p_id):
    product = get_object_or_404(Product, pk=p_id)
    cart, __ = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product=product)
    # cart, created = CartItem.objects.get_or_create(cart=cart, product=product)
    return redirect('cart')


# @require_http_methods(["PUT"])
def update_product_in_cart(request, p_id, quant):
    product = get_object_or_404(Product, pk=p_id)
    cart, __ = Cart.objects.get_or_create(user=request.user)
    cart.update_product_quantity(product=product, quantity=int(quant))
    cart.save()
    # cart, created = CartItem.objects.get_or_create(cart=cart, product=product)
    return Response()
    # return redirect('cart')


def remove_from_cart(request, p_id):
    product = get_object_or_404(Product, pk=p_id)
    cart, __ = Cart.objects.get_or_create(user=request.user)
    cart.remove_product(product=product)
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


def checkout(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = cart.cartitem_set.all()
    quantity_list = []
    product_keys_list = []
    for i, item in enumerate(cart_items):
        quantity_list.append(item.quantity)
        product_keys_list.append(item.product.product_stripe_key)

    stripe_products_ordered = []
    for product, quantity in zip(product_keys_list, quantity_list):
        stripe_products_ordered.append({'price': product, 'quantity': quantity})
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=stripe_products_ordered,
            mode='payment',
            success_url='http://127.0.0.1:8000/cart',
            cancel_url='http://127.0.0.1:8000',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


def generatePDF(request):
    # Get cart data
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.price for item in cart_items)
    # Prepare table data
    locale.setlocale(locale.LC_ALL, 'pl_PL')
    table_data = [['Lp.', 'Nazwa produktu', 'Ilosc', 'Jm', 'Cena', 'Wartosc']]
    for i, item in enumerate(cart_items):
        table_data.append([i + 1, item.product.computer.name, item.quantity, 'szt.',
                           locale.currency(item.product.price, grouping=True),
                           locale.currency(item.price, grouping=True)])
    table_data.append(['', '', '', '', 'Suma:', locale.currency(total_price, grouping=True)])
    # Define table style
    style = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 13),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('ALIGN', (-1, 1), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('SPAN', (0, -1), (-3, -1)),
    ])

    # Create table object
    t = Table(table_data)
    t.setStyle(style)

    # Define KUPUJĄCY section
    title_style = ParagraphStyle(
        name='date',
        fontName='Helvetica',
        fontSize=10,
        textColor=black,
        leading=14,
        spaceAfter=10,
        alignment=TA_RIGHT
    )

    generate_date = Paragraph(f'Data wygenerowania: {date.today()}', title_style)

    usertable_data = [['NABYWCA'], [f'{User.get_full_name(request.user)}'], [f'{request.user.email}']]

    userstyle = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 13),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
    ])

    u = Table(usertable_data)
    u.setStyle(userstyle)

    # Build PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = [generate_date, u, t]
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    # Serve PDF file as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{request.user}_cart_{date.today()}.pdf"'
    return response
