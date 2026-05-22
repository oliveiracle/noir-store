from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Represents a product category like Jackets or Trousers."""

    name = models.CharField(max_length=254)
    # Friendly name is shown to users; the regular name is used internally
    friendly_name = models.CharField(max_length=254, blank=True)

    class Meta:
        # Fix Django's default pluralisation of "Categorys"
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        """Return the display-friendly name for this category."""
        return self.friendly_name


class Product(models.Model):
    """Represents a product available for sale in the store."""

    # Category is optional — a product can exist without one
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    sku = models.CharField(max_length=254, blank=True)  # Stock keeping unit
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Rating is optional since new products may not have one yet
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True
    )
    image = models.ImageField(null=True, blank=True)

    # Used to display products in the "New Arrivals" section on the homepage
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Review(models.Model):
    """A customer review for a product."""

    # Choices list: 1 star to 5 stars
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    # Link to the product being reviewed
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews'
    )
    # Link to the user who wrote the review
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=500)

    # Automatically set when the review is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent a user from leaving more than one review per product
        unique_together = ('product', 'user')
        # Show the most recent reviews first
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.product.name}'
