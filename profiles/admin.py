from django.contrib import admin
from .models import UserProfile, Wishlist


admin.site.register(UserProfile)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    # Shows each user's wishlist in the admin panel
    list_display = ['user']
    search_fields = ['user__username']
