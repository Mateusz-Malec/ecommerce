from django.db import models


# Create your models here.

class Client(models.Model):
    login = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)


class Computer(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    full_name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
