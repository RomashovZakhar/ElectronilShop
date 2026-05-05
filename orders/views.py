from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    """
    Создает новый заказ из товаров в корзине.
    
    Args:
        request: HTTP запрос
    
    Returns:
        HttpResponse: HTML страница с формой заказа или редирект на страницу успеха
    """
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart or not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста.')
        return redirect('store:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Создаем заказ
                order = form.save(commit=False)
                order.user = request.user
                order.save()
                
                # Создаем элементы заказа из корзины
                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        price=cart_item.product.price,
                        quantity=cart_item.quantity
                    )
                
                # Очищаем корзину
                cart.delete()
                
                messages.success(request, f'Заказ #{order.id} успешно создан!')
                return redirect('orders:order_detail', order_id=order.id)
    else:
        # Предзаполняем форму данными пользователя
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = OrderCreateForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'orders/order/create.html', context)


@login_required
def order_list(request):
    """
    Отображает список заказов пользователя.
    
    Args:
        request: HTTP запрос
    
    Returns:
        HttpResponse: HTML страница со списком заказов
    """
    orders = Order.objects.filter(user=request.user).order_by('-created')
    
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order/list.html', context)


@login_required
def order_detail(request, order_id):
    """
    Отображает детальную информацию о заказе.
    
    Args:
        request: HTTP запрос
        order_id: ID заказа
    
    Returns:
        HttpResponse: HTML страница с детальной информацией о заказе
    """
    order = Order.objects.filter(user=request.user, id=order_id).first()
    
    if not order:
        messages.error(request, 'Заказ не найден.')
        return redirect('orders:order_list')
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order/detail.html', context)
