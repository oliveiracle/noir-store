from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product


class BagViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name='Dark Jacket', description='A jacket.', price=299.00
        )

    def test_bag_page_loads(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')

    def test_add_to_bag(self):
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 1, 'redirect_url': '/bag/'},
        )
        self.assertRedirects(response, '/bag/')
        bag = self.client.session.get('bag', {})
        self.assertIn(str(self.product.id), bag)

    def test_add_to_bag_increases_quantity(self):
        self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 1, 'redirect_url': '/bag/'},
        )
        self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 2, 'redirect_url': '/bag/'},
        )
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 3)

    def test_remove_from_bag(self):
        self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 1, 'redirect_url': '/bag/'},
        )
        self.client.post(reverse('remove_from_bag', args=[self.product.id]))
        bag = self.client.session.get('bag', {})
        self.assertNotIn(str(self.product.id), bag)

    def test_update_bag_quantity(self):
        self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 1, 'redirect_url': '/bag/'},
        )
        self.client.post(
            reverse('update_bag', args=[self.product.id]),
            {'quantity': 3},
        )
        bag = self.client.session.get('bag', {})
        self.assertEqual(bag[str(self.product.id)], 3)

    def test_update_bag_with_zero_removes_item(self):
        self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 1, 'redirect_url': '/bag/'},
        )
        self.client.post(
            reverse('update_bag', args=[self.product.id]),
            {'quantity': 0},
        )
        bag = self.client.session.get('bag', {})
        self.assertNotIn(str(self.product.id), bag)

    def test_add_to_bag_rejects_open_redirect(self):
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]),
            {'quantity': 1, 'redirect_url': 'https://evil.com'},
        )
        self.assertRedirects(response, '/products/')
