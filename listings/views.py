from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property

# Landing page setup
def home_view(request):
    featured_properties = Property.objects.filter(is_featured=True)
    context = {
        'featured_properties': featured_properties
    }
    return render(request, 'home.html', context)

# Temporary setup to make sure listings page is hitting the right path
def all_listings(request):
    properties = Property.objects.all()
    context = {
        'properties': properties
    }
    return render(request, 'listings.html', context)

# Pulls the property ID from the URL to test dynamic routing
def listing_detail(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    context = {
        'property': property_item
    }
    return render(request, 'property_details.html', context)

# Only logged‑in users should be able to see their dashboard
@login_required
def account_dashboard(request):
    return render(request, 'account.html')