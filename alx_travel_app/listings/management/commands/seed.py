from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Seed database with sample listing data'

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            self.stdout.write("Please create at least one user before running the seeder.")
            return

        user = User.objects.first()
        sample_titles = ['Cozy Cottage', 'Beach House', 'City Apartment', 'Mountain Cabin']
        locations = ['Accra', 'Kumasi', 'Tamale', 'Takoradi']

        for i in range(10):
            Listing.objects.create(
                title=random.choice(sample_titles),
                description='Sample description for listing.',
                location=random.choice(locations),
                price_per_night=random.randint(100, 500),
                owner=user
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded 10 listings.'))
