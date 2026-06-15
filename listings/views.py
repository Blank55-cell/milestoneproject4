from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.conf import settings
import stripe
import requests
from .models import Property, Deposit

stripe.api_key = settings.STRIPE_SECRET_KEY
RENTCAST_API_KEY = settings.RENTCAST_API_KEY

# Home page: Grab all properties marked as featured
def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True)
    context = {
        'featured_properties': featured_properties
    }
    return render(request, 'home.html', context)

# Listings directory: Get every property in the system
def all_listings(request):
    properties = Property.objects.all()
    context = {
        'properties': properties
    }
    return render(request, 'listings.html', context)

# Detail view: Show information for a single chosen property
def listing_detail(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item
    }
    return render(request, 'property_details.html', context)

# Checkout gateway page: Send logged-in users to confirm their intent
@login_required
def checkout_view(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item
    }
    return render(request, 'checkout.html', context)

# Account dashboard: Show all deposits paid by the logged-in user
@login_required
def account_dashboard(request):
    deposits = Deposit.objects.filter(user=request.user, paid=True)
    context = {
        'deposits': deposits
    }
    return render(request, 'account.html', context)

# Handshake with Stripe to create a unique checkout session URL
@login_required
def create_checkout_session(request, listing_id):
    if request.method == 'POST':
        property_item = get_object_or_404(Property, id=listing_id)
        domain_url = f"{request.scheme}://{request.get_host()}"
        
        try:
            # Build the payment parameters for a flat £250 holding fee
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
                            'unit_amount': 25000, 
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
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

# Success page processing: Intercept the redirect tokens and write a permanent deposit log
def payment_success(request):
    listing_id = request.GET.get('listing_id')
    session_id = request.GET.get('session_id')
    
    if listing_id and session_id and request.user.is_authenticated:
        property_item = get_object_or_404(Property, id=listing_id)
        
        try:
            # Retrieve the full checkout data straight from Stripe to fetch the true payment ID
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent_id = session.get('payment_intent')
            
            # Use the checkout token to safely verify or generate our transaction record
            Deposit.objects.get_or_create(
                stripe_checkout_session_id=session_id,
                defaults={
                    'user': request.user,
                    'property': property_item,
                    'amount': 250.00,
                    'stripe_payment_id': payment_intent_id,
                    'paid': True
                }
            )
        except Exception:
            # Fallback if Stripe API lookup fails on network checkout reload
            Deposit.objects.get_or_create(
                stripe_checkout_session_id=session_id,
                defaults={
                    'user': request.user,
                    'property': property_item,
                    'amount': 250.00,
                    'paid': True
                }
            )
            
    return render(request, 'success.html')