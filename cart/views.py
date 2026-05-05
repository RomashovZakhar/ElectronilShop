from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .models import Cart, CartItem


@login_required
def cart_add(request, product_id):
    """
    Добавляет товар в корзину.
    
    Args:
        request: HTTP запрос
        product_id: ID товара для добавления
    
    Returns:
        HttpResponse: Редирект на страницу товара или корзины
    """
    product = get_object_or_404(Product, id=product_id, available=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Количество товара "{product.name}" увеличено в корзине.')
    else:
        messages.success(request, f'Товар "{product.name}" добавлен в корзину.')

    return redirect(product.get_absolute_url())


@login_required
def cart_remove(request, product_id):
    """
    Удаляет товар из корзины.
    
    Args:
        request: HTTP запрос
        product_id: ID товара для удаления
    
    Returns:
        HttpResponse: Редирект на страницу корзины
    """
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    cart_item.delete()
    messages.success(request, f'Товар "{product.name}" удален из корзины.')
    
    return redirect('cart:cart_detail')


@login_required
def cart_detail(request):
    """
    Отображает содержимое корзины.
    
    Args:
        request: HTTP запрос
    
    Returns:
        HttpResponse: HTML страница с содержимым корзины
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
    }
    return render(request, 'cart/detail.html', context)


@login_required
def cart_update(request, product_id):
    """
    Обновляет количество товара в корзине.
    
    Args:
        request: HTTP запрос
        product_id: ID товара для обновления
    
    Returns:
        HttpResponse: Редирект на страницу корзины
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart = get_object_or_404(Cart, user=request.user)
            product = get_object_or_404(Product, id=product_id)
            cart_item = get_object_or_404(CartItem, cart=cart, product=product)
            
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Количество товара "{product.name}" обновлено.')
        else:
            # Если количество 0 или меньше, удаляем товар из корзины
            return cart_remove(request, product_id)
    
    return redirect('cart:cart_detail')
