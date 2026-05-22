from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from products.models import Product
from .models import Order, OrderLineItem


class StripeWH_Handler:
    """Handle Stripe webhooks for payment events."""

    def __init__(self, request):
        # Store the request so we can access it in the handler methods
        self.request = request

    def _send_confirmation_email(self, order):
        """Send order confirmation email to the customer."""
        # Build the subject and body from email template files
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
            [order.email],  # Send to the customer's email
        )

    def handle_event(self, event):
        """Handle unexpected or unhandled webhook events."""
        # Return 200 so Stripe knows we received it, even if we don't act on it
        return HttpResponse(
            content=f'Unhandled webhook: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle payment_intent.succeeded webhook from Stripe."""
        intent = event.data.object
        pid = intent.id  # The PaymentIntent ID

        # The bag was attached to the PaymentIntent as metadata
        bag = intent.metadata.get('bag', '{}')

        # Extract billing and shipping details from the Stripe event
        billing = intent.charges.data[0].billing_details
        shipping = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Build a dictionary of shipping details to create the order
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

        # Check if the order was already created by the checkout view
        order_exists = False
        try:
            order = Order.objects.get(stripe_pid=pid)
            order_exists = True
        except Order.DoesNotExist:
            # Order doesn't exist yet — create it from the webhook data
            try:
                order = Order.objects.create(
                    stripe_pid=pid,
                    grand_total=grand_total,
                    **shipping_details,
                )
                import json
                # Create a line item for each product in the bag
                for item_id, quantity in json.loads(bag).items():
                    product = Product.objects.get(pk=item_id)
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                    )
            except Exception as e:
                # If anything goes wrong, delete the incomplete order
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook error: {e}', status=500)

        # Only send the email if the order was just created by the webhook
        if not order_exists:
            self._send_confirmation_email(order)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle payment_intent.payment_failed webhook from Stripe."""
        # Log that we received it — no action needed for failed payments here
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )
