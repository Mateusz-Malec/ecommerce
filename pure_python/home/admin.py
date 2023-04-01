from django.contrib import admin
from .models import Profile, Desktop, Category, Laptop, Computer

# Register your models here.

admin.site.register(Profile)
admin.site.register(Desktop)
admin.site.register(Category)
admin.site.register(Laptop)
admin.site.register(Computer)
