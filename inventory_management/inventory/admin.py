from django.contrib import admin
from .models import InventoryItem, Category

admin.site.register(InventoryItem)
admin.site.register(Category)
