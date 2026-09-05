from decimal import Decimal

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid

User = get_user_model()

class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PROCESSING = 'processing', 'Processing'
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        CANCELED = 'canceled', 'Canceled'
        REFUNDED = 'refunded', 'Refunded'
        PARTIAL_REFUND = 'partial_refund', 'Partially Refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments',null=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, db_index=True)
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.5'))])
    currency = models.CharField(max_length=5, default='USD')
    status = models.CharField(max_length=40, choices=Status.choices, default=Status.PENDING)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    error = models.TextField(blank=True, null=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))

    class Meta:
        db_table = 'stripe_payment'
        verbose_name = 'Stripe Payment'
        verbose_name_plural = 'Stripe Payments'
        ordering = ['-id']

    def __str__(self):
        return f'Payment {self.id} - {self.amount} {self.currency} ({self.status})'

    @property
    def is_success(self):
        return self.status == self.Status.SUCCESS

    @property
    def can_be_refunded(self):
        return (self.is_success and self.refund_amount <= self.amount)