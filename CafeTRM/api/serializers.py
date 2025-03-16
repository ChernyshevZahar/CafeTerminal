from rest_framework import serializers
from .models import Order, OrderDish, Dish, Table, OrderStatus

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

class OrderDishSerializer(serializers.ModelSerializer):
    dish = DishSerializer(read_only=True)

    class Meta:
        model = OrderDish
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    dishes = OrderDishSerializer(many=True, read_only=True)
    table = TableSerializer(read_only=True)
    status = OrderStatusSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'