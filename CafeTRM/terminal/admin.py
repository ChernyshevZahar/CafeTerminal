from django.contrib import admin
from .models import Order, Dish ,Table, OrderStatus

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ["name","price"]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["num","table"]

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ["number"]

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ["name"]