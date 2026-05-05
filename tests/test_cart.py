import pytest
from django.urls import reverse
from cart.models import CartItem


@pytest.mark.django_db
class TestCartModel:
    def test_str(self, cart, user):
        assert user.username in str(cart)

    def test_total_price_empty(self, cart):
        assert cart.get_total_price() == 0

    def test_total_price_with_items(self, cart_with_item, product):
        product.refresh_from_db()
        assert cart_with_item.get_total_price() == product.price * 2

    def test_total_quantity(self, cart_with_item):
        assert cart_with_item.get_total_quantity() == 2

    def test_item_get_cost(self, cart, product):
        item = CartItem.objects.create(cart=cart, product=product, quantity=3)
        assert item.get_cost() == product.price * 3


@pytest.mark.django_db
class TestCartViews:
    def test_cart_detail_requires_login(self, client):
        response = client.get(reverse('cart:cart_detail'))
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_cart_detail_authenticated(self, auth_client):
        response = auth_client.get(reverse('cart:cart_detail'))
        assert response.status_code == 200
        assert 'cart' in response.context

    def test_cart_add_requires_login(self, client, product):
        response = client.get(reverse('cart:cart_add', args=[product.id]))
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_cart_add_creates_item(self, auth_client, product, user):
        auth_client.get(reverse('cart:cart_add', args=[product.id]))
        assert CartItem.objects.filter(product=product).count() == 1

    def test_cart_add_redirects_to_product(self, auth_client, product):
        response = auth_client.get(reverse('cart:cart_add', args=[product.id]))
        assert response.status_code == 302
        assert response['Location'] == product.get_absolute_url()

    def test_cart_add_increments_existing(self, auth_client, product, cart, user):
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        auth_client.get(reverse('cart:cart_add', args=[product.id]))
        item = CartItem.objects.get(product=product)
        assert item.quantity == 2

    def test_cart_remove(self, auth_client, product, cart):
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        response = auth_client.get(reverse('cart:cart_remove', args=[product.id]))
        assert response.status_code == 302
        assert not CartItem.objects.filter(product=product).exists()

    def test_cart_update(self, auth_client, product, cart):
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        auth_client.post(
            reverse('cart:cart_update', args=[product.id]),
            {'quantity': 5},
        )
        item = CartItem.objects.get(product=product)
        assert item.quantity == 5

    def test_cart_update_zero_removes_item(self, auth_client, product, cart):
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        auth_client.post(
            reverse('cart:cart_update', args=[product.id]),
            {'quantity': 0},
        )
        assert not CartItem.objects.filter(product=product).exists()
