import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from products.models import Product
from bag.contexts import bag_contents
from profiles.models import UserProfile
from .forms import OrderForm
from .models import Order, OrderLineItem


def checkout(request):
    # Get the Stripe keys from settings (stored in environment variables)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Get the shopping bag from the session
    bag = request.session.get('bag', {})
    if not bag:
        # Don't let users access checkout with an empty bag
        messages.error(request, 'Your bag is empty.')
        return redirect(reverse('products'))

    # Get the full bag context to access the grand total
    current_bag = bag_contents(request)
    total = current_bag['grand_total']

    # Stripe expects the amount in cents/pence, so we multiply by 100
    stripe_total = round(float(total) * 100)
    stripe.api_key = stripe_secret_key

    # Create a PaymentIntent — this is what Stripe uses to process the payment
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == 'POST':
        # Collect all the form data from the POST request
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            # Save the order but don't commit yet — we need to add the PID
            order = order_form.save(commit=False)

            # Extract the PaymentIntent ID from the client_secret string
            pid = request.POST.get('client_secret', '')
            order.stripe_pid = pid.split('_secret')[0]
            order.save()

            # Create a line item for each product in the bag
            for item_id, quantity in bag.items():
                product = get_object_or_404(Product, pk=item_id)
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
            order.update_total()

            # Clear the bag from the session after the order is placed
            request.session['bag'] = {}
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            messages.error(
                request,
                'There was an error with your form. Please check your details.'
            )
    else:
        # Pre-fill the form with the user's saved profile info if logged in
        initial = {}
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                initial = {
                    'full_name': (
                        request.user.get_full_name() or
                        request.user.username
                    ),
                    'email': request.user.email,
                    'phone_number': profile.phone_number,
                    'street_address1': profile.street_address1,
                    'street_address2': profile.street_address2,
                    'town_or_city': profile.town_or_city,
                    'postcode': profile.postcode,
                    'country': profile.country,
                    'county': profile.county,
                }
            except UserProfile.DoesNotExist:
                pass  # If there's no profile yet, just leave the form blank
        order_form = OrderForm(initial=initial)

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        # The client_secret is passed to the Stripe JS on the frontend
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def send_confirmation_email(order):
    # Build the subject and body from templates to keep things clean
    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order},
    ).strip()
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order},
    )
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],  # Send to the customer's email address
    )


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    # Send the confirmation email when the user reaches this page
    send_confirmation_email(order)

    messages.success(request, f'Order {order_number} confirmed!')
    return render(
        request, 'checkout/checkout_success.html', {'order': order}
    )
