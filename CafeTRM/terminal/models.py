from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Table(models.Model):
    number = models.CharField(max_length=50, unique=True)  # Номер стола (уникальный)
    description = models.TextField(blank=True, null=True)  # Описание стола (необязательно)

    def __str__(self):
        return f"Стол {self.number}"



class Order(models.Model):
    num = models.IntegerField(blank=True, null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    dishes = models.ManyToManyField('Dish', through='OrderDish')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, null=True, blank=True)
    def str(self):
        return f"Order {self.id}"

    def save(self, *args, **kwargs):
        if not self.num:
            last_order = Order.objects.order_by('-num').first()
            self.num = last_order.num + 1 if last_order else 1
        super().save(*args, **kwargs)

        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

    def calculate_total_amount(self):
        total = 0
        for order_dish in self.order_dishes.all():
            total += order_dish.dish.price * order_dish.quantity
        return total


class OrderDish(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,  related_name='order_dishes')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Количество блюд

    def __str__(self):
        return f"{self.dish.name} x {self.quantity} in Order {self.order.id}"


class OrderStatus(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
