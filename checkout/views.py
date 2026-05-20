import stripe
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from products.models import Product
from bag.contexts import bag_contents
from profiles.models import UserProfile
from .forms import OrderForm
from .models import Order, OrderLineItem


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Your bag is empty.')
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(float(total) * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if request.method == 'POST':
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
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret', '')
            order.stripe_pid = pid.split('_secret')[0]
            order.save()
            for item_id, quantity in bag.items():
                product = get_object_or_404(Product, pk=item_id)
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                )
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
                pass
        order_form = OrderForm(initial=initial)

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, 'checkout/checkout.html', context)


def checkout_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order {order_number} confirmed!')
    return render(
        request, 'checkout/checkout_success.html', {'order': order}
    )
