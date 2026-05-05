from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    """
    Команда для заполнения базы данных тестовыми данными.
    Создает категории и товары для демонстрации функционала магазина.
    """
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание категорий...')

        categories_data = [
            {
                'name': 'Ноутбуки',
                'slug': 'laptops',
                'products': [
                    {
                        'name': 'MacBook Pro 13"',
                        'description': 'Мощный ноутбук от Apple с процессором M2, 8 ГБ RAM и 256 ГБ SSD.',
                        'price': 129999.00,
                        'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Dell XPS 15',
                        'description': 'Премиальный ноутбук с 15.6" дисплеем и Intel Core i7.',
                        'price': 159999.00,
                        'image_url': 'https://images.unsplash.com/photo-1593642634367-d91a135587b5?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Lenovo ThinkPad X1 Carbon',
                        'description': 'Легкий бизнес-ноутбук с отличной автономностью.',
                        'price': 89999.00,
                        'image_url': 'https://images.unsplash.com/photo-1587614382346-4ec70e388b28?w=800&q=80&auto=format',
                    },
                ]
            },
            {
                'name': 'Смартфоны',
                'slug': 'smartphones',
                'products': [
                    {
                        'name': 'iPhone 15 Pro',
                        'description': 'Флагман Apple с процессором A17 Pro.',
                        'price': 99999.00,
                        'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484f4f7f?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Samsung Galaxy S24',
                        'description': 'Android-флагман с отличной камерой.',
                        'price': 89999.00,
                        'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Google Pixel 8',
                        'description': 'Лучший камерофон на чистом Android.',
                        'price': 79999.00,
                        'image_url': 'https://images.unsplash.com/photo-1695900119230-b0dff78eaef5?w=800&q=80&auto=format',
                    },
                ]
            },
            {
                'name': 'Планшеты',
                'slug': 'tablets',
                'products': [
                    {
                        'name': 'iPad Pro 12.9"',
                        'description': 'Планшет с процессором M2 и большим экраном.',
                        'price': 149999.00,
                        'image_url': 'https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Samsung Galaxy Tab S9',
                        'description': 'Android-планшет с S Pen.',
                        'price': 69999.00,
                        'image_url': 'https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Microsoft Surface Pro 9',
                        'description': 'Гибрид планшета и ноутбука.',
                        'price': 129999.00,
                        'image_url': 'https://images.unsplash.com/photo-1518779578993-ec3579fee39f?w=800&q=80&auto=format',
                    },
                ]
            },
            {
                'name': 'Аксессуары',
                'slug': 'accessories',
                'products': [
                    {
                        'name': 'AirPods Pro',
                        'description': 'Наушники с шумоподавлением.',
                        'price': 24999.00,
                        'image_url': 'https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Samsung Galaxy Watch 6',
                        'description': 'Умные часы для здоровья.',
                        'price': 29999.00,
                        'image_url': 'https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=800&q=80&auto=format',
                    },
                    {
                        'name': 'Logitech MX Master 3S',
                        'description': 'Профессиональная беспроводная мышь.',
                        'price': 8999.00,
                        'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&q=80&auto=format',
                    },
                ]
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            if created:
                self.stdout.write(f'Создана категория: {category.name}')

            for prod_data in cat_data['products']:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    category=category,
                    defaults={
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'image_url': prod_data['image_url'],
                        'available': True,
                    }
                )
                if created:
                    self.stdout.write(f'  Создан товар: {product.name}')
                else:
                    changed = False
                    if not product.image_url:
                        product.image_url = prod_data['image_url']
                        changed = True
                    if product.image:
                        product.image = ''
                        changed = True
                    if changed:
                        product.save()
                        self.stdout.write(f'  Обновлен товар: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )
