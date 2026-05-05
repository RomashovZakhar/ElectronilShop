import pytest
from django.urls import reverse
from store.models import Product


@pytest.mark.django_db
class TestCategoryModel:
    def test_str(self, category):
        assert str(category) == 'Ноутбуки'

    def test_absolute_url(self, category):
        assert category.get_absolute_url() == reverse('store:category_list', args=['noutbuki'])


@pytest.mark.django_db
class TestProductModel:
    def test_str(self, product):
        assert str(product) == 'Ноутбук Pro'

    def test_absolute_url(self, product):
        expected = reverse('store:product_detail', args=[product.id, 'noutbuk-pro'])
        assert product.get_absolute_url() == expected

    def test_slug_auto_generated(self, category):
        p = Product.objects.create(category=category, name='Samsung Galaxy', price='50000.00')
        assert p.slug == 'samsung-galaxy'


@pytest.mark.django_db
class TestProductListView:
    def test_status_200(self, client, product):
        response = client.get(reverse('store:product_list'))
        assert response.status_code == 200

    def test_context_has_products(self, client, product):
        response = client.get(reverse('store:product_list'))
        assert 'products' in response.context
        assert 'categories' in response.context

    def test_only_available_shown(self, client, category):
        Product.objects.create(
            category=category, name='Видимый', slug='vidimyj', price='1000.00', available=True
        )
        Product.objects.create(
            category=category, name='Скрытый', slug='skrytyj', price='500.00', available=False
        )
        response = client.get(reverse('store:product_list'))
        names = [p.name for p in response.context['products']]
        assert 'Видимый' in names
        assert 'Скрытый' not in names

    def test_category_filter(self, client, product, category):
        response = client.get(reverse('store:category_list', args=[category.slug]))
        assert response.status_code == 200
        assert response.context['category'] == category

    def test_template_used(self, client, product):
        response = client.get(reverse('store:product_list'))
        assert 'store/product/list.html' in [t.name for t in response.templates]


@pytest.mark.django_db
class TestProductDetailView:
    def test_status_200(self, client, product):
        response = client.get(product.get_absolute_url())
        assert response.status_code == 200

    def test_context_has_product(self, client, product):
        response = client.get(product.get_absolute_url())
        assert response.context['product'] == product

    def test_unavailable_returns_404(self, client, category):
        p = Product.objects.create(
            category=category, name='Недоступный', slug='nedostupnyj', price='100.00', available=False
        )
        response = client.get(p.get_absolute_url())
        assert response.status_code == 404
