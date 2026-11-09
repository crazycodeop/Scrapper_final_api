import datetime
import logging
import nums_from_string
from bs4 import BeautifulSoup
from myapinew.models import (
    res_sale_model,
    res_rent_model,
    res_pg_model,
    comm_sale_model,
    comm_lease_model,
)
from .base import BaseScraper

logger = logging.getLogger(__name__)


def get_date_posted(ago_count):
    previous_date = datetime.datetime.today() - datetime.timedelta(days=ago_count)
    return previous_date.strftime('%d/%m/%Y')


def parse_posted_date(text):
    if not text:
        return ""
    text_lower = text.lower()
    try:
        if 'today' in text_lower:
            return get_date_posted(0)
        elif 'yesterday' in text_lower:
            return get_date_posted(1)
        elif 'ago' in text_lower:
            nums = nums_from_string.get_nums(text)
            if nums:
                count = int(nums[0])
                if 'week' in text_lower:
                    return get_date_posted(count * 7)
                elif 'month' in text_lower:
                    return get_date_posted(count * 30)
                else:
                    return get_date_posted(count)
        return text.replace('Posted: ', '').strip()
    except Exception:
        return text.strip()


class MagicBricksScraper(BaseScraper):
    def is_blocked(self, soup):
        if not soup:
            return True
        title = soup.find('title')
        if title and ("we'll be back soon" in title.get_text().lower() or "blocked" in title.get_text().lower()):
            return True
        return False

    def scrape_sale(self, city='Mumbai', pages=1, save_to_db=True):
        """Scrape residential sale properties from MagicBricks."""
        results = []
        base_url = (
            "https://www.magicbricks.com/property-for-sale/residential-real-estate"
            f"?bedroom=2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa"
            f"&cityName={city}&language=en"
        )

        for page in range(1, pages + 1):
            url = f"{base_url}&page={page}"
            soup = self.get_soup(url)
            if not soup:
                continue

            if self.is_blocked(soup):
                logger.warning(
                    f"MagicBricks returned bot protection shield ('We'll be back soon!') for {city} sale page {page}. "
                    "Skipping request."
                )
                break

            cards = soup.find_all('div', class_='mb-srp__card')
            logger.info(f"MagicBricks found {len(cards)} sale cards on page {page}")

            for card in cards:
                try:
                    posted_date = ""
                    post_el = card.find(class_="mb-srp__card__photo__fig--post")
                    if post_el:
                        posted_date = parse_posted_date(post_el.get_text())

                    link = ""
                    link_el = card.find('a', class_='mb-srp__card__society--name') or card.find('a', href=True)
                    if link_el and link_el.get('href'):
                        link = link_el['href']

                    owner = ""
                    owner_el = card.find('div', class_='mb-srp__card__ads--name')
                    if owner_el:
                        owner = self.clean_text(owner_el.get_text())

                    bhk = ""
                    locality = city
                    title_el = card.find('h2', class_='mb-srp__card--title')
                    if title_el:
                        title_text = self.clean_text(title_el.get_text())
                        parts = title_text.split(', ')
                        if parts:
                            bhk = parts[0][:5]
                            if len(parts) > 1:
                                locality = parts[1]

                    desc = ""
                    desc_el = card.find('div', class_='mb-srp__card--desc')
                    if desc_el:
                        p_el = desc_el.find('p')
                        if p_el:
                            desc = self.clean_text(p_el.get_text())

                    price = ""
                    price_el = card.find('div', class_='mb-srp__card__price--amount')
                    if price_el:
                        price = self.clean_currency(price_el.get_text())

                    per_sqft = ""
                    sqft_el = card.find('div', class_='mb-srp__card__price--size')
                    if sqft_el:
                        per_sqft = self.clean_currency(sqft_el.get_text())

                    facing = ""
                    carpet_area = ""
                    furnishing = ""
                    bathrooms = ""
                    status = ""
                    transaction = ""
                    floor = ""

                    summary_el = card.find('div', class_='mb-srp__card__summary__list')
                    if summary_el:
                        for elem in summary_el.children:
                            if not hasattr(elem, 'get'):
                                continue
                            summary_type = elem.get('data-summary', '')
                            text_val = self.clean_text(elem.get_text())
                            if summary_type == 'facing':
                                facing = text_val.replace('facing', '').strip()
                            elif summary_type == 'floor':
                                floor = text_val.replace('Floor', '').strip()
                            elif summary_type == 'carpet-area':
                                carpet_area = text_val.replace('Carpet Area', '').strip()
                            elif summary_type == 'furnishing':
                                furnishing = text_val.replace('Furnishing', '').strip()
                            elif summary_type == 'bathroom':
                                bathrooms = text_val.replace('Bathroom', '').strip()
                            elif summary_type == 'status':
                                status = text_val.replace('Status', '').strip()
                            elif summary_type == 'transaction':
                                transaction = text_val.replace('Transaction', '').strip()

                    data = {
                        'Date_Posted': posted_date,
                        'Proptype': 'sale',
                        'Link': link,
                        'Owner': owner,
                        'BHK': bhk,
                        'Locality': locality,
                        'City': city,
                        'Price': price,
                        'Carpet_Area': carpet_area,
                        'Furnishing': furnishing,
                        'Bathrooms': bathrooms,
                        'Facing': facing,
                        'Status': status,
                        'Transaction': transaction,
                        'Price_Sqft': per_sqft,
                        'Floor': floor,
                        'Description': desc,
                    }

                    if save_to_db:
                        obj = res_sale_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing MagicBricks sale card: {e}")

        return results

    def scrape_rent(self, city='Mumbai', pages=1, save_to_db=True):
        """Scrape residential rent properties from MagicBricks."""
        results = []
        base_url = (
            "https://www.magicbricks.com/property-for-rent/residential-real-estate"
            f"?bedroom=2,3&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa"
            f"&cityName={city}&language=en"
        )

        for page in range(1, pages + 1):
            url = f"{base_url}&page={page}"
            soup = self.get_soup(url)
            if not soup or self.is_blocked(soup):
                logger.warning(f"MagicBricks rent unavailable or protected for {city} page {page}.")
                break

            cards = soup.find_all('div', class_='mb-srp__card')
            for card in cards:
                try:
                    posted_date = ""
                    post_el = card.find(class_="mb-srp__card__photo__fig--post")
                    if post_el:
                        posted_date = parse_posted_date(post_el.get_text())

                    link = ""
                    link_el = card.find('a', class_='mb-srp__card__society--name') or card.find('a', href=True)
                    if link_el and link_el.get('href'):
                        link = link_el['href']

                    owner = ""
                    owner_el = card.find('div', class_='mb-srp__card__ads--name')
                    if owner_el:
                        owner = self.clean_text(owner_el.get_text())

                    bhk = ""
                    locality = city
                    title_el = card.find('h2', class_='mb-srp__card--title')
                    if title_el:
                        title_text = self.clean_text(title_el.get_text())
                        parts = title_text.split(', ')
                        if parts:
                            bhk = parts[0][:5]
                            if len(parts) > 1:
                                locality = parts[1]

                    desc = ""
                    desc_el = card.find('div', class_='mb-srp__card--desc')
                    if desc_el:
                        p_el = desc_el.find('p')
                        if p_el:
                            desc = self.clean_text(p_el.get_text())

                    rent = ""
                    rent_el = card.find('div', class_='mb-srp__card__price--amount')
                    if rent_el:
                        rent = self.clean_currency(rent_el.get_text())

                    facing = ""
                    carpet_area = ""
                    furnishing = ""
                    tenant = ""
                    floor = ""

                    summary_el = card.find('div', class_='mb-srp__card__summary__list')
                    if summary_el:
                        for elem in summary_el.children:
                            if not hasattr(elem, 'get'):
                                continue
                            summary_type = elem.get('data-summary', '')
                            text_val = self.clean_text(elem.get_text())
                            if summary_type == 'facing':
                                facing = text_val.replace('facing', '').strip()
                            elif summary_type == 'tenent-preffered':
                                tenant = text_val.replace('Tenant Preferred', '').strip()
                            elif summary_type == 'floor':
                                floor = text_val.replace('Floor', '').strip()
                            elif summary_type == 'carpet-area':
                                carpet_area = text_val.replace('Carpet Area', '').strip()
                            elif summary_type == 'furnishing':
                                furnishing = text_val.replace('Furnishing', '').strip()

                    data = {
                        'Date_Posted': posted_date,
                        'Proptype': 'rent',
                        'Link': link,
                        'Owner': owner,
                        'BHK': bhk,
                        'Locality': locality,
                        'City': city,
                        'Rent': rent,
                        'Carpet_Area': carpet_area,
                        'Furnishing': furnishing,
                        'Facing': facing,
                        'Tenant': tenant,
                        'Floor': floor,
                        'Description': desc,
                    }

                    if save_to_db:
                        obj = res_rent_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing MagicBricks rent card: {e}")

        return results

    def scrape_pg(self, city='Mumbai', pages=1, save_to_db=True):
        """Scrape PG listings from MagicBricks."""
        results = []
        url = f"https://www.magicbricks.com/property-for-rent/residential-paying-guest?cityName={city}"
        soup = self.get_soup(url)
        if not soup or self.is_blocked(soup):
            logger.warning(f"MagicBricks PG unavailable or protected for {city}.")
            return results

        cards = soup.find_all('div', class_='m-srp-card')
        for card in cards:
            try:
                pg_for = ""
                gender_el = card.find('span', class_='m-srp-card__info__gender')
                if gender_el:
                    pg_for = self.clean_text(gender_el.get_text())

                link = ""
                link_el = card.find(attrs={'itemprop': 'url'})
                if link_el and link_el.get('content'):
                    link = 'https://www.magicbricks.com/' + link_el['content'].lstrip('/')

                owner = ""
                owner_el = card.find('meta', attrs={'itemprop': 'name'})
                if owner_el and owner_el.get('content'):
                    owner = self.clean_text(owner_el['content'])

                desc = ""
                desc_el = card.find('meta', attrs={'itemprop': 'description'})
                if desc_el and desc_el.get('content'):
                    desc = self.clean_text(desc_el['content'])

                charges = ""
                price_el = card.find('div', class_='m-srp-card__price')
                if price_el:
                    charges = self.clean_currency(price_el.get_text())

                posted_by = ""
                locality = city
                temp = card.find('span', attrs={'class': 'hidden'})
                if temp:
                    posted_by = temp.get('data-advname', '')
                    locality = temp.get('data-pglocality', city)

                data = {
                    'Posted_by': posted_by,
                    'PG_for': pg_for,
                    'Proptype': 'PG',
                    'Link': link,
                    'Owner': owner,
                    'City': city,
                    'Locality': locality,
                    'Charges': charges,
                    'Description': desc,
                }

                if save_to_db:
                    obj = res_pg_model.objects.create(**data)
                    results.append(obj)
                else:
                    results.append(data)

            except Exception as e:
                logger.warning(f"Error parsing MagicBricks PG card: {e}")

        return results

    def scrape_comm_sale(self, city='Mumbai', pages=1, save_to_db=True):
        """Scrape commercial sale listings from MagicBricks."""
        results = []
        base_url = (
            "https://www.magicbricks.com/property-for-sale/commercial-real-estate"
            f"?proptype=Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom"
            f"&cityName={city}&language=en"
        )

        for page in range(1, pages + 1):
            url = f"{base_url}&page={page}"
            soup = self.get_soup(url)
            if not soup or self.is_blocked(soup):
                logger.warning(f"MagicBricks commercial sale unavailable or protected for {city}.")
                break

            cards = soup.find_all('div', class_='mb-srp__card')
            for card in cards:
                try:
                    posted_date = ""
                    post_el = card.find(class_="mb-srp__card__photo__fig--post")
                    if post_el:
                        posted_date = parse_posted_date(post_el.get_text())

                    link = ""
                    link_el = card.find('a', class_='mb-srp__card__society--name') or card.find('a', href=True)
                    if link_el and link_el.get('href'):
                        link = link_el['href']

                    owner = ""
                    owner_el = card.find('div', class_='mb-srp__card__ads--name')
                    if owner_el:
                        owner = self.clean_text(owner_el.get_text())

                    locality = city
                    title_el = card.find('h2', class_='mb-srp__card--title')
                    if title_el:
                        title_text = self.clean_text(title_el.get_text())
                        parts = title_text.split(', ')
                        if len(parts) > 1:
                            locality = parts[1]

                    desc = ""
                    desc_el = card.find('div', class_='mb-srp__card--desc')
                    if desc_el:
                        p_el = desc_el.find('p')
                        if p_el:
                            desc = self.clean_text(p_el.get_text())

                    price = ""
                    price_el = card.find('div', class_='mb-srp__card__price--amount')
                    if price_el:
                        price = self.clean_currency(price_el.get_text())

                    carpet_area = ""
                    facing = ""
                    prop_age = ""
                    water = ""
                    parking = ""
                    pantry = ""
                    overlooking = ""

                    for elem in card.find_all('div', class_='mb-srp__card__summary-commercial__list--item'):
                        text_val = self.clean_text(elem.get_text())
                        if 'Carpet Area' in text_val:
                            carpet_area = text_val.replace('Carpet Area', '').strip()
                        elif 'Overlooking' in text_val:
                            overlooking = text_val.replace('Overlooking', '').strip()
                        elif 'Parking' in text_val:
                            parking = text_val.replace('Parking', '').strip()
                        elif 'Pantry' in text_val:
                            pantry = text_val.replace('Pantry', '').strip()
                        elif 'Facing' in text_val:
                            facing = text_val.replace('Facing', '').strip()
                        elif 'Water Availability' in text_val:
                            water = text_val.replace('Water Availability', '').strip()
                        elif 'Property Age' in text_val:
                            prop_age = text_val.replace('Property Age', '').strip()

                    data = {
                        'Date_Posted': posted_date,
                        'Proptype': 'Commercial Sale',
                        'Link': link,
                        'Owner': owner,
                        'Locality': locality,
                        'City': city,
                        'Price': price,
                        'Carpet_Area': carpet_area,
                        'Facing': facing,
                        'Property_Age': prop_age,
                        'Water_Availability': water,
                        'Parking': parking,
                        'Pantry': pantry,
                        'Overlooking': overlooking,
                        'Description': desc,
                    }

                    if save_to_db:
                        obj = comm_sale_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing MagicBricks commercial sale card: {e}")

        return results

    def scrape_comm_lease(self, city='Mumbai', pages=1, save_to_db=True):
        """Scrape commercial lease listings from MagicBricks."""
        results = []
        base_url = (
            "https://www.magicbricks.com/property-for-rent/commercial-real-estate"
            f"?proptype=Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom"
            f"&cityName={city}&language=en"
        )

        for page in range(1, pages + 1):
            url = f"{base_url}&page={page}"
            soup = self.get_soup(url)
            if not soup or self.is_blocked(soup):
                logger.warning(f"MagicBricks commercial lease unavailable or protected for {city}.")
                break

            cards = soup.find_all('div', class_='mb-srp__card')
            for card in cards:
                try:
                    posted_date = ""
                    post_el = card.find(class_="mb-srp__card__photo__fig--post")
                    if post_el:
                        posted_date = parse_posted_date(post_el.get_text())

                    link = ""
                    link_el = card.find('a', class_='mb-srp__card__society--name') or card.find('a', href=True)
                    if link_el and link_el.get('href'):
                        link = link_el['href']

                    retailer = ""
                    owner_el = card.find('div', class_='mb-srp__card__ads--name')
                    if owner_el:
                        retailer = self.clean_text(owner_el.get_text())

                    bhk = ""
                    locality = city
                    title_el = card.find('h2', class_='mb-srp__card--title')
                    if title_el:
                        title_text = self.clean_text(title_el.get_text())
                        parts = title_text.split(', ')
                        if parts:
                            bhk = parts[0][:5]
                            if len(parts) > 1:
                                locality = parts[1]

                    desc = ""
                    desc_el = card.find('div', class_='mb-srp__card--desc')
                    if desc_el:
                        p_el = desc_el.find('p')
                        if p_el:
                            desc = self.clean_text(p_el.get_text())

                    price = ""
                    price_el = card.find('div', class_='mb-srp__card__price--amount')
                    if price_el:
                        price = self.clean_currency(price_el.get_text())

                    per_sqft = ""
                    sqft_el = card.find('div', class_='mb-srp__card__price--size')
                    if sqft_el:
                        per_sqft = self.clean_currency(sqft_el.get_text())

                    carpet_area = ""
                    washroom = ""
                    facing = ""
                    water = ""
                    prop_age = ""
                    parking = ""
                    pantry = ""

                    for elem in card.find_all('div', class_='mb-srp__card__summary-commercial__list--item'):
                        text_val = self.clean_text(elem.get_text())
                        if 'Carpet Area' in text_val:
                            carpet_area = text_val.replace('Carpet Area', '').strip()
                        elif 'Washroom' in text_val:
                            washroom = text_val.replace('Washroom', '').strip()
                        elif 'Facing' in text_val:
                            facing = text_val.replace('Facing', '').strip()
                        elif 'Water Availability' in text_val:
                            water = text_val.replace('Water Availability', '').strip()
                        elif 'Property Age' in text_val:
                            prop_age = text_val.replace('Property Age', '').strip()
                        elif 'Parking' in text_val:
                            parking = text_val.replace('Parking', '').strip()
                        elif 'Pantry' in text_val:
                            pantry = text_val.replace('Pantry', '').strip()

                    data = {
                        'Date_Posted': posted_date,
                        'Proptype': 'Commercial Lease',
                        'Link': link,
                        'Retailer': retailer,
                        'BHK': bhk,
                        'Locality': locality,
                        'City': city,
                        'Price': price,
                        'Carpet_Area': carpet_area,
                        'Washroom': washroom,
                        'Facing': facing,
                        'Water_Availability': water,
                        'Property_Age': prop_age,
                        'Price_Sqft': per_sqft,
                        'Parking': parking,
                        'Pantry': pantry,
                        'Description': desc,
                    }

                    if save_to_db:
                        obj = comm_lease_model.objects.create(**data)
                        results.append(obj)
                    else:
                        results.append(data)

                except Exception as e:
                    logger.warning(f"Error parsing MagicBricks commercial lease card: {e}")

        return results


# Module helper functions
_default_magicbricks_scraper = MagicBricksScraper()


def scrape_magicbricks_sale(city='Mumbai', pages=1, save_to_db=True):
    return _default_magicbricks_scraper.scrape_sale(city, pages, save_to_db)


def scrape_magicbricks_rent(city='Mumbai', pages=1, save_to_db=True):
    return _default_magicbricks_scraper.scrape_rent(city, pages, save_to_db)


def scrape_magicbricks_pg(city='Mumbai', pages=1, save_to_db=True):
    return _default_magicbricks_scraper.scrape_pg(city, pages, save_to_db)


def scrape_magicbricks_comm_sale(city='Mumbai', pages=1, save_to_db=True):
    return _default_magicbricks_scraper.scrape_comm_sale(city, pages, save_to_db)


def scrape_magicbricks_comm_lease(city='Mumbai', pages=1, save_to_db=True):
    return _default_magicbricks_scraper.scrape_comm_lease(city, pages, save_to_db)
