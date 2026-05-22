from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Review
from .forms import ProductForm, ReviewForm


def all_products(request):
    """Display all products with optional search and category filtering."""
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
    """Display a single product detail page."""
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()
    user_review = None
    review_form = None

    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        if not user_review:
            review_form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def add_review(request, product_id):
    """Allow authenticated users to submit a review for a product."""
    product = get_object_or_404(Product, pk=product_id)
    if Review.objects.filter(product=product, user=request.user).exists():
        messages.info(request, 'You have already reviewed this product.')
        return redirect('product_detail', product_id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added.')
    return redirect('product_detail', product_id=product_id)


@login_required
def edit_review(request, review_id):
    """Allow users to edit their own review."""
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated.')
            return redirect('product_detail', product_id=review.product.id)
    else:
        form = ReviewForm(instance=review)
    return render(
        request,
        'products/edit_review.html',
        {'form': form, 'review': review},
    )


@login_required
def delete_review(request, review_id):
    """Allow users to delete their own review."""
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Your review has been removed.')
    return redirect('product_detail', product_id=product_id)


@login_required
def add_product(request):
    """Allow superusers to add a new product to the store."""
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
    """Allow superusers to edit an existing product."""
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
    """Allow superusers to delete a product from the store."""
    if not request.user.is_superuser:
        messages.error(request, 'Access restricted to store administrators.')
        return redirect('products')
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'"{product.name}" deleted.')
    return redirect('products')
