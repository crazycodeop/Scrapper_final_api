import logging
import re
import time
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
}


class BaseScraper:
    def __init__(self, timeout=12, delay=1.0):
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)

    def get_soup(self, url):
        """Fetch URL and return BeautifulSoup object or None on failure."""
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code != 200:
                logger.warning(f"Request to {url} returned status code {response.status_code}")
                return None
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    @staticmethod
    def clean_text(val):
        """Clean string text, replace non-breaking spaces, strip whitespace."""
        if not val:
            return ""
        # Remove currency symbol and strip
        val = str(val).replace('\u20b9', '').replace('₹', '').replace('\xa0', ' ')
        val = re.sub(r'\s+', ' ', val)
        return val.strip()

    @staticmethod
    def clean_currency(val):
        """Remove symbols and clean currency string."""
        if not val:
            return ""
        return BaseScraper.clean_text(val).replace(',', '')
