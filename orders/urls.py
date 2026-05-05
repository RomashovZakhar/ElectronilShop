from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Создание нового заказа
    path('create/', views.order_create, name='order_create'),
    # Список заказов пользователя
    path('', views.order_list, name='order_list'),
    # Детальная информация о заказе
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
