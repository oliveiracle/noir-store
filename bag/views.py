from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/products/')

    bag = request.session.get('bag', {})
    key = str(item_id)

    if key in bag:
        bag[key] += quantity
    else:
        bag[key] = quantity

    request.session['bag'] = bag
    messages.success(request, f'"{product.name}" added to your bag.')
    return redirect(redirect_url)
