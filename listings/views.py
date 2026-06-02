from django.http import HttpResponse

def all_listings(request):
    return HttpResponse("Welcome to the listings page!")

def listing_detail(request, listing_id):
    return HttpResponse(f"Looking at listing details for ID: {listing_id}")