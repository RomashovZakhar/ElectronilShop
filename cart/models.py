from decimal import Decimal
from django.conf import settings
from django.db import models
from store.models import Product


class Cart(models.Model):
    """
    Модель корзины покупок.
    Связана с пользователем и содержит товары в корзине.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
    
    def __str__(self):
        return f'Корзина пользователя {self.user.username}'
    
    def get_total_price(self):
        """Возвращает общую стоимость товаров в корзине"""
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_quantity(self):
        """Возвращает общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Модель элемента корзины.
    Содержит товар и его количество в корзине.
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'элемент корзины'
        verbose_name_plural = 'элементы корзины'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f'{self.quantity}x {self.product.name}'
    
    def get_cost(self):
        """Возвращает стоимость данного количества товара"""
        return self.product.price * self.quantity
