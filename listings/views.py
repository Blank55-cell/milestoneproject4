from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings
import stripe
import requests # helpful for making RentCast API requests later
from .models import Property

# Pull api keys from settings config
stripe.api_key = settings.STRIPE_SECRET_KEY
RENTCAST_API_KEY = settings.RENTCAST_API_KEY

# Home page view
def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True)
    context = {
        'featured_properties': featured_properties
    }
    return render(request, 'home.html', context)

# Main listings page
def all_listings(request):
    properties = Property.objects.all()
    context = {
        'properties': properties
    }
    return render(request, 'listings.html', context)

# Dynamic routing for single listings
def listing_detail(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item
    }
    return render(request, 'property_details.html', context)

# Send user to checkout page
@login_required
def checkout_view(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item
    }
    return render(request, 'checkout.html', context)

# User dashboard routing
@login_required
def account_dashboard(request):
    return render(request, 'account.html')

# Handles the stripe payment intent creation
@login_required
def create_checkout_session(request, listing_id):
    if request.method == 'POST':
        property_item = get_object_or_404(Property, id=listing_id)
        
        # Pull dynamic hostname for urls
        domain_url = f"{request.scheme}://{request.get_host()}"
        
        try:
            # Stripe checkout setup
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                                'name': f"Viewing Booking: {property_item.title}",
                                'description': f"Securing your appointment for {property_item.location}",
                            },
                            'unit_amount': 1000, # 10.00 GBP
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=domain_url + '/checkout/success/',
                cancel_url=domain_url + f"/listings/{property_item.id}/",
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Success page redirect
def payment_success(request):
    return render(request, 'success.html')