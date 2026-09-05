from django.db import models
from categories.models import Category


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Book Title")
    author = models.CharField(max_length=150, verbose_name="Author")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Book Category")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")

    def __str__(self) -> str:
        return f"{self.title} ({self.author})"

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"

