from django.urls import path
from .views import OrderCreateView , OrderListView, OrderUpdateView, OrderDeleteView , IncomeByDayView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create_order'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='update_order'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='delete_order'),
    path('income-by-day/', IncomeByDayView.as_view(), name='income_by_day'),
    path('', OrderListView.as_view(), name='order_list'),
]