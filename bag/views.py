from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """Render the shopping bag page."""
    # The bag contents are passed via the context processor in bag/contexts.py
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a product to the shopping bag or increase its quantity."""
    # Get the product or return 404 if it doesn't exist
    product = get_object_or_404(Product, pk=item_id)

    # Get quantity from the form and make sure it's between 1 and 99
    quantity = int(request.POST.get('quantity', 1))
    quantity = max(1, min(quantity, 99))

    # Get the URL to redirect back to after adding the item
    redirect_url = request.POST.get('redirect_url', '/products/')

    # Safety check to prevent open redirect attacks
    if not redirect_url.startswith('/'):
        redirect_url = '/products/'

    # The bag is stored in the session as a dictionary {item_id: quantity}
    bag = request.session.get('bag', {})
    key = str(item_id)  # Session keys must be strings

    # If product already in bag, increase quantity; otherwise add it
    if key in bag:
        bag[key] += quantity
    else:
        bag[key] = quantity

    # Save the updated bag back to the session
    request.session['bag'] = bag
    messages.success(request, f'"{product.name}" added to your bag.')
    return redirect(redirect_url)


def update_bag(request, item_id):
    """Update item quantity in the bag, or remove it if zero."""
    quantity = int(request.POST.get('quantity', 1))
    bag = request.session.get('bag', {})
    key = str(item_id)

    # If quantity is more than 0, update it; otherwise remove the item
    if quantity > 0:
        bag[key] = quantity
    else:
        bag.pop(key, None)  # Remove item safely without raising an error

    request.session['bag'] = bag
    return redirect('view_bag')


def remove_from_bag(request, item_id):
    """Remove an item from the shopping bag entirely."""
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})

    # pop() removes the item from the dict; None avoids a KeyError if missing
    bag.pop(str(item_id), None)

    request.session['bag'] = bag
    messages.success(request, f'"{product.name}" removed from your bag.')
    return redirect('view_bag')
