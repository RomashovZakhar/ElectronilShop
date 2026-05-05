from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Product


def product_list(request, category_slug=None):
    """
    Представление для отображения списка товаров.
    
    Args:
        request: HTTP запрос
        category_slug: slug категории (опционально)
    
    Returns:
        HttpResponse: HTML страница со списком товаров
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Если указана категория, фильтруем товары по ней
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Пагинация: 6 товаров на страницу
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является числом, показываем первую страницу
        products = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимальной, показываем последнюю страницу
        products = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'store/product/list.html', context)


def product_detail(request, id, slug):
    """
    Представление для отображения детальной информации о товаре.
    
    Args:
        request: HTTP запрос
        id: ID товара
        slug: slug товара
    
    Returns:
        HttpResponse: HTML страница с детальной информацией о товаре
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    context = {
        'product': product,
    }
    return render(request, 'store/product/detail.html', context)
