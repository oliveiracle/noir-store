from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from products.models import Product
from .models import Order, OrderLineItem


class StripeWH_Handler:
    """Handle Stripe webhooks for payment events."""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send order confirmation email to the customer."""
        subject = render_to_string(
            'checkout/confirmation_emails/'
            'confirmation_email_subject.txt',
            {'order': order},
        ).strip()
        body = render_to_string(
            'checkout/confirmation_emails/'
            'confirmation_email_body.txt',
            {'order': order},
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
        )

    def handle_event(self, event):
        """Handle unexpected or unhandled webhook events."""
        return HttpResponse(
            content=f'Unhandled webhook: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle payment_intent.succeeded webhook from Stripe."""
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.get('bag', '{}')

        billing = intent.charges.data[0].billing_details
        shipping = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        shipping_details = {
            'full_name': shipping.name,
            'email': billing.email,
            'phone_number': shipping.phone,
            'street_address1': shipping.address.line1,
            'street_address2': shipping.address.line2 or '',
            'town_or_city': shipping.address.city,
            'postcode': shipping.address.postal_code or '',
            'country': shipping.address.country,
            'county': shipping.address.state or '',
        }

        order_exists = False
        try:
            order = Order.objects.get(stripe_pid=pid)
            order_exists = True
        except Order.DoesNotExist:
            try:
                order = Order.objects.create(
                    stripe_pid=pid,
                    grand_total=grand_total,
                    **shipping_details,
                )
                import json
                for item_id, quantity in json.loads(bag).items():
                    product = Product.objects.get(pk=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook error: {e}', status=500)

        if not order_exists:
            self._send_confirmation_email(order)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle payment_intent.payment_failed webhook from Stripe."""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )
