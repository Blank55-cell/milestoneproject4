from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'is_featured')
    list_filter = ('is_featured', 'bedrooms', 'bathrooms')
    search_fields = ('title', 'location')