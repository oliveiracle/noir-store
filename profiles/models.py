from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product


class UserProfile(models.Model):
    """Stores delivery information for a registered user."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=True, blank=True)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=40, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    profile, _ = UserProfile.objects.get_or_create(user=instance)
    profile.save()


class Wishlist(models.Model):
    """Stores products saved to a user's wishlist."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wishlist'
    )
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s wishlist'
