from django.db import models


class Client(models.Model):
    login = models.CharField(max_length=15, default="")
    first_name = models.CharField(max_length=30, default="")
    surname = models.CharField(max_length=50, default="")


class Category(models.Model):
    category_name = models.CharField(max_length=50, default="")
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_category = models.ForeignKey(Category, related_name='category_fk', on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)


class Desktop(Product):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=20, default="")
    cpu = models.CharField(max_length=50, default="")
    gpu = models.CharField(max_length=50, default="")
    ram = models.CharField(max_length=50, default="")
    system = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to="home/images", default="")


class Laptop(Product):
    name = models.CharField(max_length=150, default="")
    description = models.TextField(blank=True)
    manufacturer = models.CharField(max_length=20, default="")
    cpu = models.CharField(max_length=50, default="")
    gpu = models.CharField(max_length=50, default="")
    ram = models.CharField(max_length=50, default="")
    disk = models.CharField(max_length=50, default="")
    system = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to="home/images", default="")
