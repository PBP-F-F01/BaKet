from django.test import TestCase
from django.contrib.auth.models import User
from apps.catalogue.models import Product, Cart, CartItem, Order

class ProductModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(
            name='Test Product',
            price=50000,
            category='smartphone',
            specs='Test Specifications',
            image=None  # You can use mock or temp file for images
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
        self.assertEqual(response.status_code, 200)  # Check that the view is accessible
        self.assertEqual(Cart.objects.get(user=self.user).cartitem_set.count(), 1)
