from django.shortcuts import render, redirect
from django.contrib import messages
from products.models import Product
from .models import NewsletterSubscriber


def index(request):
    """Render the homepage with new arrivals and the product strip."""
    # Get up to 4 products marked as new, in random order
    new_products = Product.objects.filter(is_new=True).order_by('?')[:4]

    # Get all products that have an image for the scrolling strip
    strip_products = (
        Product.objects.filter(image__isnull=False).exclude(image='')
    )
    context = {
        'new_products': new_products,
        'strip_products': strip_products,
    }
    return render(request, 'home/index.html', context)


def faq(request):
    """Render the FAQ page."""
    return render(request, 'home/faq.html')


def shipping(request):
    """Render the shipping information page."""
    return render(request, 'home/shipping.html')


def returns(request):
    """Render the returns policy page."""
    return render(request, 'home/returns.html')


def contact(request):
    """Render the contact page and handle form submission."""
    message_sent = False
    if request.method == 'POST':
        message_sent = True
    user_email = ''
    if request.user.is_authenticated:
        user_email = request.user.email
    return render(
        request, 'home/contact.html',
        {'message_sent': message_sent, 'user_email': user_email}
    )


def about(request):
    """Render the About Us page."""
    return render(request, 'home/about.html')


def facebook_mockup(request):
    """Render the Facebook Business Page screenshots for marketing."""
    return render(request, 'home/facebook_mockup.html')


def custom_404(request, exception):
    """Render a custom 404 error page."""
    return render(request, '404.html', status=404)


def newsletter_signup(request):
    """Handle newsletter email subscription via POST."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            # get_or_create avoids duplicate entries for the same email
            _, created = NewsletterSubscriber.objects.get_or_create(
                email=email
            )
            if created:
                messages.success(
                    request, "You're on the list. Welcome to NOIR."
                )
            else:
                messages.info(request, "You're already subscribed.")
    # Redirect the user back to whatever page they signed up from
    return redirect(request.META.get('HTTP_REFERER', '/'))
