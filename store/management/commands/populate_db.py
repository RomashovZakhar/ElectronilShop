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
                        'image_url': 'https://i.ebayimg.com/images/g/EGUAAOSwSWhjxdjA/s-l1200.jpg',
                    },
                    {
                        'name': 'Dell XPS 15',
                        'description': 'Премиальный ноутбук с 15.6" дисплеем и Intel Core i7.',
                        'price': 159999.00,
                        'image_url': 'https://www.notebookcheck-ru.com/uploads/tx_nbc2/DellXPS15-9510__1__04.jpg',
                    },
                    {
                        'name': 'Lenovo ThinkPad X1 Carbon',
                        'description': 'Легкий бизнес-ноутбук с отличной автономностью.',
                        'price': 89999.00,
                        'image_url': 'https://cdn.kns.ru/linkpics/lenovo-thinkpad-x1-carbon-gen-13-aura-edition-21nxa038cd_kod_1032329.jpg',
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
                        'image_url': 'https://hi-stores.ru/upload/iblock/dfd/s6rq8qz7df2vo9azcpsag1mgk2u7hu6z.jpg',
                    },
                    {
                        'name': 'Samsung Galaxy S24',
                        'description': 'Android-флагман с отличной камерой.',
                        'price': 89999.00,
                        'image_url': 'https://cdn1.technopark.ru/technopark/photos_resized/product/1000_1000/713856/1_713856.jpg',
                    },
                    {
                        'name': 'Google Pixel 8',
                        'description': 'Лучший камерофон на чистом Android.',
                        'price': 79999.00,
                        'image_url': 'https://main-cdn.sbermegamarket.ru/big1/hlr-system/-18/927/334/591/120/214/7/600014221751b0.jpeg',
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
                        'image_url': 'https://store123.ru/upload/rbs.moyskladstocks/files/0e709015-bfa3-415e-aa02-6b93d8f4fb71/462cc94b2cd8d6915c20b2c8f20c1a5d/3de/rk3v4r3no638khnxpntsbj0wwhi0pvh0.jpg',
                    },
                    {
                        'name': 'Samsung Galaxy Tab S9',
                        'description': 'Android-планшет с S Pen.',
                        'price': 69999.00,
                        'image_url': 'https://www.notebookcheck-ru.com/uploads/tx_nbc2/Samsung_Galaxy_Tab_S9_Ultra.JPG',
                    },
                    {
                        'name': 'Microsoft Surface Pro 9',
                        'description': 'Гибрид планшета и ноутбука.',
                        'price': 129999.00,
                        'image_url': 'https://microless.com/cdn/products/47694d88b5353f6bef8a52a530993ea3-hi.jpg',
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
                        'image_url': 'https://static.insales-cdn.com/images/products/1/255/764788991/fe890d70a3a23e9367a5d6ac0bd1b00b.jpg',
                    },
                    {
                        'name': 'Samsung Galaxy Watch 6',
                        'description': 'Умные часы для здоровья.',
                        'price': 29999.00,
                        'image_url': 'https://hi-stores.ru/upload/iblock/8d3/evfu11dtl578wcb9dcr3qqowrpbq8mk2.jpg',
                    },
                    {
                        'name': 'Logitech MX Master 3S',
                        'description': 'Профессиональная беспроводная мышь.',
                        'price': 8999.00,
                        'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTadwItNLzz97u-4tz7klbhNAT6UfH8Tpe89Q&s',
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
                    new_image_url = prod_data.get('image_url', '')
                    if new_image_url and product.image_url != new_image_url:
                        product.image_url = new_image_url
                        changed = True

                    new_description = prod_data.get('description', '')
                    if product.description != new_description:
                        product.description = new_description
                        changed = True

                    new_price = prod_data.get('price')
                    if new_price is not None and product.price != new_price:
                        product.price = new_price
                        changed = True

                    if product.available is not True:
                        product.available = True
                        changed = True

                    if new_image_url and product.image:
                        product.image = ''
                        changed = True
                    if changed:
                        product.save()
                        self.stdout.write(f'  Обновлен товар: {product.name}')

        self.stdout.write(
            self.style.SUCCESS('База данных успешно заполнена тестовыми данными!')
        )
