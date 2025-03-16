from rest_framework import serializers
from terminal.models import Order, OrderDish, Dish, Table, OrderStatus

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
    dishes = OrderDishSerializer(source='order_dishes', many=True)
    table = TableSerializer(read_only=True)
    table_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), write_only=True)
    status = OrderStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=OrderStatus.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):

        dishes_data = validated_data.pop('order_dishes')


        order = Order.objects.create(**validated_data)


        for dish_data in dishes_data:
            OrderDish.objects.create(order=order, dish=dish_data['dish_id'], quantity=dish_data['quantity'])

        return order

    def update(self, instance, validated_data):

        instance.num = validated_data.get('num', instance.num)
        instance.table = validated_data.get('table_id', instance.table)
        instance.status = validated_data.get('status_id', instance.status)
        instance.save()


        dishes_data = validated_data.get('order_dishes', [])


        instance.order_dishes.all().delete()


        for dish_data in dishes_data:
            OrderDish.objects.create(order=instance, dish=dish_data['dish_id'], quantity=dish_data['quantity'])

        return instance