from django.urls import include, path
from rest_framework import routers
from myapinew import views

router = routers.DefaultRouter()
router.register(r'res_sale_model', views.resSaleViewSet, basename='res_sale_model')
router.register(r'res_rent_model', views.resRentViewSet, basename='res_rent_model')
router.register(r'res_pg_model', views.resPgViewSet, basename='res_pg_model')
router.register(r'comm_sale_model', views.commSaleViewSet, basename='comm_sale_model')
router.register(r'comm_lease_model', views.commLeaseViewSet, basename='comm_lease_model')
router.register(r'nobrokerRent', views.noBrokerRent, basename='nobrokerRent')
router.register(r'nobrokerSale', views.noBrokerSale, basename='nobrokerSale')
router.register(r'noBrokerCommRent', views.noBrokerCommRent, basename='noBrokerCommRent')
router.register(r'noBrokerCommSale', views.noBrokerCommSale, basename='noBrokerCommSale')
router.register(r'noBrokerPg', views.noBrokerPg, basename='noBrokerPg')

urlpatterns = [
    path('scrape/', views.ScrapeTriggerAPIView.as_view(), name='api-scrape-trigger'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
