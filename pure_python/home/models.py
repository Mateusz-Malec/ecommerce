from django.contrib.auth.models import User
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


class Cart(models.Model):
    session_id = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    products = models.ManyToManyField(Product, through='CartItem')

    def add_product(self, product, quantity=1):
        """
        Dodaj produkt do koszyka z określoną ilością.
        """
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def remove_product(self, product):
        """
        Usuń produkt z koszyka.
        """
        cart_item = CartItem.objects.get(cart=self, product=product)
        cart_item.delete()

    def update_product_quantity(self, product, quantity):
        """
        Zaktualizuj ilość produktu w koszyku.
        """
        cart_item = CartItem.objects.get(cart=self, product=product)
        cart_item.quantity = quantity
        cart_item.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # price = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.product.quantity -= self.quantity
            self.product.save()
        else:
            original_cart_item = CartItem.objects.get(pk=self.pk)
            self.product.quantity -= self.quantity - original_cart_item.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    @property
    def price(self):
        return self.product.price * self.quantity
