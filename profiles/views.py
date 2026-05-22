from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order
from products.models import Product
from .forms import UserProfileForm
from .models import Wishlist


@login_required
def profile(request):
    """Display and update the user's delivery profile and order history."""
    user_profile = request.user.profile
    orders = Order.objects.filter(email=request.user.email).order_by('-date')
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form, 'orders': orders, 'wishlist': wishlist}
    return render(request, 'profiles/profile.html', context)


@login_required
def toggle_wishlist(request, product_id):
    """Add or remove a product from the user's wishlist."""
    product = get_object_or_404(Product, pk=product_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

    if product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f'"{product.name}" removed from wishlist.')
    else:
        wishlist.products.add(product)
        messages.success(request, f'"{product.name}" added to wishlist.')

    return redirect('product_detail', product_id=product_id)
