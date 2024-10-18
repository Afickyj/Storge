# models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    ROLE_CHOICES = [
        ('ADMINISTRATOR', 'Administrator'),
        ('USER', 'User'),
    ]

    COMMUNICATION_CHANNEL_CHOICES = [
        ('POST', 'Pošta'),
        ('EMAIL', 'Email'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    communication_channel = models.CharField(max_length=10, choices=COMMUNICATION_CHANNEL_CHOICES, default='EMAIL')

    def __str__(self):
        return f'{self.user.username} Profile'

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=200, blank=True)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    availability = models.BooleanField(default=True)
    author = models.ForeignKey(
        User,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

    class Meta:
        permissions = [
            ("can_edit_product", "Can edit product"),
            ("can_delete_product", "Can delete product"),
        ]

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Hotově při doručení'),
        ('card', 'Kartou při doručení'),
    ]

    DELIVERY_CHOICES = [
        ('courier', 'Kurýr'),
        ('pickup', 'Osobní odběr'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Čekající'),
        ('processed', 'Zpracováno'),
        ('shipped', 'Odesláno'),
        ('delivered', 'Doručeno'),
    ]

    # Umožnit uživateli být null a blank
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    # Přidat pole pro informace o zákazníkovi
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=255, default='Zadejte adresu doručení')
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='courier')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    delivery_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Objednávka {self.id}'

    def get_total_cost(self):
        items_total = sum(item.get_cost() for item in self.items.all())
        return items_total + self.delivery_price

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_cost(self):
        return self.price * self.quantity
