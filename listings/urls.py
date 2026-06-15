from django.urls import path
from . import views

urlpatterns = [
    # Main listing pages
    path('', views.home_view, name='home'),                                          # Homepage with featured properties
    path('listings/', views.all_listings, name='listings'),                          # Main catalog showing all listings
    path('listings/<int:listing_id>/', views.listing_detail, name='listing_detail'), # Individual property detail pages

    # Stripe payment and checkout steps
    path('checkout/<int:listing_id>/', views.checkout_view, name='checkout_view'),   # Confirmation page before paying
    path('checkout/session/<int:listing_id>/', views.create_checkout_session, name='create_checkout_session'), # Endpoint for Stripe to build the checkout session
    path('checkout/success/', views.payment_success, name='payment_success'),        # Land here after paying to log the deposit to the database
]