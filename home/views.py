from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import NewsletterSubscriber


def index(request):
    # order_by('?') randomises the selection so different products appear each visit
    new_products = Product.objects.filter(is_new=True).order_by('?')[:4]
    # Only show products that have an uploaded image in the scrolling strip
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
    # message_sent is used to show a success message in the template
    # without a redirect, so the user sees confirmation on the same page
    message_sent = False
    if request.method == 'POST':
        message_sent = True
    # Pre-fill the email field for logged-in users
    user_email = ''
    if request.user.is_authenticated:
        user_email = request.user.email
    return render(
        request, 'home/contact.html',
        {'message_sent': message_sent, 'user_email': user_email}
    )


def about(request):
    return render(request, 'home/about.html')


def facebook_mockup(request):
    # Marketing page showing a mockup of the NOIR Facebook business page
    return render(request, 'home/facebook_mockup.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)


def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            # get_or_create prevents duplicate entries for the same email
            _, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "You're on the list. Welcome to NOIR.")
            else:
                messages.info(request, "You're already subscribed.")
    # Redirect back to whichever page the form was submitted from
    return redirect(request.META.get('HTTP_REFERER', '/'))
