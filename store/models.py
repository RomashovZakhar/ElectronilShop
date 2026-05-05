from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """
    Модель категории товаров.
    Содержит название категории и slug для URL.
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Возвращает URL для отображения категории"""
        return reverse('store:category_list', args=[self.slug])


class Product(models.Model):
    """
    Модель товара.
    Содержит всю информацию о товаре: название, описание, цену, изображение и т.д.
    """
    category = models.ForeignKey(Category, related_name='products', 
                                on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Slug')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Возвращает URL для отображения товара"""
        return reverse('store:product_detail', args=[self.id, self.slug])
    
    def save(self, *args, **kwargs):
        """Автоматически создает slug из названия при сохранении"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
