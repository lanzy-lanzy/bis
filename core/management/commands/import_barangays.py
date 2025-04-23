import requests
import json
from django.core.management.base import BaseCommand, CommandError
from core.models import Barangay
from django.db import transaction
from tqdm import tqdm
import time


class Command(BaseCommand):
    help = 'Import barangay data from the PSGC API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--region',
            type=str,
            help='Filter by region code (e.g., 01, 02, NCR)',
        )
        parser.add_argument(
            '--province',
            type=str,
            default='Zamboanga del Sur',
            help='Filter by province name (case-insensitive), default: Zamboanga del Sur',
        )
        parser.add_argument(
            '--municipality',
            type=str,
            default='Dumingag',
            help='Filter by municipality name (case-insensitive), default: Dumingag',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Limit the number of barangays to import',
        )
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

        self.stdout.write(self.style.SUCCESS('Starting barangay data import...'))

        # First, get all regions
        regions_url = 'https://psgc.gitlab.io/api/regions.json'
        self.stdout.write(self.style.SUCCESS(f'Fetching regions from {regions_url}'))

        try:
            regions_response = requests.get(regions_url)
            regions_response.raise_for_status()
            regions = regions_response.json()
        except requests.exceptions.RequestException as e:
            raise CommandError(f'Error fetching regions: {e}')

        # Filter regions if specified
        if options['region']:
            regions = [r for r in regions if r['code'] == options['region']]
            if not regions:
                raise CommandError(f'No region found with code {options["region"]}')

        # Process each region
        for region in regions:
            region_code = region['code']
            region_name = region['name']
            self.stdout.write(self.style.SUCCESS(f'Processing region: {region_name} ({region_code})'))

            # Get provinces in this region
            provinces_url = f'https://psgc.gitlab.io/api/regions/{region_code}/provinces.json'

            try:
                provinces_response = requests.get(provinces_url)
                provinces_response.raise_for_status()
                provinces = provinces_response.json()
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.WARNING(f'Error fetching provinces for region {region_code}: {e}'))
                # Try to get cities directly for regions like NCR
                self.process_cities_in_region(region_code, region_name, options)
                continue

            # Filter provinces if specified
            if options['province']:
                provinces = [p for p in provinces if options['province'].lower() in p['name'].lower()]
                if not provinces:
                    self.stdout.write(self.style.WARNING(f'No provinces found matching "{options["province"]}" in region {region_name}'))
                    continue

            # Process each province
            for province in provinces:
                province_code = province['code']
                province_name = province['name']
                self.stdout.write(self.style.SUCCESS(f'Processing province: {province_name} ({province_code})'))

                # Process municipalities in this province
                self.process_municipalities(province_code, province_name, options)

        self.stdout.write(self.style.SUCCESS('Barangay data import completed successfully!'))

    def process_cities_in_region(self, region_code, region_name, options):
        """Process cities directly under a region (like NCR)"""
        cities_url = f'https://psgc.gitlab.io/api/regions/{region_code}/cities.json'

        try:
            cities_response = requests.get(cities_url)
            cities_response.raise_for_status()
            cities = cities_response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.WARNING(f'Error fetching cities for region {region_code}: {e}'))
            return

        # Filter municipalities/cities if specified
        if options['municipality']:
            cities = [m for m in cities if options['municipality'].lower() in m['name'].lower()]
            if not cities:
                self.stdout.write(self.style.WARNING(f'No cities found matching "{options["municipality"]}" in region {region_name}'))
                return

        # Process each city
        for city in cities:
            city_code = city['code']
            city_name = city['name']
            self.stdout.write(self.style.SUCCESS(f'Processing city: {city_name} ({city_code})'))

            # Get barangays in this city
            self.process_barangays(city_code, city_name, region_name, options)

    def process_municipalities(self, province_code, province_name, options):
        """Process municipalities in a province"""
        # Get municipalities in this province
        municipalities_url = f'https://psgc.gitlab.io/api/provinces/{province_code}/municipalities.json'

        try:
            municipalities_response = requests.get(municipalities_url)
            municipalities_response.raise_for_status()
            municipalities = municipalities_response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.WARNING(f'Error fetching municipalities for province {province_code}: {e}'))
            municipalities = []

        # Get cities in this province
        cities_url = f'https://psgc.gitlab.io/api/provinces/{province_code}/cities.json'

        try:
            cities_response = requests.get(cities_url)
            cities_response.raise_for_status()
            cities = cities_response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.WARNING(f'Error fetching cities for province {province_code}: {e}'))
            cities = []

        # Combine municipalities and cities
        all_municipalities = municipalities + cities

        # Filter municipalities/cities if specified
        if options['municipality']:
            all_municipalities = [m for m in all_municipalities if options['municipality'].lower() in m['name'].lower()]
            if not all_municipalities:
                self.stdout.write(self.style.WARNING(f'No municipalities/cities found matching "{options["municipality"]}" in province {province_name}'))
                return

        # Process each municipality/city
        for municipality in all_municipalities:
            municipality_code = municipality['code']
            municipality_name = municipality['name']
            self.stdout.write(self.style.SUCCESS(f'Processing municipality/city: {municipality_name} ({municipality_code})'))

            # Get barangays in this municipality/city
            self.process_barangays(municipality_code, municipality_name, province_name, options)

    def process_barangays(self, parent_code, municipality_name, province_name, options):
        """Process barangays in a municipality/city"""
        # Get barangays in this municipality/city
        barangays_url = f'https://psgc.gitlab.io/api/{parent_code}/barangays.json'

        try:
            barangays_response = requests.get(barangays_url)
            barangays_response.raise_for_status()
            barangays = barangays_response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.WARNING(f'Error fetching barangays for {parent_code}: {e}'))
            return

        # Apply limit if specified
        if options['limit'] and len(barangays) > options['limit']:
            barangays = barangays[:options['limit']]

        # Create barangays in the database
        with transaction.atomic():
            for barangay in tqdm(barangays, desc=f'Importing barangays in {municipality_name}'):
                barangay_name = barangay['name']

                # Generate a zip code (since the API doesn't provide this)
                # In a real application, you would want to use actual zip codes
                zip_code = f"{parent_code[:2]}00"  # Use first 2 digits of parent code + 00

                # Use specific zip code for Dumingag, Zamboanga del Sur
                if municipality_name.lower() == 'dumingag' and province_name.lower() == 'zamboanga del sur':
                    zip_code = "7028"

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
