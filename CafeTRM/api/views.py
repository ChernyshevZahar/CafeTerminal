from rest_framework import viewsets
from terminal.models import Order, OrderDish, Dish, Table, OrderStatus
from .serializers import OrderSerializer, DishSerializer, TableSerializer, OrderStatusSerializer
from django_filters import rest_framework as filters

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class OrderStatusViewSet(viewsets.ModelViewSet):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer

class OrderFilter(filters.FilterSet):
    num = filters.NumberFilter(field_name='num')
    table = filters.NumberFilter(field_name='table__id')
    status = filters.NumberFilter(field_name='status__id')

    class Meta:
        model = Order
        fields = ['num', 'table', 'status']
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = OrderFilter