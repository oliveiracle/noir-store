import uuid
from django.db import models
from django.db.models import Sum
from products.models import Product


class Order(models.Model):

    # The order number is auto-generated using UUID — not editable by users
    order_number = models.CharField(max_length=32, null=False, editable=False)

    # Customer delivery details
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)

    # Auto-set date when the order is created
    date = models.DateTimeField(auto_now_add=True)

    # These are calculated automatically in the update_total method
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)

    # Stripe payment intent ID — used to link the order to a payment
    stripe_pid = models.CharField(
        max_length=254, null=False, blank=False, default='')

    def _generate_order_number(self):
        # UUID gives us a random 32-character string — very unlikely to repeat
        return uuid.uuid4().hex.upper()

    def update_total(self):
        # Sum all the line item totals to get the order total
        self.order_total = (
            self.lineitems.aggregate(
                Sum('lineitem_total'))['lineitem_total__sum'] or 0
        )
        # Free delivery for orders over €150, otherwise 10% of the total
        self.delivery_cost = (
            0 if self.order_total >= 150
            else round(self.order_total * 0.1, 2)
        )
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        # Only generate the order number if the order doesn't have one yet
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):

    # Each line item belongs to one order and refers to one product
    order = models.ForeignKey(
        Order, null=False, blank=False,
        on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)

    # Calculated automatically — price x quantity
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the line total before saving
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
