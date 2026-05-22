from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('add/', views.add_product, name='add_product'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path(
        '<int:product_id>/delete/',
        views.delete_product,
        name='delete_product',
    ),
    path(
        '<int:product_id>/review/',
        views.add_review,
        name='add_review',
    ),
    path(
        'review/<int:review_id>/edit/',
        views.edit_review,
        name='edit_review',
    ),
    path(
        'review/<int:review_id>/delete/',
        views.delete_review,
        name='delete_review',
    ),
]
