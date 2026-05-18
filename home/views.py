from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import NewsletterSubscriber


def index(request):
    new_products = Product.objects.filter(is_new=True).order_by('?')[:4]
    strip_products = (
        Product.objects.filter(image__isnull=False).exclude(image='')
    )
    context = {
        'new_products': new_products,
        'strip_products': strip_products,
    }
    return render(request, 'home/index.html', context)


def faq(request):
    return render(request, 'home/faq.html')


def shipping(request):
    return render(request, 'home/shipping.html')


def returns(request):
    return render(request, 'home/returns.html')


def contact(request):
    message_sent = False
    if request.method == 'POST':
        message_sent = True
    return render(
        request, 'home/contact.html', {'message_sent': message_sent}
    )


def about(request):
    return render(request, 'home/about.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            _, created = NewsletterSubscriber.objects.get_or_create(
                email=email
            )
            if created:
                messages.success(
                    request, "You're on the list. Welcome to NOIR."
                )
            else:
                messages.info(request, "You're already subscribed.")
    return redirect(request.META.get('HTTP_REFERER', '/'))
