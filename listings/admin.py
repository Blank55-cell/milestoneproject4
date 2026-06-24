from django.contrib import admin
from .models import Property, Deposit


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # Columns shown in the property list view
    list_display = (
        "title",
        "price",
        "location",
        "is_featured"
    )

    # Filters available on the right sidebar
    list_filter = (
        "is_featured",
        "bedrooms",
        "bathrooms"
    )

    # Search bar targets
    search_fields = (
        "title",
        "location"
    )


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    # Columns shown in the deposit list view
    list_display = (
        "user",
        "property",
        "amount",
        "paid",
        "is_refunded",
        "created_at"
    )

    # Filters to sort through payment status quickly
    list_filter = (
        "paid",
        "is_refunded",
        "created_at"
    )

    # Search targets, including relational lookups and Stripe identifiers
    search_fields = (
        "user__username",
        "property__title",
        "stripe_payment_id",
        "stripe_checkout_session_id"
    )
