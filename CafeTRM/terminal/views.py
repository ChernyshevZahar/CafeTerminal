from django.views.generic.edit import CreateView , UpdateView, DeleteView
from django.views.generic import ListView , TemplateView
from django.urls import reverse_lazy
from .models import Order, Dish, OrderDish, Table, OrderStatus
from .forms import OrderForm, OrderDishFormSet
from collections import defaultdict
from django.utils import timezone
from decimal import Decimal

from django.db.models import Q
from django.contrib import messages

class OrderCreateView(CreateView):
    """
    Представление для создание ордера

    Возвращает:
        Контекст - возвращете данные из баз по столам и статусам
        Форму для создание ордера

    """
    model = Order
    form_class = OrderForm
    template_name = 'terminal/create_order.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        context['statuses'] = OrderStatus.objects.all()
        if self.request.POST:
            context['formset'] = OrderDishFormSet(self.request.POST)
        else:
            context['formset'] = OrderDishFormSet()



        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            for order_dish_form in formset:
                if order_dish_form.cleaned_data.get('dish'):
                    order_dish = order_dish_form.save(commit=False)
                    order_dish.order = self.object
                    order_dish.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrderUpdateView(UpdateView):
    """
        Представление для редоктирование ордера

        Возвращает:
            Контекст - данные по объекту по id
            Форму для обновления заказа
    """
    model = Order
    form_class = OrderForm
    template_name = 'terminal/update_order.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tables'] = Table.objects.all()
        if self.request.POST:
            context['formset'] = OrderDishFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = OrderDishFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class OrderDeleteView(DeleteView):
    """
            Представление для удаления ордера

    """
    model = Order
    template_name = 'terminal/delete_order.html'
    success_url = reverse_lazy('order_list')

class OrderListView(ListView):
    """
        Представление для удаления ордера

        Возвращает:
            Контекст - сформерованый по запросу utm


    """
    model = Order
    template_name = 'terminal/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        """
             Подготовка данных по фильтрации

             Возвращает:
                Фильтрацию или по num заказа, столу, статусу

        """
        queryset = super().get_queryset()


        order_id = self.request.GET.get('order_id')
        table_id = self.request.GET.get('table')
        status_id = self.request.GET.get('status')


        filters = Q()

        # Фильтрация по ID заказа
        if order_id:
            try:
                order_id = int(order_id)
                filters &= Q(num=order_id)
            except ValueError:
                messages.warning(self.request, "Номер заказа должен быть числом.")

        # Фильтрация по столу
        if table_id:
            try:
                table_id = int(table_id)
                filters &= Q(table_id=table_id)
            except ValueError:
                messages.warning(self.request, "Нет такого стола")

        # Фильтрация по статусу
        if status_id:
            try:
                status_id = int(status_id)
                filters &= Q(status_id=status_id)
            except ValueError:
                messages.warning(self.request, "Нет такого статуса")


        queryset = queryset.filter(filters)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['statuses'] = OrderStatus.objects.all()
        context['tables'] = Table.objects.all()


        context['order_id'] = self.request.GET.get('order_id', '')
        context['table_id'] = self.request.GET.get('table', '')
        context['status_id'] = self.request.GET.get('status', '')

        return context


class IncomeByDayView(TemplateView):
    """
            Представление для сметы по дням

            Возвращает:
                Контекст - сформерованый отчет дохода по каждому дню


        """

    template_name = 'terminal/income_by_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        paid_status = OrderStatus.objects.get(name='оплачено')


        paid_orders = Order.objects.filter(status=paid_status)


        income_by_day = defaultdict(Decimal)
        for order in paid_orders:
            day = order.created_at.date()
            income_by_day[day] += Decimal(order.total_amount)


        income_by_day = sorted(income_by_day.items(), reverse=True)


        context['income_by_day'] = income_by_day
        return context