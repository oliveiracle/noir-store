from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from products.models import Product


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return ['home', 'products', 'faq', 'shipping', 'returns', 'contact']

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return None
