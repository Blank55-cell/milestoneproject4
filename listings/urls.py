from django.urls import path
from . import views

urlpatterns = [
    # Main listing pages
    path('', views.home_view, name='home'),
    path('listings/', views.all_listings, name='listings'),
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'),

    # Stripe payment and checkout steps
    path('checkout/<int:listing_id>/', views.checkout_view, name='checkout_view'),
    path('checkout/session/<int:listing_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('checkout/success/', views.payment_success, name='payment_success'),
]