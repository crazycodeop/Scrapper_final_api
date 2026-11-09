import logging
from bs4 import BeautifulSoup
from myapinew.models import (
    no_broker_rent_model,
    no_broker_sale_model,
    no_broker_comm_rent_model,
    no_broker_comm_sale_model,
    no_broker_pg_model,
)
from .base import BaseScraper

logger = logging.getLogger(__name__)


class NoBrokerScraper(BaseScraper):
    def get_card_elements(self, soup):
        """Extract property card containers and links from search page."""
        cards = []
        seen_links = set()
        for a in soup.find_all('a', href=lambda x: x and ('/property/' in x or '/pg/' in x)):
            href = a['href']
            if href in seen_links:
                continue
            seen_links.add(href)
            parent = a.find_parent('div', class_='bg-white')
            if parent and parent not in [c[1] for c in cards]:
                cards.append((href, parent))
        return cards

    def _extract_id_text(self, card, elem_id):
        elem = card.find(attrs={'id': elem_id})
        if not elem:
            return ""
        sb = elem.find(class_=lambda c: c and 'font-semi-bold' in c)
        if sb:
            return self.clean_text(sb.get_text())
        return self.clean_text(elem.get_text())

    def scrape_rent(self, city='mumbai', pages=1, save_to_db=True, fetch_details=False):
        """Scrape residential rent properties from NoBroker."""
        results = []
        city_lower = city.lower()

        for page in range(1, pages + 1):
            url = f"https://www.nobroker.in/flats-for-rent-in-{city_lower}_{city_lower}"
            if page > 1:
                url += f"-page-{page}"

            soup = self.get_soup(url)
            if not soup:
                continue

            card_items = self.get_card_elements(soup)
            logger.info(f"Found {len(card_items)} rent cards on page {page}")

            for link, card in card_items:
                try:
                    if not link.startswith('http'):
                        link = 'https://www.nobroker.in' + link

                    feats = [self.clean_text(el.get_text()) for el in card.find_all('div', class_='font-semibold')]
                    rent = feats[0] if len(feats) > 0 else ""
                    deposit = feats[2] if len(feats) > 2 else ""
                    sqft = feats[3] if len(feats) > 3 else ""
                    furnishing = feats[4] if len(feats) > 4 else ""
                    apt_type = feats[5] if len(feats) > 5 else "Apartment"
                    tenants = feats[6] if len(feats) > 6 else ""
                    avail = feats[7] if len(feats) > 7 else ""

                    nearby_elem = card.find('div', class_=lambda c: c and ('mt-0.5p' in c or 'mt-[2px]' in c)) or card.find('h2')
                    nearby = self.clean_text(nearby_elem.get_text()) if nearby_elem else city

                    bedrooms = apt_type
                    prop_type = "Apartment"
                    parking = ""
                    posted_on = ""
                    possession = avail
                    balcony = ""

                    if fetch_details:
                        detail_soup = self.get_soup(link)
                        if detail_soup:
                            b_elem = detail_soup.find('h4', id='details-summary-typeDesc')
                            if b_elem:
                                bedrooms = self.clean_text(b_elem.get_text())
                            p_elem = detail_soup.find('h4', id='details-summary-buildingType')
                            if p_elem:
                                prop_type = self.clean_text(p_elem.get_text())
                            pk_elem = detail_soup.find('h4', id='details-summary-parkingDesc')
                            if pk_elem:
                                parking = self.clean_text(pk_elem.get_text())
                            post_elem = detail_soup.find('h4', id='details-summary-lastUpdateDate')
                            if post_elem:
                                posted_on = self.clean_text(post_elem.get_text())
                            pos_elem = detail_soup.find('h4', id='details-summary-availableFrom')
                            if pos_elem:
                                possession = self.clean_text(pos_elem.get_text())
                            balc_elem = detail_soup.find('h4', id='details-summary-balconies')
                            if balc_elem:
                                balcony = self.clean_text(balc_elem.get_text())

                    data = {
                        'Date_Posted': posted_on,
                        'Link': link,
                        'Rent': rent,
                        'EMI': deposit,
                        'Nearby': nearby,
                        'SQFT': sqft,
                        'Furnishing': furnishing,
                        'Available_from': avail,
                        'Prop_Type': prop_type,
                        'Preferred_Tenants': tenants,
                        'Apt_Type': apt_type,
                        'Parking': parking,
                        'Bedrooms': bedrooms,
                        'Possesion_By': possession,
                        'Balcony': balcony,
                    }

                    if save_to_db:
                        obj = no_broker_rent_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing rent card: {e}")

        return results

    def scrape_sale(self, city='mumbai', pages=1, save_to_db=True, fetch_details=False):
        """Scrape residential sale properties from NoBroker."""
        results = []
        city_lower = city.lower()

        for page in range(1, pages + 1):
            url = f"https://www.nobroker.in/flats-for-sale-in-{city_lower}_{city_lower}"
            if page > 1:
                url += f"-page-{page}"

            soup = self.get_soup(url)
            if not soup:
                continue

            card_items = self.get_card_elements(soup)
            logger.info(f"Found {len(card_items)} sale cards on page {page}")

            for link, card in card_items:
                try:
                    if not link.startswith('http'):
                        link = 'https://www.nobroker.in' + link

                    price = self._extract_id_text(card, 'minDeposit')
                    emi = self._extract_id_text(card, 'roomType')
                    sqft = self._extract_id_text(card, 'minRent') or self._extract_id_text(card, 'unitCode')

                    feats = [self.clean_text(el.get_text()) for el in card.find_all('div', class_='font-semibold')]
                    facing = feats[0] if len(feats) > 0 else ""
                    apt_type = feats[1] if len(feats) > 1 else ""
                    bathrooms = feats[2] if len(feats) > 2 else ""
                    parking = feats[3] if len(feats) > 3 else ""

                    nearby_elem = card.find('div', class_=lambda c: c and ('mt-0.5p' in c or 'mt-[2px]' in c)) or card.find('h2')
                    nearby = self.clean_text(nearby_elem.get_text()) if nearby_elem else city
                    apt_name = nearby

                    bedrooms = apt_type
                    posted_on = ""
                    possession = ""
                    balcony = ""
                    power_backup = ""

                    if fetch_details:
                        detail_soup = self.get_soup(link)
                        if detail_soup:
                            b_elem = detail_soup.find('h4', id='details-summary-typeDesc')
                            if b_elem:
                                bedrooms = self.clean_text(b_elem.get_text())
                            post_elem = detail_soup.find('h4', id='details-summary-lastUpdateDate')
                            if post_elem:
                                posted_on = self.clean_text(post_elem.get_text())
                            pos_elem = detail_soup.find('h4', id='details-summary-availableFrom')
                            if pos_elem:
                                possession = self.clean_text(pos_elem.get_text())
                            balc_elem = detail_soup.find('h4', id='details-summary-balconies')
                            if balc_elem:
                                balcony = self.clean_text(balc_elem.get_text())
                            soc_elem = detail_soup.find('h4', id='details-summary-society')
                            if soc_elem:
                                apt_name = self.clean_text(soc_elem.get_text())
                            pb_elem = detail_soup.find('h4', id='details-summary-powerBackup')
                            if pb_elem:
                                power_backup = self.clean_text(pb_elem.get_text())

                    data = {
                        'Date_Posted': posted_on,
                        'Link': link,
                        'Price': price,
                        'EMI': emi,
                        'Nearby': nearby,
                        'SQFT': sqft,
                        'Facing': facing,
                        'Bathrooms': bathrooms,
                        'Apt_Type': apt_type,
                        'Apt_Name': apt_name,
                        'Parking': parking,
                        'Bedrooms': bedrooms,
                        'Possesion_By': possession,
                        'Balcony': balcony,
                        'Power_Backup': power_backup,
                    }

                    if save_to_db:
                        obj = no_broker_sale_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing sale card: {e}")

        return results

    def scrape_comm_rent(self, city='mumbai', pages=1, save_to_db=True, fetch_details=False):
        """Scrape commercial rent properties from NoBroker."""
        results = []
        city_lower = city.lower()

        for page in range(1, pages + 1):
            url = f"https://www.nobroker.in/commercial-properties-for-rent-in-{city_lower}_{city_lower}"
            if page > 1:
                url += f"-page-{page}"

            soup = self.get_soup(url)
            if not soup:
                continue

            card_items = self.get_card_elements(soup)
            logger.info(f"Found {len(card_items)} commercial rent cards on page {page}")

            for link, card in card_items:
                try:
                    if not link.startswith('http'):
                        link = 'https://www.nobroker.in' + link

                    rent = self._extract_id_text(card, 'minimumRent') or self._extract_id_text(card, 'minDeposit')
                    deposit = self._extract_id_text(card, 'roomType')
                    sqft = self._extract_id_text(card, 'minRent') or self._extract_id_text(card, 'unitCode')

                    feats = [self.clean_text(el.get_text()) for el in card.find_all('div', class_='font-semibold')]
                    prop_type = feats[0] if len(feats) > 0 else "Commercial"
                    parking = feats[1] if len(feats) > 1 else ""
                    furnishing = feats[2] if len(feats) > 2 else ""
                    avail = feats[3] if len(feats) > 3 else ""

                    nearby_elem = card.find('div', class_=lambda c: c and ('mt-0.5p' in c or 'mt-[2px]' in c)) or card.find('h2')
                    nearby = self.clean_text(nearby_elem.get_text()) if nearby_elem else city

                    floor = ""
                    posted_on = ""

                    if fetch_details:
                        detail_soup = self.get_soup(link)
                        if detail_soup:
                            fl_elem = detail_soup.find('h4', id='details-summary-floor')
                            if fl_elem:
                                floor = self.clean_text(fl_elem.get_text())
                            post_elem = detail_soup.find('h4', id='details-summary-activationDate')
                            if post_elem:
                                posted_on = self.clean_text(post_elem.get_text())

                    data = {
                        'Date_Posted': posted_on,
                        'Link': link,
                        'Rent': rent,
                        'Deposit': deposit,
                        'Nearby': nearby,
                        'SQFT': sqft,
                        'Floor': floor,
                        'Prop_Type': prop_type,
                        'Furnishing': furnishing,
                        'Availability': avail,
                        'Parking': parking,
                    }

                    if save_to_db:
                        obj = no_broker_comm_rent_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing commercial rent card: {e}")

        return results

    def scrape_comm_sale(self, city='mumbai', pages=1, save_to_db=True, fetch_details=False):
        """Scrape commercial sale properties from NoBroker."""
        results = []
        city_lower = city.lower()

        for page in range(1, pages + 1):
            url = f"https://www.nobroker.in/commercial-properties-for-sale-in-{city_lower}_{city_lower}"
            if page > 1:
                url += f"-page-{page}"

            soup = self.get_soup(url)
            if not soup:
                continue

            card_items = self.get_card_elements(soup)
            logger.info(f"Found {len(card_items)} commercial sale cards on page {page}")

            for link, card in card_items:
                try:
                    if not link.startswith('http'):
                        link = 'https://www.nobroker.in' + link

                    price = self._extract_id_text(card, 'minDeposit')
                    emi = self._extract_id_text(card, 'roomType')
                    sqft = self._extract_id_text(card, 'minRent') or self._extract_id_text(card, 'unitCode')

                    feats = [self.clean_text(el.get_text()) for el in card.find_all('div', class_='font-semibold')]
                    prop_type = feats[0] if len(feats) > 0 else "Commercial Sale"
                    parking = feats[1] if len(feats) > 1 else ""
                    furnishing = feats[2] if len(feats) > 2 else ""
                    avail = feats[3] if len(feats) > 3 else ""

                    nearby_elem = card.find('div', class_=lambda c: c and ('mt-0.5p' in c or 'mt-[2px]' in c)) or card.find('h2')
                    nearby = self.clean_text(nearby_elem.get_text()) if nearby_elem else city

                    posted_on = ""
                    facing = ""
                    bathrooms = ""

                    if fetch_details:
                        detail_soup = self.get_soup(link)
                        if detail_soup:
                            post_elem = detail_soup.find('h4', id='details-summary-availableFrom')
                            if post_elem:
                                posted_on = self.clean_text(post_elem.get_text())

                    data = {
                        'Date_Posted': posted_on,
                        'Link': link,
                        'Price': price,
                        'EMI': emi,
                        'Nearby': nearby,
                        'SQFT': sqft,
                        'Facing': facing,
                        'Bathrooms': bathrooms,
                        'Apt_Type': prop_type,
                        'Parking': parking,
                    }

                    if save_to_db:
                        obj = no_broker_comm_sale_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing commercial sale card: {e}")

        return results

    def scrape_pg(self, city='mumbai', pages=1, save_to_db=True, fetch_details=False):
        """Scrape PG/Hostel properties from NoBroker."""
        results = []
        city_lower = city.lower()

        for page in range(1, pages + 1):
            url = f"https://www.nobroker.in/pg-in-{city_lower}_{city_lower}"
            if page > 1:
                url += f"-page-{page}"

            soup = self.get_soup(url)
            if not soup:
                continue

            card_items = self.get_card_elements(soup)
            logger.info(f"Found {len(card_items)} PG cards on page {page}")

            for link, card in card_items:
                try:
                    if not link.startswith('http'):
                        link = 'https://www.nobroker.in' + link

                    deposit = self._extract_id_text(card, 'minDeposit')
                    room_type = self._extract_id_text(card, 'roomType') or "PG Room"
                    rent = self._extract_id_text(card, 'minRent') or self._extract_id_text(card, 'unitCode')

                    feats = [self.clean_text(el.get_text()) for el in card.find_all('div', class_='font-semibold')]
                    tenants = feats[0] if len(feats) > 0 else ""
                    posted_on = feats[1] if len(feats) > 1 else ""
                    food = feats[2] if len(feats) > 2 else ""
                    parking = feats[3] if len(feats) > 3 else ""

                    nearby_elem = card.find('div', class_=lambda c: c and ('mt-0.5p' in c or 'mt-[2px]' in c)) or card.find('h2')
                    nearby = self.clean_text(nearby_elem.get_text()) if nearby_elem else city
                    possession = ""

                    if fetch_details:
                        detail_soup = self.get_soup(link)
                        if detail_soup:
                            pk_elem = detail_soup.find('h4', id='details-summary-parkingDesc')
                            if pk_elem:
                                parking = self.clean_text(pk_elem.get_text())
                            pos_elem = detail_soup.find('h4', id='details-summary-availableFrom')
                            if pos_elem:
                                possession = self.clean_text(pos_elem.get_text())

                    data = {
                        'Date_Posted': posted_on,
                        'Link': link,
                        'Rent': rent,
                        'Deposit': deposit,
                        'Nearby': nearby,
                        'Room_Type': room_type,
                        'Preferred_Tenants': tenants,
                        'Food': food,
                        'Parking': parking,
                        'Possesion_By': possession,
                    }

                    if save_to_db:
                        obj = no_broker_pg_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing PG card: {e}")

        return results


# Module helper functions
_default_nobroker_scraper = NoBrokerScraper()


def scrape_nobroker_rent(city='mumbai', pages=1, save_to_db=True, fetch_details=False):
    return _default_nobroker_scraper.scrape_rent(city, pages, save_to_db, fetch_details)


def scrape_nobroker_sale(city='mumbai', pages=1, save_to_db=True, fetch_details=False):
    return _default_nobroker_scraper.scrape_sale(city, pages, save_to_db, fetch_details)


def scrape_nobroker_comm_rent(city='mumbai', pages=1, save_to_db=True, fetch_details=False):
    return _default_nobroker_scraper.scrape_comm_rent(city, pages, save_to_db, fetch_details)


def scrape_nobroker_comm_sale(city='mumbai', pages=1, save_to_db=True, fetch_details=False):
    return _default_nobroker_scraper.scrape_comm_sale(city, pages, save_to_db, fetch_details)


def scrape_nobroker_pg(city='mumbai', pages=1, save_to_db=True, fetch_details=False):
    return _default_nobroker_scraper.scrape_pg(city, pages, save_to_db, fetch_details)
