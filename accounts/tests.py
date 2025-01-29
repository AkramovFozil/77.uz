from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from products.models import Category

class UserCreatePostTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/accounts/seller/registration/"
        self.category = Category.objects.filter(id=3)

    def test_create_post(self):
        data = {'username': 'your username', 'product': 'category of product that you wanna sell', 'phone_number': 'your phone number', 'category': self.category, 'address': 'your address'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserUpdatePutTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = f"/api/accounts/me/update/{'your user id'}"
        self.category = Category.objects.filter(id='your category id')

    def test_update_put(self):
        data = {'username': 'your username', 'product': "category of product that you wanna sell", 'phone_number': 'your phone number', 'category': self.category,
                'address': 'your address'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDeleteTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = f"/api/accounts/me/destroy/{'your_user_id'}"

    def test_destroy_delete(self):
        response = self.client.delete(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserRetrieveGetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = f"/api/accounts/me/{'Any user id or your id'}"

    def test_retrieve_get(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserLoginJwtTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/accounts/login/"

    def test_login_post(self):
        data = {'username': 'your username that you registered', 'password': 'your password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class UserRefreshJwtTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/accounts/refresh/"

    def test_refresh_post(self):
        data = {'username': 'your username that you registered', 'password': 'your password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class UserLogoutTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/accounts/logout/"

    def test_logout_post(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


