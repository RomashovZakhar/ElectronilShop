from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Главная страница со списком товаров
    path('', views.product_list, name='product_list'),
    # Список товаров по категории
    path('category/<slug:category_slug>/', views.product_list, name='category_list'),
    # Детальная страница товара
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]
