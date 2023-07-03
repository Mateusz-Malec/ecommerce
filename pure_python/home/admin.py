from django.contrib import admin
from .models import Profile, Desktop, Category, Laptop, Computer, Cart, Product, CartItem

# Register your models here.

admin.site.register(Profile)
admin.site.register(Desktop)
admin.site.register(Category)
admin.site.register(Laptop)
admin.site.register(Computer)
admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(CartItem)
