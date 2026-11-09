import logging
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response

from myapinew.models import (
    res_sale_model,
    res_rent_model,
    res_pg_model,
    comm_sale_model,
    comm_lease_model,
    no_broker_rent_model,
    no_broker_sale_model,
    no_broker_comm_rent_model,
    no_broker_comm_sale_model,
    no_broker_pg_model,
)
from myapinew.serializers import (
    resSaleSerializer,
    resRentSerializer,
    resPgSerializer,
    commSaleSerializer,
    commLeaseSerializer,
    noBrokerRentSerializer,
    noBrokerSaleSerializer,
    noBrokerCommRentSerializer,
    noBrokerCommSaleSerializer,
    noBrokerPgSerializer,
)
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


# -------------------------------------------------------------------------
# MagicBricks ViewSets
# -------------------------------------------------------------------------

class resSaleViewSet(viewsets.ModelViewSet):
    """API endpoint for MagicBricks residential properties for sale."""
    queryset = res_sale_model.objects.all().order_by('-Id')
    serializer_class = resSaleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['City', 'Locality', 'BHK', 'Owner', 'Description']
    ordering_fields = '__all__'


class resRentViewSet(viewsets.ModelViewSet):
    """API endpoint for MagicBricks residential properties for rent."""
    queryset = res_rent_model.objects.all().order_by('-Id')
    serializer_class = resRentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['City', 'Locality', 'BHK', 'Owner', 'Description']
    ordering_fields = '__all__'


class resPgViewSet(viewsets.ModelViewSet):
    """API endpoint for MagicBricks PG listings."""
    queryset = res_pg_model.objects.all().order_by('-Id')
    serializer_class = resPgSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['City', 'Locality', 'Owner', 'PG_for', 'Description']
    ordering_fields = '__all__'


class commSaleViewSet(viewsets.ModelViewSet):
    """API endpoint for MagicBricks commercial properties for sale."""
    queryset = comm_sale_model.objects.all().order_by('-Id')
    serializer_class = commSaleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['City', 'Locality', 'Owner', 'Proptype', 'Description']
    ordering_fields = '__all__'


class commLeaseViewSet(viewsets.ModelViewSet):
    """API endpoint for MagicBricks commercial properties for lease."""
    queryset = comm_lease_model.objects.all().order_by('-Id')
    serializer_class = commLeaseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['City', 'Locality', 'Retailer', 'BHK', 'Description']
    ordering_fields = '__all__'


# -------------------------------------------------------------------------
# NoBroker ViewSets
# -------------------------------------------------------------------------

class noBrokerRent(viewsets.ModelViewSet):
    """API endpoint for NoBroker residential properties for rent."""
    queryset = no_broker_rent_model.objects.all().order_by('-Id')
    serializer_class = noBrokerRentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Nearby', 'Apt_Type', 'Furnishing', 'Preferred_Tenants']
    ordering_fields = '__all__'


class noBrokerSale(viewsets.ModelViewSet):
    """API endpoint for NoBroker residential properties for sale."""
    queryset = no_broker_sale_model.objects.all().order_by('-Id')
    serializer_class = noBrokerSaleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Nearby', 'Apt_Type', 'Apt_Name', 'Facing']
    ordering_fields = '__all__'


class noBrokerCommRent(viewsets.ModelViewSet):
    """API endpoint for NoBroker commercial properties for rent."""
    queryset = no_broker_comm_rent_model.objects.all().order_by('-Id')
    serializer_class = noBrokerCommRentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Nearby', 'Prop_Type', 'Furnishing', 'Floor']
    ordering_fields = '__all__'


class noBrokerCommSale(viewsets.ModelViewSet):
    """API endpoint for NoBroker commercial properties for sale."""
    queryset = no_broker_comm_sale_model.objects.all().order_by('-Id')
    serializer_class = noBrokerCommSaleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Nearby', 'Apt_Type', 'Facing']
    ordering_fields = '__all__'


class noBrokerPg(viewsets.ModelViewSet):
    """API endpoint for NoBroker PG/hostel properties."""
    queryset = no_broker_pg_model.objects.all().order_by('-Id')
    serializer_class = noBrokerPgSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['Nearby', 'Room_Type', 'Preferred_Tenants', 'Food']
    ordering_fields = '__all__'


# -------------------------------------------------------------------------
# On-demand Scraper Trigger API View
# -------------------------------------------------------------------------

class ScrapeTriggerAPIView(APIView):
    """
    Trigger real-time web scraping for NoBroker or MagicBricks.
    Accepts POST with JSON payload:
    {
        "source": "nobroker" | "magicbricks" | "all",
        "category": "rent" | "sale" | "comm_rent" | "comm_sale" | "pg" | "all",
        "city": "mumbai",
        "pages": 1,
        "details": false
    }
    """

    SCRAPER_MAP = {
        'nobroker': {
            'rent': scrape_nobroker_rent,
            'sale': scrape_nobroker_sale,
            'comm_rent': scrape_nobroker_comm_rent,
            'comm_sale': scrape_nobroker_comm_sale,
            'pg': scrape_nobroker_pg,
        },
        'magicbricks': {
            'rent': scrape_magicbricks_rent,
            'sale': scrape_magicbricks_sale,
            'comm_rent': scrape_magicbricks_comm_lease,
            'comm_sale': scrape_magicbricks_comm_sale,
            'pg': scrape_magicbricks_pg,
        },
    }

    def get(self, request):
        return Response({
            "message": "Scraper API Trigger Endpoint",
            "usage": "Send a POST request with JSON payload to trigger scraping.",
            "options": {
                "source": ["nobroker", "magicbricks", "all"],
                "category": ["rent", "sale", "comm_rent", "comm_sale", "pg", "all"],
                "city": "mumbai (or any supported city)",
                "pages": "int (default: 1)",
                "details": "boolean (default: false)",
            },
        })

    def post(self, request):
        source = request.data.get('source', 'nobroker').lower()
        category = request.data.get('category', 'rent').lower()
        city = request.data.get('city', 'mumbai')
        pages = int(request.data.get('pages', 1))
        fetch_details = bool(request.data.get('details', False))

        if source not in ['nobroker', 'magicbricks', 'all']:
            return Response(
                {"error": f"Invalid source '{source}'. Must be 'nobroker', 'magicbricks', or 'all'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if category not in ['rent', 'sale', 'comm_rent', 'comm_sale', 'pg', 'all']:
            return Response(
                {"error": f"Invalid category '{category}'. Must be 'rent', 'sale', 'comm_rent', 'comm_sale', 'pg', or 'all'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sources_to_run = ['nobroker', 'magicbricks'] if source == 'all' else [source]
        categories_to_run = (
            ['rent', 'sale', 'comm_rent', 'comm_sale', 'pg']
            if category == 'all'
            else [category]
        )

        results_summary = {}
        total_scraped = 0

        for src in sources_to_run:
            results_summary[src] = {}
            for cat in categories_to_run:
                func = self.SCRAPER_MAP.get(src, {}).get(cat)
                if not func:
                    continue
                try:
                    kwargs = {'city': city, 'pages': pages, 'save_to_db': True}
                    if src == 'nobroker':
                        kwargs['fetch_details'] = fetch_details
                    scraped = func(**kwargs)
                    count = len(scraped)
                    results_summary[src][cat] = {"status": "success", "count": count}
                    total_scraped += count
                except Exception as e:
                    logger.error(f"Error scraping {src} {cat}: {e}")
                    results_summary[src][cat] = {"status": "error", "error": str(e)}

        return Response({
            "status": "completed",
            "total_scraped": total_scraped,
            "city": city,
            "pages": pages,
            "results": results_summary,
        }, status=status.HTTP_200_OK)
