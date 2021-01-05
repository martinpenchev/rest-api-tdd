import random

from django.test import TestCase
from django.urls import reverse
from django.test import Client
from django.core.exceptions import ObjectDoesNotExist
from http.cookies import SimpleCookie

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

#User model
from django.contrib.auth import get_user_model

#Permissions
from .permissions import IsStudent, IsTeacher

class LoginTests(APITestCase):
    """
    Testing Login endpoints
    """
    def setUp(self):
        self._student_login_url = "/core/login/"
        self._teacher_login_url = "/core/login/"
        self._admin_login_url = "/core/login/"

    def test_student_login(self):
        #Create student user
        User = get_user_model()
        self.user = User.objects.create_user(
            email="student@example.com",
            password="student",
            first_name="Freddy",
            last_name="Mercury",
            is_student=True,
            is_teacher=False,
        )

        #Login attempt
        data = {"email":"student@example.com", "password":"student"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Incorrect email
        data = {"email":"random", "password":"student"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #Incorrect password
        data = {"email":"student@example.com", "password":"random"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_teacher_login(self):
        #Create techer user
        User = get_user_model()
        self.user = User.objects.create_user(
            email="teacher@example.com",
            password="teacher",
            first_name="John",
            last_name="Lennon",
            is_student=False,
            is_teacher=True,
        )

        #Login attempt
        data = {"email":"teacher@example.com", "password":"teacher"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Incorrect email
        data = {"email":"random", "password":"teacher"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #Incorrect password
        data = {"email":"teacher@example.com", "password":"random"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_admin_login(self):
        #Create admin user
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email="admin@example.com",
            password="admin",
            first_name="Super",
            last_name="User",
            is_student=True,
            is_teacher=True,
        )

        #Correct login
        data = {"email":"admin@example.com", "password":"admin"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Incorrect email
        data = {"email":"random", "password":"admin"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #Incorrect password
        data = {"email":"admin@example.com", "password":"random"}
        response = self.client.post("/core/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserRegistrationTests(APITestCase):
    """
    Tetsing user's registration endpoint
    """
    def setUp(self):
        self._user_registration_url = reverse("core:signup")

    def test_user_registration(self):
        User = get_user_model()
        initial_user_count = User.objects.count()
        data = {
            "email":"student@example.com",
            "password":"student1234",
            "first_name":"Michael",
            "last_name":"Bubble",
        }
        response = self.client.post(self._user_registration_url, data, format="json")
        if response.status_code != 200:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), initial_user_count + 1)

        data.pop("password")
        for attr, expected_value in data.items():
            self.assertEqual(response.data[attr], expected_value)
        try:
            User.objects.get(email="student@example.com")
        except ObjectDoesNotExist:
            raise ValueError

        #Pop a random key
        incorrect_data = {key: item for key, item in data.items()}
        random_key = random.choice(list(incorrect_data.keys()))
        response = self.client.post(self._user_registration_url, incorrect_data.pop(random_key), format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
        #Change key's text direction
        incorrect_data = {key[::-1]:data[key] for key in data.keys()}
        response = self.client.post(self._user_registration_url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #Add a key
        incorrect_data = {key: item for key, item in data.items()}
        incorrect_data["random_key"] = "random_value"
        response = self.client.post(self._user_registration_url, incorrect_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class UserLogoutTests(APITestCase):
    """
    Testing user's logout endpoint
    """
    def setUp(self):
        self._user_logout_url = reverse("core:logout")

    def test_user_logout_after_login(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="user@example.com",
            password="user",
            first_name="John",
            last_name="Lennon",
            is_student=False,
            is_teacher=True,
        )
        #Generating a token in order to simulate login
        refresh = RefreshToken.for_user(self.user)
        access = str(refresh.access_token)

        #Setting up HTTP headers and HTTP-ONLY cookie
        client = Client(HTTP_AUTHORIZATION=f"Bearer {access}")
        client.cookies.load({'jwt':str(refresh)})

        #Logout attempt via POST request
        response = client.post(self._user_logout_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Logout attempt via GET request
        response = client.get(self._user_logout_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_logout_before_login(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email="user@example.com",
            password="user",
            first_name="John",
            last_name="Lennon",
            is_student=False,
            is_teacher=True,
        )

        #Logout attempt when user is not authenticated
        response = self.client.post(self._user_logout_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #Logout attempt via GET request
        response = self.client.get(self._user_logout_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class UserCreateTests(TestCase):
    """
    Testing user, staff_user and superuser creation
    """
    def test_create_student_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='student@example.com',
            password='student',
            first_name="John",
            last_name="Lennon",
            is_student=True,
            is_teacher=False,
            is_staff=False,
            is_superuser=False
        )
        self.assertEqual(user.email, 'student@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_teacher)

        try:
            #Email adress is user for a user authentication
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        #Negative cases
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='student')

    def test_create_teacher_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='teacher@example.com',
            password='teacher',
            first_name="Freddy",
            last_name="Mercury",
            is_student=False,
            is_teacher=True,
            is_staff=False,
            is_superuser=False
        )
        self.assertEqual(user.email, 'teacher@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_student)
        self.assertTrue(user.is_teacher)

        try:
            #Email adress is user for a user authentication
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        #Negative cases
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='teacher')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='admin@example.com', 
            password='admin',
            first_name="Super",
            last_name="User",
            is_teacher=True,
            is_student=True,
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_student)
        self.assertTrue(admin_user.is_teacher)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass

        #Negative cases
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='admin',
                is_superuser=False
            )