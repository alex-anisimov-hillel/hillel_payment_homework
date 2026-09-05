from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from users.models import User
from books.models import Book

from django.contrib.auth import get_user_model

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        PAID = 'paid', 'Paid'
        IN_WORK = 'in work', 'In work'
        SENT = 'sent', 'Sent'
        DELIVERED = 'delivered', 'Delivered'
        CANCELED = 'canceled', 'Canceled'

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.OneToOneField('payment.Payment', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f'{self.user} -- {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f'{self.order} -- {self.book} -- {self.price}'