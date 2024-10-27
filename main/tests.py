from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.user.models import UserProfile
from apps.catalogue.models import Cart

class MainViewsTestCase(TestCase):
    def setUp(self):
        # Set up a client and user for authentication tests
        self.client = Client()
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
    def test_index_view(self):
        """Test index view returns a successful response."""
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('current_time', response.context)
    
    def test_register_view_get(self):
        """Test the register view (GET request)."""
        response = self.client.get(reverse('main:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_view_post_success(self):
        """Test a successful registration."""
        response = self.client.post(reverse('main:register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'Test',
            'last_name': 'User',
        })
        
        print("haii :" + str(response.status_code))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='newuser').exists())

    # def test_register_view_post_failure(self):
    #     """Test registration failure with invalid data."""
    #     response = self.client.post(reverse('main:register'), {
    #         'username': 'newuser',
    #         'password1': 'password123',
    #         'password2': 'wrongpassword',
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(User.objects.filter(username='newuser').exists())
    #     self.assertFalse(UserProfile.objects.filter(user__username='newuser').exists())
    #     self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")

    def test_login_user_view_get(self):
        """Test login page loads correctly with a GET request."""
        response = self.client.get(reverse('main:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_user_view_post_success(self):
        """Test a successful login."""
        response = self.client.post(reverse('main:login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        self.assertIn('_auth_user_id', self.client.session)  # Check if user is logged in

    # def test_login_user_view_post_failure(self):
    #     """Test login failure with incorrect credentials."""
    #     response = self.client.post(reverse('main:login'), {
    #         'username': self.username,
    #         'password': 'wrongpassword',
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')
    #     self.assertContains(response, "Invalid username or password. Please try again.")
    #     self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_user_view(self):
        """Test logout functionality."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('main:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main:index'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_get_cart_count_authenticated(self):
        """Test getting cart count for authenticated user."""
        self.client.login(username=self.username, password=self.password)
        Cart.objects.create(user=self.user)  # Create an empty cart for user
        response = self.client.get(reverse('main:get_cart_count'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'cart_count': 0})

    # def test_get_cart_count_authenticated_with_items(self):
    #     """Test getting cart count with items in the cart."""
    #     self.client.login(username=self.username, password=self.password)
    #     cart = Cart.objects.create(user=self.user)
    #     cart.cartitem_set.create(product_id=1, quantity=2)  # Add an item to the cart
    #     cart.cartitem_set.create(product_id=2, quantity=1)  # Add another item to the cart
    #     response = self.client.get(reverse('main:get_cart_count'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(response.content, {'cart_count': 2})

    # def test_get_cart_count_unauthenticated(self):
    #     """Test getting cart count for unauthenticated user (should be 0)."""
    #     response = self.client.get(reverse('main:get_cart_count'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertJSONEqual(response.content, {'cart_count': 0})
