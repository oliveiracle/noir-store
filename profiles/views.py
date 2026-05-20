from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from checkout.models import Order
from .forms import UserProfileForm


@login_required
def profile(request):
    user_profile = request.user.profile
    orders = Order.objects.filter(email=request.user.email).order_by('-date')

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    context = {'form': form, 'orders': orders}
    return render(request, 'profiles/profile.html', context)
