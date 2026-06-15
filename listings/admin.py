from django.contrib import admin
from .models import Property, Deposit

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'is_featured')
    list_filter = ('is_featured', 'bedrooms', 'bathrooms')
    search_fields = ('title', 'location')

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'amount', 'paid', 'is_refunded', 'created_at')
    list_filter = ('paid', 'is_refunded', 'created_at')
    search_fields = ('user__username', 'property__title', 'stripe_payment_id')