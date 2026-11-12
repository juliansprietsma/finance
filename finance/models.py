from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractUser):
    pass


class TransactionCategory(models.Model):
    category = models.CharField(max_length=20, blank=False)
    budget = models.IntegerField(blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'category'],
                name='unique_categories_per_user'
            )
        ]

    def __str__(self):
        return self.category

class Transaction(models.Model):
    TYPE_CHOICES = {
        "expense": "expense",
        "income": "income"
    }
    
    description = models.TextField(blank=False)
    category = models.ForeignKey(
        TransactionCategory,
        on_delete=models.CASCADE,
        related_name='transaction',
    )
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES['expense'], blank=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    date = models.DateField(blank=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )