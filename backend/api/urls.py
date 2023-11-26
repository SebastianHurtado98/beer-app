from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, BeerViewSet, OrderViewSet, BillListView, PayBillView, GenerateBillView

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'beers', BeerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bills/generate/', GenerateBillView.as_view(), name='generate-bill'),
    path('bills/list/', BillListView.as_view(), name='list-bill'),
    path('bills/pay/<int:customer_id>/', PayBillView.as_view(), name='pay-bill'),
]
