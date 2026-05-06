from django.shortcuts import render
from .models import Product, Category


def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    current_category = None

    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__name=category_filter)
        current_category = category_filter

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
    }
    return render(request, 'products/products.html', context)
