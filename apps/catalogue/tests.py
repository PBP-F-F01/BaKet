from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .views import add_review_ajax
from apps.catalogue.models import Product, Cart, CartItem, Order, Review

class ProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name='Test Product',
            price=50000,
            category='smartphone',
            specs='Test Specifications',
            image=None
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 50000)
        self.assertEqual(self.product.category, 'smartphone')


class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.cartitem_set.count(), 0)

    def test_add_item_to_cart(self):
        product = Product.objects.create(
            name='Test Product',
            price=50000,
            category='smartphone',
            specs='Test Specifications',
            image=None
        )
        cart_item = CartItem.objects.create(cart=self.cart, product=product, quantity=2)
        self.assertEqual(self.cart.cartitem_set.count(), 1)
        self.assertEqual(cart_item.get_total_price(), 100000)


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.cart = Cart.objects.create(user=self.user)
        self.order = Order.objects.create(user=self.user, cart=self.cart)

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertFalse(self.order.is_paid)


class AddToCartViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name='Test Product',
            price=50000,
            category='smartphone',
            specs='Test Specifications',
            image=None
        )
        self.client.login(username='testuser', password='12345')

    def test_add_to_cart(self):
        response = self.client.get(f'/catalogue/cart/add/{self.product.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/catalogue/cart/')
class ReviewViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        self.product = Product.objects.create(
            name='Test Product',
            category='smartphone',
            price=100,
            specs='Test Specs'
        )

        self.client = Client()

    def test_add_review_ajax_authenticated_user(self):
        self.client.login(username='testuser', password='testpass')

        response = self.client.post(reverse('catalogue:add_review_ajax'), {
            'prod_id': str(self.product.id),
            'comment': 'Great product!',
            'rate': 5,
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, b'CREATED')

        review = Review.objects.get(user=self.user, product=self.product)
        self.assertEqual(review.comment, 'Great product!')
        self.assertEqual(review.rating, 5)

    def test_add_review_ajax_existing_review(self):
        self.client.login(username='testuser', password='testpass')

        Review.objects.create(user=self.user, product=self.product, comment='Old review', rating=3)

        response = self.client.post(reverse('catalogue:add_review_ajax'), {
            'prod_id': str(self.product.id),
            'comment': 'Updated review',
            'rate': 4,
        })

        self.assertEqual(response.status_code, 201)

        review = Review.objects.get(user=self.user, product=self.product)
        self.assertEqual(review.comment, 'Updated review')
        self.assertEqual(review.rating, 4)

    def test_add_review_ajax_empty_rating(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('catalogue:add_review_ajax'), {
            'prod_id': str(self.product.id),
            'comment': 'No rating provided',
            'rate': '',
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('Rating cannot be empty!', response.content.decode())
