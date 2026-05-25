from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product, Review


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name='jackets', friendly_name='Jackets'
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.category), 'jackets')

    def test_get_friendly_name(self):
        self.assertEqual(self.category.get_friendly_name(), 'Jackets')


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='jackets')
        self.product = Product.objects.create(
            name='Dark Jacket',
            description='A premium jacket.',
            price=299.00,
            category=self.category,
            is_new=True,
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.product), 'Dark Jacket')

    def test_is_new_default_false(self):
        product = Product.objects.create(
            name='Basic Tee', description='Plain tee.', price=99.00
        )
        self.assertFalse(product.is_new)

    def test_category_optional(self):
        product = Product.objects.create(
            name='No Cat', description='No category.', price=50.00
        )
        self.assertIsNone(product.category)


class ProductViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='jackets', friendly_name='Jackets'
        )
        self.product = Product.objects.create(
            name='Dark Jacket',
            description='A premium jacket.',
            price=299.00,
            category=self.category,
        )

    def test_all_products_page_loads(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')

    def test_product_detail_page_loads(self):
        response = self.client.get(
            reverse('product_detail', args=[self.product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_detail_404_for_invalid_id(self):
        response = self.client.get(reverse('product_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_search_returns_matching_product(self):
        response = self.client.get(reverse('products'), {'q': 'Jacket'})
        self.assertContains(response, 'Dark Jacket')

    def test_search_returns_no_results_for_unknown_term(self):
        response = self.client.get(reverse('products'), {'q': 'xyznothing'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NO PRODUCTS FOUND')

    def test_category_filter(self):
        response = self.client.get(
            reverse('products'), {'category': 'jackets'}
        )
        self.assertContains(response, 'Dark Jacket')


class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='pass1234'
        )
        self.product = Product.objects.create(
            name='Dark Jacket', description='A jacket.', price=299.00
        )
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment='Incredible quality.',
        )

    def test_str_format(self):
        self.assertIn('testuser', str(self.review))
        self.assertIn('Dark Jacket', str(self.review))

    def test_review_linked_to_product(self):
        self.assertEqual(self.review.product, self.product)


class AdminProductViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@noir.com'
        )
        self.regular_user = User.objects.create_user(
            username='user', password='user123'
        )
        self.product = Product.objects.create(
            name='Dark Jacket', description='A jacket.', price=299.00
        )

    def test_add_product_requires_login(self):
        response = self.client.get(reverse('add_product'))
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("add_product")}'
        )

    def test_non_superuser_cannot_add_product(self):
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('add_product'))
        self.assertRedirects(response, reverse('products'))

    def test_superuser_can_access_add_product(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_delete_product(self):
        self.client.login(username='admin', password='admin123')
        self.client.post(
            reverse('delete_product', args=[self.product.id])
        )
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
