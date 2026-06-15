# listings/services.py
import requests
from django.conf import settings
from .models import Property

def sync_rentcast_properties():
    url = "https://api.rentcast.io/v1/listings/listings"
    headers = {"accept": "application/json", "X-Api-Key": settings.RENTCAST_API_KEY}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            Property.objects.update_or_create(
                id=item.get('id'),
                defaults={
                    'title': item.get('formattedAddress'),
                    'price': item.get('price'),
                }
            )