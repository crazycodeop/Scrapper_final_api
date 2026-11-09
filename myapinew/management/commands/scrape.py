import logging
from django.core.management.base import BaseCommand
from myapinew.scrapers import (
    scrape_nobroker_rent,
    scrape_nobroker_sale,
    scrape_nobroker_comm_rent,
    scrape_nobroker_comm_sale,
    scrape_nobroker_pg,
    scrape_magicbricks_sale,
    scrape_magicbricks_rent,
    scrape_magicbricks_pg,
    scrape_magicbricks_comm_sale,
    scrape_magicbricks_comm_lease,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Scrape real estate data from NoBroker and/or MagicBricks and store into the database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='nobroker',
            choices=['all', 'nobroker', 'magicbricks'],
            help="Data source to scrape (nobroker, magicbricks, or all).",
        )
        parser.add_argument(
            '--category',
            type=str,
            default='all',
            choices=['all', 'rent', 'sale', 'comm_rent', 'comm_sale', 'pg'],
            help="Property category to scrape.",
        )
        parser.add_argument(
            '--city',
            type=str,
            default='mumbai',
            help="City to scrape (e.g., mumbai, pune, bangalore).",
        )
        parser.add_argument(
            '--pages',
            type=int,
            default=1,
            help="Number of pages to scrape per category (default: 1).",
        )
        parser.add_argument(
            '--details',
            action='store_true',
            help="Whether to fetch individual detail pages (slower, but fetches all extra fields).",
        )

    def handle(self, *args, **options):
        source = options['source']
        category = options['category']
        city = options['city']
        pages = options['pages']
        fetch_details = options['details']

        self.stdout.write(
            self.style.NOTICE(
                f"Starting scraper: source={source}, category={category}, city={city}, pages={pages}, details={fetch_details}"
            )
        )

        total_scraped = 0

        # NoBroker scrapers
        if source in ('all', 'nobroker'):
            nb_tasks = []
            if category in ('all', 'rent'):
                nb_tasks.append(("NoBroker Rent", scrape_nobroker_rent))
            if category in ('all', 'sale'):
                nb_tasks.append(("NoBroker Sale", scrape_nobroker_sale))
            if category in ('all', 'comm_rent'):
                nb_tasks.append(("NoBroker Commercial Rent", scrape_nobroker_comm_rent))
            if category in ('all', 'comm_sale'):
                nb_tasks.append(("NoBroker Commercial Sale", scrape_nobroker_comm_sale))
            if category in ('all', 'pg'):
                nb_tasks.append(("NoBroker PG", scrape_nobroker_pg))

            for label, func in nb_tasks:
                self.stdout.write(f"Scraping {label} for {city} ({pages} page(s))...")
                try:
                    results = func(city=city, pages=pages, save_to_db=True, fetch_details=fetch_details)
                    count = len(results)
                    total_scraped += count
                    self.stdout.write(self.style.SUCCESS(f"  -> Saved {count} records for {label}."))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"  -> Failed to scrape {label}: {e}"))

        # MagicBricks scrapers
        if source in ('all', 'magicbricks'):
            mb_tasks = []
            if category in ('all', 'sale'):
                mb_tasks.append(("MagicBricks Residential Sale", scrape_magicbricks_sale))
            if category in ('all', 'rent'):
                mb_tasks.append(("MagicBricks Residential Rent", scrape_magicbricks_rent))
            if category in ('all', 'pg'):
                mb_tasks.append(("MagicBricks PG", scrape_magicbricks_pg))
            if category in ('all', 'comm_sale'):
                mb_tasks.append(("MagicBricks Commercial Sale", scrape_magicbricks_comm_sale))
            if category in ('all', 'comm_rent'):
                mb_tasks.append(("MagicBricks Commercial Lease", scrape_magicbricks_comm_lease))

            for label, func in mb_tasks:
                self.stdout.write(f"Scraping {label} for {city} ({pages} page(s))...")
                try:
                    results = func(city=city, pages=pages, save_to_db=True)
                    count = len(results)
                    total_scraped += count
                    self.stdout.write(self.style.SUCCESS(f"  -> Saved {count} records for {label}."))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"  -> Failed to scrape {label}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Scraping completed! Total records saved: {total_scraped}"))
