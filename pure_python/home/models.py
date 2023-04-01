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
    id = models.AutoField(primary_key=True)
    product_category = models.ForeignKey(Category, related_name='category_fk', on_delete=models.CASCADE, null=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)


class Computer(Product):
    name = models.CharField(max_length=150)
    manufacturer = models.CharField(max_length=20, default="")
    cpu = models.CharField(max_length=50, default="")
    gpu = models.CharField(max_length=50, default="")
    ram = models.IntegerField(default=8)
    system = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to="home/images", default="")


class Desktop(Computer):
    description = models.TextField(blank=True)


class Laptop(Computer):
    przekatna = models.DecimalField(default=15.5, decimal_places=1, max_digits=3)
    disk = models.IntegerField(default=256)
    description = models.TextField(blank=True)
