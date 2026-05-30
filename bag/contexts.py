import json
from products.models import Product


def all_products_json(request):
    # Serialise all products to JSON so the chat widget can search them
    # client-side without making extra API calls
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
    # Read the bag from the session — it's stored as {product_id: quantity}
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
            # If a product was deleted after being added to the bag, skip it
            pass

    from decimal import Decimal
    # Free delivery on orders over €150, otherwise 10% of the order total
    delivery = 0 if total >= 150 else round(total * Decimal('0.1'), 2)
    grand_total = total + delivery

    return {
        'bag_items': bag_items,
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'item_count': item_count,
    }
