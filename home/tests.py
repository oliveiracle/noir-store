from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product
from .models import NewsletterSubscriber


class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_homepage_shows_new_products(self):
        Product.objects.create(
            name='New Jacket', description='New arrival.', price=299.00,
            is_new=True
        )
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'New Jacket')

    def test_faq_page_loads(self):
        response = self.client.get(reverse('faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/faq.html')

    def test_shipping_page_loads(self):
        response = self.client.get(reverse('shipping'))
        self.assertEqual(response.status_code, 200)

    def test_returns_page_loads(self):
        response = self.client.get(reverse('returns'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')

    def test_contact_form_submission(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@noir.com',
            'subject': 'Hello',
            'message': 'Test message',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message received")

    def test_about_page_loads(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)


class NewsletterTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_newsletter_signup_creates_subscriber(self):
        self.client.post(
            reverse('newsletter_signup'), {'email': 'test@noir.com'}
        )
        self.assertTrue(
            NewsletterSubscriber.objects.filter(
                email='test@noir.com'
            ).exists()
        )

    def test_newsletter_duplicate_does_not_create_second_record(self):
        self.client.post(
            reverse('newsletter_signup'), {'email': 'test@noir.com'}
        )
        self.client.post(
            reverse('newsletter_signup'), {'email': 'test@noir.com'}
        )
        self.assertEqual(
            NewsletterSubscriber.objects.filter(
                email='test@noir.com'
            ).count(), 1
        )
