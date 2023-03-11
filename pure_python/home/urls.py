from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('computers/', views.computers_, name='computers'),
    path('computers/<c_id>', views.computer_detail)
]