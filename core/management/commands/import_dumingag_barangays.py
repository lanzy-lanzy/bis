import requests
import json
from django.core.management.base import BaseCommand, CommandError
from core.models import Barangay
from django.db import transaction
from tqdm import tqdm
import time


class Command(BaseCommand):
    help = 'Import barangay data for Dumingag municipality from the PSGC API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing barangay data before importing',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing barangay data...'))
            Barangay.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Existing barangay data cleared.'))

        self.stdout.write(self.style.SUCCESS('Starting Dumingag barangay data import...'))

        # Zamboanga del Sur province code
        province_code = '097300000'  # This is the code for Zamboanga del Sur
        province_name = 'Zamboanga del Sur'

        # First, find Dumingag municipality
        self.stdout.write(self.style.SUCCESS(f'Looking for Dumingag municipality in {province_name}...'))

        # Get municipalities in Zamboanga del Sur
        municipalities_url = f'https://psgc.gitlab.io/api/provinces/{province_code}/municipalities.json'

        try:
            municipalities_response = requests.get(municipalities_url)
            municipalities_response.raise_for_status()
            municipalities = municipalities_response.json()
        except requests.exceptions.RequestException as e:
            raise CommandError(f'Error fetching municipalities: {e}')

        # Find Dumingag
        dumingag = None
        for municipality in municipalities:
            if municipality['name'].lower() == 'dumingag':
                dumingag = municipality
                break

        if not dumingag:
            raise CommandError('Dumingag municipality not found in Zamboanga del Sur')

        municipality_code = dumingag['code']
        municipality_name = dumingag['name']

        self.stdout.write(self.style.SUCCESS(f'Found Dumingag municipality (code: {municipality_code})'))

        # Get barangays in Dumingag
        barangays_url = f'https://psgc.gitlab.io/api/municipalities/{municipality_code}/barangays.json'

        try:
            barangays_response = requests.get(barangays_url)
            barangays_response.raise_for_status()
            barangays = barangays_response.json()
        except requests.exceptions.RequestException as e:
            raise CommandError(f'Error fetching barangays: {e}')

        self.stdout.write(self.style.SUCCESS(f'Found {len(barangays)} barangays in Dumingag'))

        # Create barangays in the database
        with transaction.atomic():
            for barangay in tqdm(barangays, desc=f'Importing barangays in {municipality_name}'):
                barangay_name = barangay['name']

                # Generate a zip code (since the API doesn't provide this)
                # In a real application, you would want to use actual zip codes
                zip_code = "7028"  # Dumingag, Zamboanga del Sur zip code

                # Create or update the barangay
                Barangay.objects.update_or_create(
                    name=barangay_name,
                    municipality=municipality_name,
                    province=province_name,
                    defaults={
                        'zip_code': zip_code,
                    }
                )

                # Add a small delay to avoid overwhelming the API
                time.sleep(0.01)

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(barangays)} barangays from {municipality_name}, {province_name}'))
