from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.views.static import serve
from home.sitemaps import StaticViewSitemap, ProductSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}


def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Disallow: /admin/\n"
        "Disallow: /accounts/\n"
        "Disallow: /bag/\n"
        "Disallow: /checkout/\n"
        "Sitemap: https://noir-store.herokuapp.com/sitemap.xml\n"
    )
    return HttpResponse(content, content_type='text/plain')


handler404 = 'home.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('bag/', include('bag.urls')),
    path('checkout/', include('checkout.urls')),
    path('profile/', include('profiles.urls')),
    path('robots.txt', robots_txt),
    path(
        'sitemap.xml', sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    re_path(
        r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
]
