from django.contrib import admin
from .models import Client, Desktop, Category, Laptop, Computer

# Register your models here.

admin.site.register(Client)
admin.site.register(Desktop)
admin.site.register(Category)
admin.site.register(Laptop)
admin.site.register(Computer)
