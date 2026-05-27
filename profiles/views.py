from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order
from products.models import Product
from .forms import UserProfileForm
from .models import Wishlist


@login_required
def profile(request):
    user_profile = request.user.profile

    # Get all orders linked to this user's email, newest first
    orders = Order.objects.filter(email=request.user.email).order_by('-date')

    # Get or create the wishlist — every user should have one
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Bind the form to both the POST data and the existing profile instance
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        # Pre-fill the form with the user's current saved info
        form = UserProfileForm(instance=user_profile)

    context = {'form': form, 'orders': orders, 'wishlist': wishlist}
    return render(request, 'profiles/profile.html', context)


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # get_or_create ensures the user always has a wishlist record
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    # Check if the product is already in the wishlist
    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f'"{product.name}" removed from wishlist.')
    else:
        wishlist.products.add(product)
        messages.success(request, f'"{product.name}" added to wishlist.')

    return redirect('product_detail', product_id=product_id)
