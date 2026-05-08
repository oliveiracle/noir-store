from products.models import Product


def bag_contents(request):
    bag = request.session.get('bag', {})
    bag_items = []
    total = 0
    item_count = 0

    for item_id, quantity in bag.items():
        try:
            product = Product.objects.get(pk=item_id)
            subtotal = product.price * quantity
            total += subtotal
            item_count += quantity
            bag_items.append({
                'item_id': item_id,
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })
        except Product.DoesNotExist:
            pass

    return {
        'bag_items': bag_items,
        'total': total,
        'item_count': item_count,
    }
