from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """Render the shopping bag page."""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a product to the shopping bag or increase its quantity."""
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, 99))
    redirect_url = request.POST.get('redirect_url', '/products/')

    if not redirect_url.startswith('/'):
        redirect_url = '/products/'

    bag = request.session.get('bag', {})
    key = str(item_id)

    if key in bag:
        bag[key] += quantity
    else:
        bag[key] = quantity

    request.session['bag'] = bag
    messages.success(request, f'"{product.name}" added to your bag.')
    return redirect(redirect_url)


def update_bag(request, item_id):
    """Update item quantity in the bag, or remove it if zero."""
    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})
    key = str(item_id)

    if quantity > 0:
        bag[key] = quantity
    else:
        bag.pop(key, None)

    request.session['bag'] = bag
    return redirect('view_bag')


def remove_from_bag(request, item_id):
    """Remove an item from the shopping bag entirely."""
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    bag.pop(str(item_id), None)
    request.session['bag'] = bag
    messages.success(request, f'"{product.name}" removed from your bag.')
    return redirect('view_bag')
