from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from listings.models import Deposit, Property
from .models import SavedProperty


@login_required
def account_dashboard(request):
    # Grab all successful deposits for the logged-in user
    user_deposits = Deposit.objects.filter(
        user=request.user, paid=True
    ).order_by('-created_at')

    # Grab saved properties for comparison
    saved_properties = SavedProperty.objects.filter(
        user=request.user
    ).order_by('-added_at')

    context = {
        'deposits': user_deposits,
        'saved_properties': saved_properties,
        'saved_count': saved_properties.count(),
    }
    return render(request, 'account/dashboard.html', context)


@login_required
def toggle_save_property(request, listing_id):
    property_item = get_object_or_404(Property, id=listing_id)
    existing = SavedProperty.objects.filter(
        user=request.user, property=property_item
    ).first()

    if existing:
        # Already saved — remove it
        existing.delete()
        messages.success(request, f'"{property_item.title}" removed from your saved properties.')
    else:
        # Enforce 3-property limit
        if SavedProperty.objects.filter(user=request.user).count() >= 3:
            messages.error(request, 'You can only save up to 3 properties. Remove one first.')
        else:
            SavedProperty.objects.create(user=request.user, property=property_item)
            messages.success(request, f'"{property_item.title}" saved to your dashboard.')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def remove_saved_property(request, saved_id):
    # Only lets the owner delete their own saved property
    saved = get_object_or_404(SavedProperty, id=saved_id, user=request.user)
    title = saved.property.title
    saved.delete()
    messages.success(request, f'"{title}" removed from your saved properties.')
    return redirect('account_dashboard')