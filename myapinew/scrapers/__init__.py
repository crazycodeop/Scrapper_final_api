"""Scrapers module for MagicBricks and NoBroker."""
from .nobroker import (
    scrape_nobroker_rent,
    scrape_nobroker_sale,
    scrape_nobroker_comm_rent,
    scrape_nobroker_comm_sale,
    scrape_nobroker_pg,
)
from .magicbricks import (
    scrape_magicbricks_sale,
    scrape_magicbricks_rent,
    scrape_magicbricks_pg,
    scrape_magicbricks_comm_sale,
    scrape_magicbricks_comm_lease,
)

__all__ = [
    'scrape_nobroker_rent',
    'scrape_nobroker_sale',
    'scrape_nobroker_comm_rent',
    'scrape_nobroker_comm_sale',
    'scrape_nobroker_pg',
    'scrape_magicbricks_sale',
    'scrape_magicbricks_rent',
    'scrape_magicbricks_pg',
    'scrape_magicbricks_comm_sale',
    'scrape_magicbricks_comm_lease',
]
