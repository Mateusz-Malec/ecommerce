from django.db import models


# Create your models here.

class Client(models.Model):
    login = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)


class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    price = models.IntegerField(default=0)
    numbers = models.IntegerField(default=0)


class Computer(Product):
    computer_id = models.CharField(max_length=20)
    full_name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000, default="")
    cpu = models.CharField(max_length=50, default="")
    gpu = models.CharField(max_length=50, default="")
    ram = models.CharField(max_length=50, default="")
    system = models.CharField(max_length=50, default="")
