from django.shortcuts import render
from products.models import Product


def index(request):
    new_products = Product.objects.filter(is_new=True).order_by('?')[:4]
    context = {'new_products': new_products}
    return render(request, 'home/index.html', context)
