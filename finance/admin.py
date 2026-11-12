from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, TransactionCategory, Transaction

class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'user', 'budget']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['type', 'category', 'description', 'amount', 'date']

class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(TransactionCategory, TransactionCategoryAdmin)
admin.site.register(Transaction, TransactionAdmin)