from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
import stripe
from .models import Property, Deposit

stripe.api_key = settings.STRIPE_SECRET_KEY


# Home page: Grab all properties marked as featured
def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True)
    context = {'featured_properties': featured_properties}
    return render(request, 'home.html', context)


# Listings directory: Get every property in the system
def all_listings(request):
    properties = Property.objects.all()
    context = {'properties': properties}
    return render(request, 'listings.html', context)


# Detail view: Show information for a single chosen property
def listing_detail(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    is_saved = False
    saved_count = 0

    if request.user.is_authenticated:
        from accounts.models import SavedProperty
        is_saved = SavedProperty.objects.filter(
            user=request.user, property=property_item
        ).exists()
        saved_count = SavedProperty.objects.filter(user=request.user).count()

    context = {
        'property': property_item,
        'is_saved': is_saved,
        'saved_count': saved_count,
    }
    return render(request, 'property_details.html', context)


# Checkout gateway page
@login_required
def checkout_view(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'checkout.html', context)


# Account dashboard
@login_required
def account_dashboard(request):
    deposits = Deposit.objects.filter(user=request.user, paid=True)
    context = {'deposits': deposits}
    return render(request, 'account/dashboard.html', context)


# Handshake with Stripe
@login_required
def create_checkout_session(request, listing_id):
    if request.method == 'POST':
        property_item = get_object_or_404(Property, id=listing_id)
        domain_url = f"{request.scheme}://{request.get_host()}"

        try:
            unit_amount = 25000
            success_url = (
                domain_url + f'/checkout/success/?listing_id='
                f'{property_item.id}&session_id={{CHECKOUT_SESSION_ID}}'
            )
            cancel_url = domain_url + f"/listings/{property_item.id}/"

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp',
                        'product_data': {
                            'name': f"Holding Deposit: {property_item.title}",
                            'description': (
                                f"£250 deposit for {property_item.title}. "
                                f"Monthly rent: £{property_item.price}/month."
                            ),
                        },
                        'unit_amount': unit_amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return JsonResponse({
                'id': checkout_session.id,
                'stripe_public_key': settings.STRIPE_PUBLIC_KEY
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


# Success page processing
def payment_success(request):
    listing_id = request.GET.get('listing_id')
    session_id = request.GET.get('session_id')

    if listing_id and session_id and request.user.is_authenticated:
        property_item = get_object_or_404(Property, id=listing_id)

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_intent_id = session.get('payment_intent')
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