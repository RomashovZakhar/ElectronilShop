from cart.models import Cart


def cart_items_count(request):
    """
    Контекстный процессор для отображения количества товаров в корзине.
    Добавляет переменную cart_items_count в контекст всех шаблонов.
    """
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            return {'cart_items_count': cart.get_total_quantity()}
    return {'cart_items_count': 0}
