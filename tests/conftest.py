import os
import pytest
from django.contrib.auth.models import User
from store.models import Category, Product
from cart.models import Cart, CartItem

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electronics_store.settings')


@pytest.fixture
def category(db):
    return Category.objects.create(name='Ноутбуки', slug='noutbuki')


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        category=category,
        name='Ноутбук Pro',
        slug='noutbuk-pro',
        price='75000.00',
        available=True,
    )


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='pass12345', email='test@test.ru')


@pytest.fixture
def auth_client(client, user):
    client.login(username='testuser', password='pass12345')
    return client


@pytest.fixture
def cart(db, user):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_with_item(db, cart, product):
    CartItem.objects.create(cart=cart, product=product, quantity=2)
    return cart
