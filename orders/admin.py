from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Встроенная форма для отображения элементов заказа в административной панели.
    """
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['get_cost']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Order.
    Отображение и управление заказами.
    """
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'status', 'paid', 'created', 'get_total_cost']
    list_filter = ['paid', 'status', 'created']
    list_editable = ['paid', 'status']
    search_fields = ['user__username', 'first_name', 'last_name', 'email']
    readonly_fields = ['created', 'updated']
    inlines = [OrderItemInline]
    
    def get_total_cost(self, obj):
        """Отображает общую стоимость заказа"""
        return obj.get_total_cost()
    get_total_cost.short_description = 'Общая стоимость'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Административная панель для модели OrderItem.
    Отображение элементов заказов.
    """
    list_display = ['order', 'product', 'price', 'quantity', 'get_cost']
    list_filter = ['order__status']
    search_fields = ['order__user__username', 'product__name']
    
    def get_cost(self, obj):
        """Отображает стоимость элемента заказа"""
        return obj.get_cost()
    get_cost.short_description = 'Стоимость'
