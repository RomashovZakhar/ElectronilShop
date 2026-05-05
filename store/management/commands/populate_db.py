from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.utils.text import slugify


class Command(BaseCommand):
    """
    Команда для заполнения базы данных тестовыми данными.
    Создает категории и товары для демонстрации функционала магазина.
    """
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание категорий...')
        
        # Создаем категории
        categories_data = [
            {
                'name': 'Ноутбуки',
                'slug': 'laptops',
                'products': [
                    {
                        'name': 'MacBook Pro 13"',
                        'description': 'Мощный ноутбук от Apple с процессором M2, 8 ГБ RAM и 256 ГБ SSD. Идеален для работы и творчества.',
                        'price': 129999.00,
                        'image': None
                    },
                    {
                        'name': 'Dell XPS 15',
                        'description': 'Премиальный ноутбук с 15.6" дисплеем, Intel Core i7, 16 ГБ RAM и 512 ГБ SSD. Отличный выбор для профессионалов.',
                        'price': 159999.00,
                        'image': None
                    },
                    {
                        'name': 'Lenovo ThinkPad X1 Carbon',
                        'description': 'Легкий и прочный бизнес-ноутбук с 14" дисплеем, Intel Core i5, 8 ГБ RAM и 256 ГБ SSD.',
                        'price': 89999.00,
                        'image': None
                    }
                ]
            },
            {
                'name': 'Смартфоны',
                'slug': 'smartphones',
                'products': [
                    {
                        'name': 'iPhone 15 Pro',
                        'description': 'Новейший iPhone с процессором A17 Pro, 6.1" дисплеем и тройной камерой. Максимальная производительность.',
                        'price': 99999.00,
                        'image': None
                    },
                    {
                        'name': 'Samsung Galaxy S24',
                        'description': 'Флагманский Android-смартфон с 6.2" дисплеем, Snapdragon 8 Gen 3 и отличной камерой.',
                        'price': 89999.00,
                        'image': None
                    },
                    {
                        'name': 'Google Pixel 8',
                        'description': 'Смартфон с лучшей камерой и чистой Android-системой. 6.2" дисплей и Tensor G3 процессор.',
                        'price': 79999.00,
                        'image': None
                    }
                ]
            },
            {
                'name': 'Планшеты',
                'slug': 'tablets',
                'products': [
                    {
                        'name': 'iPad Pro 12.9"',
                        'description': 'Мощный планшет с 12.9" дисплеем, процессором M2 и поддержкой Apple Pencil. Идеален для творчества.',
                        'price': 149999.00,
                        'image': None
                    },
                    {
                        'name': 'Samsung Galaxy Tab S9',
                        'description': 'Android-планшет с 11" дисплеем, Snapdragon 8 Gen 2 и S Pen в комплекте.',
                        'price': 69999.00,
                        'image': None
                    },
                    {
                        'name': 'Microsoft Surface Pro 9',
                        'description': 'Гибридный планшет-ноутбук с 13" дисплеем, Intel Core i5 и Windows 11.',
                        'price': 129999.00,
                        'image': None
                    }
                ]
            },
            {
                'name': 'Аксессуары',
                'slug': 'accessories',
                'products': [
                    {
                        'name': 'AirPods Pro',
                        'description': 'Беспроводные наушники с активным шумоподавлением и пространственным звуком.',
                        'price': 24999.00,
                        'image': None
                    },
                    {
                        'name': 'Samsung Galaxy Watch 6',
                        'description': 'Умные часы с круглосуточным мониторингом здоровья и множеством функций.',
                        'price': 29999.00,
                        'image': None
                    },
                    {
                        'name': 'Logitech MX Master 3S',
                        'description': 'Беспроводная мышь для профессионалов с точным сенсором и эргономичным дизайном.',
                        'price': 8999.00,
                        'image': None
                    }
                ]
            }
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            
            if created:
                self.stdout.write(f'Создана категория: {category.name}')
            
            # Создаем товары для категории
            for prod_data in cat_data['products']:
                product, created = Product.objects.get_or_create(
                    name=prod_data['name'],
                    category=category,
                    defaults={
                        'description': prod_data['description'],
                        'price': prod_data['price'],
                        'available': True
                    }
                )
                
                if created:
                    self.stdout.write(f'Создан товар: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )
