# Scrapper Final API

A robust Django REST Framework (DRF) backend and web scraping engine for real estate properties across residential sales, residential rentals, commercial sales, commercial leases, and PG/hostels (supporting NoBroker and MagicBricks).

---

## 🚀 Key Improvements & Architecture Refactor

1. **Decoupled Scraping from Request/Module Lifecycle**:
   - *Previous state*: Web scraping functions executed during module import inside ViewSet class definitions, blocking server startup and command execution on heavy synchronous HTTP loops.
   - *Refactored*: Scrapers are fully decoupled into modular classes under `myapinew/scrapers/`, executable via CLI management commands (`python manage.py scrape`) or via an on-demand API trigger (`POST /scrape/`).

2. **Clean Database Models**:
   - `models.AutoField` primary keys replace manual index collision risks.
   - Optional fields configured with `null=True, blank=True` to gracefully handle varying listing attributes.
   - Fixed all broken `__str__` methods that referenced non-existent model attributes (`AttributeError`).
   - Added descriptive model metadata (`verbose_name` and `verbose_name_plural`) for Django Admin.

3. **RESTful API & Serializers**:
   - Refactored serializers to standard DRF `ModelSerializer` with `fields = '__all__'`.
   - Enabled built-in pagination (`PageNumberPagination`, 20 items per page).
   - Added `SearchFilter` and `OrderingFilter` support across endpoints (e.g., search by locality, apartment type, furnishing, or city).

4. **Resilient Scraper Engine**:
   - Configured realistic modern browser headers and session pooling (`requests.Session`).
   - Handled anti-bot / maintenance shields (e.g. MagicBricks Akamai defense) gracefully with logged warnings rather than process crashes.
   - Added safe parsing and string sanitization utilities in `BaseScraper`.

5. **Project Hygiene**:
   - Added `.gitignore` to prevent tracking `db.sqlite3` and `__pycache__` binaries.
   - Added `requirements.txt` with tested dependencies.
   - Added automated unit test suite with 100% test pass rate (`python manage.py test`).

---

## 📦 Setup & Installation

### 1. Clone & Navigate to Project
```bash
git clone https://github.com/crazycodeop/Scrapper_final_api.git
cd Scrapper_final_api
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations
```bash
python manage.py migrate
```

---

## 🛠️ Usage

### Running the Development Server
```bash
python manage.py runserver
```
Visit the browsable API at `http://127.0.0.1:8000/`.

---

### Running the Scraper CLI Command

Scrape real-time properties and store them directly into the database:

```bash
# Scrape all NoBroker categories for Mumbai (1 page each)
python manage.py scrape --source nobroker --category all --city mumbai --pages 1

# Scrape only rental properties from NoBroker for 2 pages
python manage.py scrape --source nobroker --category rent --city mumbai --pages 2

# Scrape residential sales from MagicBricks
python manage.py scrape --source magicbricks --category sale --city Mumbai --pages 1

# Optional flag: fetch individual detail pages for extra metadata (slower)
python manage.py scrape --source nobroker --category rent --pages 1 --details
```

**CLI Arguments:**
- `--source`: `nobroker`, `magicbricks`, or `all` (default: `nobroker`)
- `--category`: `rent`, `sale`, `comm_rent`, `comm_sale`, `pg`, or `all` (default: `all`)
- `--city`: target city name (default: `mumbai`)
- `--pages`: number of pages to scrape (default: `1`)
- `--details`: flag to fetch individual listing detail pages for deeper fields

---

### On-Demand Scraping via REST API

Trigger scraping over HTTP by making a POST request to `/scrape/`:

**Request:**
```http
POST /scrape/
Content-Type: application/json

{
  "source": "nobroker",
  "category": "rent",
  "city": "mumbai",
  "pages": 1,
  "details": false
}
```

**Response:**
```json
{
  "status": "completed",
  "total_scraped": 26,
  "city": "mumbai",
  "pages": 1,
  "results": {
    "nobroker": {
      "rent": {
        "status": "success",
        "count": 26
      }
    }
  }
}
```

---

## 🌐 REST API Endpoints

All endpoints support pagination, search, and ordering queries.

| Endpoint | Description | Query Example |
| :--- | :--- | :--- |
| `GET /nobrokerRent/` | NoBroker residential rental listings | `?search=Malad&ordering=-Id` |
| `GET /nobrokerSale/` | NoBroker residential sale listings | `?search=Andheri` |
| `GET /noBrokerCommRent/` | NoBroker commercial rental listings | `?search=Office` |
| `GET /noBrokerCommSale/` | NoBroker commercial sale listings | `?search=Shop` |
| `GET /noBrokerPg/` | NoBroker PG & hostel listings | `?search=Single` |
| `GET /res_sale_model/` | MagicBricks residential sale listings | `?search=Bandra` |
| `GET /res_rent_model/` | MagicBricks residential rent listings | `?search=2+BHK` |
| `GET /res_pg_model/` | MagicBricks PG listings | `?search=Powai` |
| `GET /comm_sale_model/` | MagicBricks commercial sale listings | `?search=BKC` |
| `GET /comm_lease_model/` | MagicBricks commercial lease listings | `?search=Retail` |
| `GET, POST /scrape/` | On-demand scraper trigger endpoint | - |

---

## 🧪 Running Tests

Execute the automated test suite with:

```bash
python manage.py test
```
