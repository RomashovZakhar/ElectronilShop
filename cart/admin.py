from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Cart.
    Отображение корзин пользователей.
    """
    list_display = ['user', 'created', 'updated', 'get_total_price', 'get_total_quantity']
    list_filter = ['created', 'updated']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created', 'updated']
    
    def get_total_price(self, obj):
        """Отображает общую стоимость корзины"""
        return obj.get_total_price()
    get_total_price.short_description = 'Общая стоимость'
    
    def get_total_quantity(self, obj):
        """Отображает общее количество товаров в корзине"""
        return obj.get_total_quantity()
    get_total_quantity.short_description = 'Общее количество'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Административная панель для модели CartItem.
    Отображение элементов корзины.
    """
    list_display = ['cart', 'product', 'quantity', 'get_cost', 'created']
    list_filter = ['created']
    search_fields = ['cart__user__username', 'product__name']
    readonly_fields = ['created']
    
    def get_cost(self, obj):
        """Отображает стоимость элемента корзины"""
        return obj.get_cost()
    get_cost.short_description = 'Стоимость'
