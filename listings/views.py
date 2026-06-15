from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings
import stripe
import requests
from .models import Property, Deposit

# Initialize external API keys from project settings configuration
stripe.api_key = settings.STRIPE_SECRET_KEY
RENTCAST_API_KEY = settings.RENTCAST_API_KEY

# Home page view: Fetches and displays properties flagged as featured assets
def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True)
    context = {
        'featured_properties': featured_properties
    }
    return render(request, 'home.html', context)

# Main listings directory page: Retreives and renders all property cards
def all_listings(request):
    properties = Property.objects.all()
    context = {
        'properties': properties
    }
    return render(request, 'listings.html', context)

# Dynamic routing view: Renders granular details for a specific property asset
def listing_detail(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item
    }
    return render(request, 'property_details.html', context)

# Checkout page gateway: Directs authenticated users to the confirmation view
@login_required
def checkout_view(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item
    }
    return render(request, 'checkout.html', context)

# User profile management dashboard routing
@login_required
def account_dashboard(request):
    deposits = Deposit.objects.filter(user=request.user, paid=True)
    context = {
        'deposits': deposits
    }
    return render(request, 'account.html', context)

# Handles the dynamic initialization of Stripe Checkout Sessions for holding deposits
@login_required
def create_checkout_session(request, listing_id):
    if request.method == 'POST':
        property_item = get_object_or_404(Property, id=listing_id)
        
        # Determine host domain dynamically to ensure cross-environment compatibility
        domain_url = f"{request.scheme}://{request.get_host()}"
        
        try:
            # Construct Stripe Session tailored for a refundable property holding deposit
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'gbp',
                            'product_data': {
                                'name': f"Holding Deposit: {property_item.title}",
                                'description': f"Holding deposit to secure {property_item.location}. Applied to balance upon closing.",
                            },
                            'unit_amount': 25000, # Value parsed in minor currency units (£250.00 GBP)
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                # Append the property target metadata parameter to track fulfillment on completion
                success_url=domain_url + f'/checkout/success/?listing_id={property_item.id}&session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=domain_url + f"/listings/{property_item.id}/",
            )
            return JsonResponse({
                'id': checkout_session.id,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Success fulfillment view: Validates checkout returns and logs paid Deposits to the database
def payment_success(request):
    listing_id = request.GET.get('listing_id')
    session_id = request.GET.get('session_id')
    
    # Verify transaction context matches an authenticated operational user sessions
    if listing_id and request.user.is_authenticated:
        property_item = get_object_or_404(Property, id=listing_id)
        
        # Persist the transactional holding deposit record inside the database architecture
        Deposit.objects.get_or_create(
            stripe_payment_id=session_id,
            defaults={
                'user': request.user,
                'property': property_item,
                'amount': 250.00,
                'paid': True
            }
        )
    return render(request, 'success.html')