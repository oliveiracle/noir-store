from django.shortcuts import render
from products.models import Product


def index(request):
    new_products = Product.objects.filter(is_new=True).order_by('?')[:4]
    strip_products = Product.objects.filter(image__isnull=False).exclude(image='')
    context = {'new_products': new_products, 'strip_products': strip_products}
    return render(request, 'home/index.html', context)


def faq(request):
    return render(request, 'home/faq.html')


def shipping(request):
    return render(request, 'home/shipping.html')


def returns(request):
    return render(request, 'home/returns.html')


def contact(request):
    return render(request, 'home/contact.html')
