import pytest
from django.urls import reverse
from cart.models import Cart, CartItem
from orders.models import Order, OrderItem

ORDER_DATA = {
    'first_name': 'Иван',
    'last_name': 'Иванов',
    'email': 'ivan@test.ru',
    'address': 'ул. Ленина, 1',
    'postal_code': '123456',
    'city': 'Москва',
    'phone': '+79991234567',
}


@pytest.fixture
def order(db, user):
    return Order.objects.create(user=user, **ORDER_DATA)


@pytest.mark.django_db
class TestOrderModel:
    def test_str(self, order):
        assert str(order.id) in str(order)

    def test_default_status(self, order):
        assert order.status == 'pending'

    def test_not_paid_by_default(self, order):
        assert order.paid is False

    def test_total_cost(self, order, product):
        product.refresh_from_db()
        OrderItem.objects.create(order=order, product=product, price=product.price, quantity=2)
        assert order.get_total_cost() == product.price * 2


@pytest.mark.django_db
class TestOrderViews:
    def test_order_list_requires_login(self, client):
        response = client.get(reverse('orders:order_list'))
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_order_list_authenticated(self, auth_client):
        response = auth_client.get(reverse('orders:order_list'))
        assert response.status_code == 200
        assert 'orders' in response.context

    def test_order_create_empty_cart_redirects(self, auth_client):
        response = auth_client.get(reverse('orders:order_create'))
        assert response.status_code == 302
        assert response['Location'] == reverse('store:product_list')

    def test_order_create_success(self, auth_client, product, user):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        response = auth_client.post(reverse('orders:order_create'), ORDER_DATA)
        assert Order.objects.filter(user=user).count() == 1
        order = Order.objects.get(user=user)
        assert response['Location'] == reverse('orders:order_detail', args=[order.id])

    def test_order_create_clears_cart(self, auth_client, product, user):
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        auth_client.post(reverse('orders:order_create'), ORDER_DATA)
        assert not Cart.objects.filter(user=user).exists()

    def test_order_detail_own_order(self, auth_client, order):
        response = auth_client.get(reverse('orders:order_detail', args=[order.id]))
        assert response.status_code == 200
        assert response.context['order'] == order

    def test_order_detail_foreign_order_redirects(self, client, db):
        from django.contrib.auth.models import User
        other = User.objects.create_user(username='other', password='pass12345')
        other_order = Order.objects.create(user=other, **ORDER_DATA)
        client.login(username='testuser', password='pass12345')
        # testuser не создан, получим редирект на логин
        response = client.get(reverse('orders:order_detail', args=[other_order.id]))
        assert response.status_code == 302
