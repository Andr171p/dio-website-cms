from django.http import JsonResponse
from wagtail.models import Page
from .models import ProductPage
from fuzzywuzzy import fuzz
from django.db.models import Q

def search_products(request, page_id):
    query = request.GET.get('q', '').strip()
    manufacturer = request.GET.get('manufacturer', 'all')
    
    # Получаем продукты текущей подкатегории
    products = ProductPage.objects.child_of(Page.objects.get(pk=page_id)).live()
    
    # Фильтрация по производителю
    if manufacturer and manufacturer != 'all':
        products = products.filter(manufacturer=manufacturer)
    
    # Нечёткий поиск
    if query:
        filtered_products = []
        for product in products:
            # Вычисляем похожесть для title и description
            title_score = fuzz.partial_ratio(query.lower(), product.title.lower())
            desc_score = fuzz.partial_ratio(query.lower(), product.description.to_plaintext().lower()) if product.description else 0
            # Добавляем продукт, если есть достаточное совпадение (порог 70)
            if title_score > 70 or desc_score > 70:
                filtered_products.append(product)
    else:
        filtered_products = products

    # Формируем JSON-ответ
    results = [{
        'title': product.title,
        'url': product.url,
        'description': product.description.to_plaintext()[:100] if product.description else '',
        'price': str(product.price) if product.price else '',
        'currency': product.currency,
        'manufacturer': product.manufacturer,
        'image': product.image.get_rendition('fill-600x400').url if product.image else ''
    } for product in filtered_products]
    
    return JsonResponse({'products': results})