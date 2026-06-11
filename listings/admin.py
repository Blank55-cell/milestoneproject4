from django.contrib import admin
from .models import Property, Booking

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'is_featured')
    list_filter = ('is_featured', 'bedrooms', 'bathrooms')
    search_fields = ('title', 'location')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'booking_date', 'paid')
    list_filter = ('paid', 'booking_date')
    search_fields = ('user__username', 'property__title', 'stripe_payment_id')