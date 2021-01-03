import random

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

#User model
from django.contrib.auth import get_user_model

#Permissions
from core.permissions import IsStudent, IsTeacher

class EndpointTests(APITestCase):
    """
    Testing API endpoints
    """
    def setUp(self):
        User = get_user_model()
        #Student user
        self.user = User.objects.create(
            email="student@example.com",
            first_name="Freddy",
            last_name="Mercury",
            is_student=True,
            is_teacher=False,
        )

        #List of GET API endpoints
        self._get_urls = [
            reverse("cat:list"), reverse("cat:detail", kwargs={"id":"1"}),
            reverse("course:list"), reverse("course:detail", kwargs={"id":"1"}),
            reverse("lesson:list"), reverse("lesson:detail", kwargs={"id":"1"}),
            reverse("slide:list"), reverse("slide:detail", kwargs={"id":"1"}),
        ]

        #List of Create API endpoints
        self._create_urls = [
            reverse("cat:create"),
            reverse("course:create"),
            reverse("lesson:create"),
            reverse("slide:create"),
        ]

        #List of RUD API endpoints
        self._rud_urls = [
            reverse("cat:rud", kwargs={"id":"1"}),
            reverse("course:rud", kwargs={"id":"1"}),
            reverse("lesson:rud", kwargs={"id":"1"}),
            reverse("slide:rud", kwargs={"id":"1"}),
        ]

    def test_api_requests(self):
        #GET requests
        for url in self._get_urls:
            self.user.is_teacher = False
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            self.user.is_teacher = True
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Create requests
        for url in self._create_urls:
            self.user.is_teacher = False
            response = self.client.post(url, data={"ping": "pong"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            self.user.is_teacher = True
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #PUT requests
        for url in self._rud_urls:
            self.user.is_teacher = False
            response = self.client.put(url, data={"ping": "pong"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            self.user.is_teacher = True
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        #DELETE requests
        for url in self._rud_urls:
            self.user.is_teacher = False
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            self.user.is_teacher = True
            self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginTests(APITestCase):
    """
    Testing Login endpoints
    """
    def setUp(self):
        self._student_login_url = reverse("user:login"),
        self._teacher_login_url = reverse("user:login"),
        self._admin_login_url = reverse("admin:login"),

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
        response = self.client.post(self._student_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client.login(**data))

        #Incorrect email
        data = {"email":"random", "password":"student"}
        response = self.client.post(self._student_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(self.client.login(**data))

        #Incorrect password
        data = {"email":"student@example.com", "password":"random"}
        response = self.client.post(self._student_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(self.client.login(**data))

    def test_teacher_login(self):
        #Create techer user
        User = get_user_model()
        self.user = User.objects.create_user(
            email="student@example.com",
            password="teacher",
            first_name="John",
            last_name="Lennon",
            is_student=False,
            is_teacher=True,
        )

        #Login attempt
        data = {"email":"teacher@example.com", "password":"teacher"}
        response = self.client.post(self._teacher_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client.login(**data))

        #Incorrect email
        data = {"email":"random", "password":"teacher"}
        response = self.client.post(self._teacher_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(self.client.login(**data))

        #Incorrect password
        data = {"email":"teacher@example.com", "password":"random"}
        response = self.client.post(self._teacher_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(self.client.login(**data))

    def test_admin_login(self):
        #Create admin user
        User = get_user_model()
        self.user = User.objects.create_superuser(email="admin@example.com", password="admin")

        #Correct login
        data = {"email":"admin@example.com", "password":"admin"}
        response = self.client.post(self._admin_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.client.login(**data))

        #Incorrect email
        data = {"email":"random", "password":"admin"}
        response = self.client.post(self._admin_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(self.client.login(**data))

        #Incorrect password
        data = {"email":"admin@example.com", "password":"random"}
        response = self.client.post(self._admin_login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(self.client.login(**data))

class UserRegistrationTests(APITestCase):
    """
    Tetsing user's registration endpoint
    """
    def setUp(self):
        self._user_registration_url = reverse("user:registration")

    def test_user_registration(self):
        data = {
            "email":"student@example.com",
            "password":"student",
            "first_name":"Michael",
            "last_name":"Bubble",
        }
        response = self.client.post(self._user_registration_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #Pop a random key
        incorrect_data = {key: item for key, item in data.items()}
        response = self.client.post(self._user_registration_url, incorrect_data.pop(random.choice(incorrect_data.keys())), format="json")
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
        self._user_logout_url = reverse("user:logout")

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
        data = {"email":"user@example.com", "password":"user"}
        self.user.login(**data)

        #Logout attempt via POST request
        response = self.client.post(self._user_logout_url, {"email":"user@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        data = {"email":"user@example.com", "password":"user"}
        self.user.login(**data)
        self.user.logout()

        #Logout attempt when user is not authenticated
        response = self.client.post(self._user_logout_url, {"email":"user@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserPermissionTests(TestCase):
    """
    Testing custom permissions
    """
    def test_student_permission(self):
        User = get_user_model()
        self.user = User.objects.create(
            email="student@example.com",
            first_name="Freddy",
            last_name="Mercury",
            is_student=True,
            is_teacher=False,
        )

        self.assertTrue(self.user.has_perm(IsStudent))
        self.assertFalse(self.user.has_perm(IsTeacher))

        #Adding teacher permission
        self.user.user_permissions.add(IsTeacher)
        self.assertTrue(self.user.has_perm(IsStudent))
        self.assertTrue(self.user.has_perm(IsTeacher))

    def test_teacher_permission(self):
        User = get_user_model()
        self.user = User.objects.create(
            email="student@example.com",
            first_name="Freddy",
            last_name="Mercury",
            is_student=False,
            is_teacher=True,
        )

        self.assertFalse(self.user.has_perm(IsStudent))
        self.assertTrue(self.user.has_perm(IsTeacher))

        #Adding student permission
        self.user.user_permissions.add(IsStudent)
        self.assertTrue(self.user.has_perm(IsStudent))
        self.assertTrue(self.user.has_perm(IsTeacher))

class UserCreateTests(TestCase):
    """
    Testing user, staff_user and superuser creation
    """
    def test_create_student_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='student@example.com',
            password='student',
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
            'admin@example.com', 
            'admin',
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

