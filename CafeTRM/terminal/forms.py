from django import forms
from django.forms import inlineformset_factory
from .models import Order, Dish, OrderDish

class OrderForm(forms.ModelForm):
    """
    Форма для выбора  статусов и стола

    """

    class Meta:
        model = Order
        fields = [ 'table', 'status']


#FormSet для подгрузки блюд и работы выборки их в заказе

OrderDishFormSet = inlineformset_factory(
    Order,
    OrderDish,
    fields=('dish', 'quantity'),
    extra=7,
    widgets={
        'dish': forms.Select(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)