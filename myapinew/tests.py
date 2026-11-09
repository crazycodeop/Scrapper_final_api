from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

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
from myapinew.scrapers.base import BaseScraper


class ModelTestCase(TestCase):
    def test_model_creation_and_str(self):
        """Verify models can be created and __str__ executes without error."""
        sale = res_sale_model.objects.create(
            BHK="2 BHK", Proptype="sale", Locality="Andheri", City="Mumbai"
        )
        self.assertIn("2 BHK", str(sale))

        rent = res_rent_model.objects.create(
            BHK="1 BHK", Proptype="rent", Locality="Bandra", City="Mumbai"
        )
        self.assertIn("1 BHK", str(rent))

        pg = res_pg_model.objects.create(
            Owner="Sunshine PG", Locality="Powai", City="Mumbai"
        )
        self.assertIn("Sunshine PG", str(pg))

        csale = comm_sale_model.objects.create(
            Proptype="Office Space", Locality="BKC", City="Mumbai"
        )
        self.assertIn("Office Space", str(csale))

        clease = comm_lease_model.objects.create(
            Retailer="Retail Shop", Locality="Dadar", City="Mumbai"
        )
        self.assertIn("Retail Shop", str(clease))

        nb_rent = no_broker_rent_model.objects.create(
            Apt_Type="2 BHK", Nearby="Malad West", Rent="45000"
        )
        self.assertIn("2 BHK", str(nb_rent))

        nb_sale = no_broker_sale_model.objects.create(
            Apt_Type="3 BHK", Nearby="Borivali", Price="1.5 Cr"
        )
        self.assertIn("3 BHK", str(nb_sale))

        nb_crent = no_broker_comm_rent_model.objects.create(
            Prop_Type="Shop", Nearby="Thane", Rent="25000"
        )
        self.assertIn("Shop", str(nb_crent))

        nb_csale = no_broker_comm_sale_model.objects.create(
            Apt_Type="Commercial Space", Nearby="Kandivali", Price="80 L"
        )
        self.assertIn("Commercial Space", str(nb_csale))

        nb_pg = no_broker_pg_model.objects.create(
            Room_Type="Single Room", Nearby="Goregaon", Rent="12000"
        )
        self.assertIn("Single Room", str(nb_pg))


class APIEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nb_rent = no_broker_rent_model.objects.create(
            Apt_Type="2 BHK",
            Nearby="Malad",
            Rent="40000",
            SQFT="800 sqft",
            Furnishing="Furnished",
        )

    def test_nobroker_rent_endpoint(self):
        response = self.client.get(reverse('nobrokerRent-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['Apt_Type'], "2 BHK")

    def test_nobroker_rent_filter(self):
        response = self.client.get(reverse('nobrokerRent-list') + '?search=Malad')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data['results']), 1)

        response_none = self.client.get(reverse('nobrokerRent-list') + '?search=NonExistentLocality')
        self.assertEqual(response_none.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_none.json()['results']), 0)

    def test_all_list_endpoints(self):
        endpoints = [
            'res_sale_model-list',
            'res_rent_model-list',
            'res_pg_model-list',
            'comm_sale_model-list',
            'comm_lease_model-list',
            'nobrokerRent-list',
            'nobrokerSale-list',
            'noBrokerCommRent-list',
            'noBrokerCommSale-list',
            'noBrokerPg-list',
        ]
        for name in endpoints:
            response = self.client.get(reverse(name))
            self.assertEqual(response.status_code, status.HTTP_200_OK, f"Endpoint {name} failed")

    def test_scrape_trigger_endpoint_get(self):
        response = self.client.get(reverse('api-scrape-trigger'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('options', response.json())

    def test_scrape_trigger_endpoint_validation(self):
        response = self.client.post(
            reverse('api-scrape-trigger'),
            {"source": "invalid_source", "category": "rent"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_cat = self.client.post(
            reverse('api-scrape-trigger'),
            {"source": "nobroker", "category": "invalid_category"},
            format='json'
        )
        self.assertEqual(response_cat.status_code, status.HTTP_400_BAD_REQUEST)


class ScraperUtilitiesTestCase(TestCase):
    def test_clean_text(self):
        clean = BaseScraper.clean_text("  ₹ 45,000 \xa0 per month   \n")
        self.assertEqual(clean, "45,000 per month")

    def test_clean_currency(self):
        clean = BaseScraper.clean_currency("₹ 1,50,000")
        self.assertEqual(clean, "150000")
