from django.urls import path
from . import views

urlpatterns = [
    # Core Property Catalog Interfaces
    path('', views.home_view, name='home'),                                          # Application Homepage featuring promotional listings
    path('listings/', views.all_listings, name='listings'),                          # Main master directory displaying all active listings
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'), # Granular specifications and data for an isolated property

    # Transactional Checkout Gateways
    path('checkout/<int:listing_id>/', views.checkout_view, name='checkout_view'),   # Gateway entry page outlining holding deposit parameters
    path('checkout/session/<int:listing_id>/', views.create_checkout_session, name='create_checkout_session'), # Stripe endpoint creating tokenized payload
    path('checkout/success/', views.payment_success, name='payment_success'),        # Transaction success interceptor that commits Deposit data to DB
]