from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

#User model
from django.contrib.auth import get_user_model

class EndpointTests(APITestCase):
    """
    Testing API endpoints
    """
    def setUp(self):
        User = get_user_model()
        #Student user
        student_user = User.objects.create_user(
            email="student@example.com",
            password="student",
            first_name="Freddy",
            last_name="Mercury",
            is_student=True,
            is_teacher=False,
        )
        #Teacher user
        teacher_user = User.objects.create_user(
            email="teacher@example.com",
            password="teacher",
            first_name="John",
            last_name="Lennon",
            is_student=False,
            is_teacher=True,
        )
        #Generating a token for student user
        student_refresh = RefreshToken.for_user(student_user)
        student_access = str(student_refresh.access_token)

        #Generating a token for teacher user
        teacher_refresh = RefreshToken.for_user(teacher_user)
        teacher_access = str(teacher_refresh.access_token)

        #Setting up student client with token authorization
        self._student_client = Client(HTTP_AUTHORIZATION=f"Bearer {student_access}")
        self._student_client.cookies.load({'jwt':str(student_refresh)})

        #Setting up teacher client with token authorization
        self._teacher_client = Client(HTTP_AUTHORIZATION=f"Bearer {teacher_access}")
        self._teacher_client.cookies.load({'jwt':str(teacher_refresh)})

        #List of GET API endpoints
        self._get_urls = [
            reverse("api:cat-list"),
            reverse("api:course-list"),
            reverse("api:lesson-list"),
            reverse("api:slide-list", kwargs={"id":1}),
        ]

        #List of Create API endpoints
        self._create_urls = [
            reverse("api:cat-create"),
            reverse("api:course-create"),
            reverse("api:lesson-create"),
            reverse("api:slide-create", kwargs={"id":1}),
        ]

        #List of RUD API endpoints
        self._rud_urls = [
            reverse("api:cat-rud", kwargs={"id":1}),
            reverse("api:course-rud", kwargs={"id":1}),
            reverse("api:lesson-rud", kwargs={"id":1}),
            reverse("api:slide-rud", kwargs={"id":1, "position":1}),
        ]

    def test_api_requests(self):
        #GET requests
        for url in self._get_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

            response = self._student_client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = self._teacher_client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        #Create requests
        for url in self._create_urls:
            response = self.client.post(url, data={"ping": "pong"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #PUT requests
        for url in self._rud_urls:
            response = self.client.put(url, data={"ping": "pong"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #DELETE requests
        for url in self._rud_urls:
            response = self.client.delete(url, data={"ping": "pong"}, format="json")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# TODO test cat / course / lesson / slide creation