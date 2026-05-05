from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Добавление товара в корзину
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    # Удаление товара из корзины
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    # Обновление количества товара в корзине
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    # Просмотр корзины
    path('', views.cart_detail, name='cart_detail'),
]
