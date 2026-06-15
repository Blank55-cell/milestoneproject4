from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SavedProperty
from listings.models import Property

@login_required
def toggle_save_property(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    # If it's already saved, delete it (remove). If not, create it (add).
    saved, created = SavedProperty.objects.get_or_create(user=request.user, property=property_item)
    
    if not created:
        saved.delete()
        
    return redirect(request.META.get('HTTP_REFERER', 'listings'))
