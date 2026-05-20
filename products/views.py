from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    current_category = None
    query = request.GET.get('q')
    category_filter = request.GET.get('category')

    if query:
        products = (
            products.filter(name__icontains=query) |
            products.filter(description__icontains=query)
        )

    if category_filter:
        products = products.filter(category__name=category_filter)
        current_category = category_filter

    categories_with_products = []
    if not current_category and not query:
        for cat in categories:
            cat_products = Product.objects.filter(category=cat)
            if cat_products.exists():
                categories_with_products.append({
                    'category': cat,
                    'products': cat_products,
                })

    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'query': query,
        'categories_with_products': categories_with_products,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Access restricted to store administrators.')
        return redirect('products')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'"{product.name}" added successfully.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access restricted to store administrators.')
        return redirect('products')
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'"{product.name}" updated successfully.')
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(
        request,
        'products/edit_product.html',
        {'form': form, 'product': product},
    )


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Access restricted to store administrators.')
        return redirect('products')
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'"{product.name}" deleted.')
    return redirect('products')
