from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    # The bag contents (items, totals, delivery) are injected via the
    # bag_contents context processor defined in bag/contexts.py
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    # Clamp quantity between 1 and 99 to prevent invalid values
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, 99))
    redirect_url = request.POST.get('redirect_url', '/products/')

    # Prevent open redirect — only allow paths within this site
    if not redirect_url.startswith('/'):
        redirect_url = '/products/'

    # The bag is stored in the session as {product_id: quantity}
    bag = request.session.get('bag', {})
    key = str(item_id)

    # If the product is already in the bag, increase the quantity
    if key in bag:
        bag[key] += quantity
    else:
        bag[key] = quantity

    # Reassigning triggers Django to mark the session as modified and save it
    request.session['bag'] = bag
    messages.success(request, f'"{product.name}" added to your bag.')
    return redirect(redirect_url)


def update_bag(request, item_id):
    # Clamp quantity to 1–10 on the server side, regardless of what the form sends
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, 10))
    bag = request.session.get('bag', {})
    key = str(item_id)

    if quantity > 0:
        bag[key] = quantity
    else:
        # If quantity reaches zero, remove the item entirely
        bag.pop(key, None)

    request.session['bag'] = bag
    return redirect('view_bag')


def remove_from_bag(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    # pop with a default of None avoids a KeyError if the item is already gone
    bag.pop(str(item_id), None)
    request.session['bag'] = bag
    messages.success(request, f'"{product.name}" removed from your bag.')
    return redirect('view_bag')
