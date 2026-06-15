from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from listings.models import Deposit, Property
from .models import SavedProperty

@login_required
def account_dashboard(request):
    # I'm grabbing all successful deposits for the logged-in user
    user_deposits = Deposit.objects.filter(user=request.user, paid=True).order_by('-created_at')
    
    context = {
        'deposits': user_deposits
    }
    return render(request, 'account/account.html', context)

@login_required
def toggle_save_property(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    # Using get_or_create to toggle the save status
    saved, created = SavedProperty.objects.get_or_create(user=request.user, property=property_item)
    
    if not created:
        saved.delete()
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))