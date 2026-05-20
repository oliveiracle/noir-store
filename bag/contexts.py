import json
from products.models import Product


def all_products_json(request):
    """Return all products as a JSON-serialisable dict for the chat widget."""
    products = Product.objects.select_related('category').all()
    data = [
        {
            'name': p.name,
            'category': p.category.friendly_name if p.category else '',
            'price': str(p.price),
            'id': p.id,
        }
        for p in products
    ]
    return {'products_json': json.dumps(data)}


def bag_contents(request):
    """Calculate bag totals and return context for use across all templates."""
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

    delivery = 0 if total >= 150 else round(total * 0.1, 2)
    grand_total = total + delivery

    return {
        'bag_items': bag_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'item_count': item_count,
    }
