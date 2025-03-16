from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, TableViewSet, OrderViewSet, OrderStatusViewSet

router = DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'tables', TableViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'statuses', OrderStatusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]