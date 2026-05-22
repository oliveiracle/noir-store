from django.contrib import admin
from .models import Category, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'friendly_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'rating', 'is_new']
    list_filter = ['category', 'is_new']
    search_fields = ['name', 'description']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    # Shows all reviews with key fields visible at a glance
    list_display = ['product', 'user', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['product__name', 'user__username']
