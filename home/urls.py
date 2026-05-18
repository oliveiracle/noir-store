from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('faq/', views.faq, name='faq'),
    path('shipping/', views.shipping, name='shipping'),
    path('returns/', views.returns, name='returns'),
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter_signup, name='newsletter_signup'),
    path('about/', views.about, name='about'),
]
