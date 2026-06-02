from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')  # Renders the home template

def all_listings(request):
    return HttpResponse("Welcome to the listings page!")  # Test response for listings

def listing_detail(request, listing_id):
    return HttpResponse(f"Looking at listing details for ID: {listing_id}")  # Dynamic listing ID test