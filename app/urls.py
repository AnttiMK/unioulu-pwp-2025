from django.urls import path, include
from rest_framework import routers

from app.views import UserViewSet, TableViewSet, ReservationViewSet, MenuItemViewSet, OrderItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'menu-items', MenuItemViewSet, basename='menuitem')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'orders', OrderViewSet, basename='order')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
