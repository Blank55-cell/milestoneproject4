from django.core.management.base import BaseCommand
from listings.models import Property


class Command(BaseCommand):
    help = "Seed the database with demo UK property listings"

    def handle(self, *args, **kwargs):
        properties = [
            {
                'title': '2 Bed Apartment, Canary Wharf',
                'description': 'Modern two-bedroom apartment with river views, close to transport links and shops.',
                'location': 'London, E14',
                'price': 2200.00,
                'bedrooms': 2,
                'bathrooms': 1,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800',
            },
            {
                'title': 'Victorian Terrace House, Chorlton',
                'description': 'Charming three-bedroom terrace with a private garden and period features.',
                'location': 'Manchester, M21',
                'price': 1400.00,
                'bedrooms': 3,
                'bathrooms': 1,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800',
            },
            {
                'title': 'Studio Flat, City Centre',
                'description': 'Compact and modern studio, perfect for students or young professionals.',
                'location': 'Leeds, LS1',
                'price': 800.00,
                'bedrooms': 1,
                'bathrooms': 1,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1502672023488-70e25813eb80?w=800',
            },
            {
                'title': '4 Bed Detached House, Cheadle Hulme',
                'description': 'Spacious family home with driveway, garage, and large rear garden.',
                'location': 'Stockport, SK8',
                'price': 1850.00,
                'bedrooms': 4,
                'bathrooms': 2,
                'is_featured': True,
                'image_url': 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800',
            },
            {
                'title': '1 Bed Flat, Jesmond',
                'description': 'Stylish one-bedroom flat in a popular residential area close to amenities.',
                'location': 'Newcastle upon Tyne, NE2',
                'price': 950.00,
                'bedrooms': 1,
                'bathrooms': 1,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=800',
            },
            {
                'title': '3 Bed Semi-Detached, Headingley',
                'description': 'Well-presented semi-detached home, ideal for sharers, with off-street parking.',
                'location': 'Leeds, LS6',
                'price': 1300.00,
                'bedrooms': 3,
                'bathrooms': 1,
                'is_featured': False,
                'image_url': 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=800',
            },
        ]

        for prop in properties:
            obj, created = Property.objects.get_or_create(
                title=prop['title'],
                defaults=prop
            )
            status = "Created" if created else "Already exists"
            self.stdout.write(self.style.SUCCESS(f"{status}: {obj.title}"))

        self.stdout.write(self.style.SUCCESS("Seeding complete."))