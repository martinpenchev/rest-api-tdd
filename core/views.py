import datetime
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings

from .serializers import UserSerializer, UserRegistrationSerializer

class UserLogin(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        refresh = serializer.validated_data.pop('refresh')
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)

        #Setting up a HTTP-only cookie to refresh access tokens automatically
        response.set_cookie(
            key='jwt',
            value=refresh,
            max_age=4*60*60,
            domain="127.0.0.1",
            samesite=None,
            httponly=True,
            secure=False #TO DO Change to true when using HTTPS and add samesite for protection
        )

        return response

class UserRefresh(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        try:
            refresh = request.COOKIES['jwt']
        except TokenError as e:
            raise InvalidToken(e.args[0])
        except KeyError:
            raise NotAuthenticated()

        serializer = self.get_serializer(data={"refresh":refresh})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

@require_POST
def UserLogout(request):
    try:
        if (request.COOKIES['jwt']):
            response = HttpResponse(status=200)
            response.delete_cookie('jwt')
            return response
    except KeyError:
        return HttpResponse(status=400)

    return HttpResponse(status=400)

class UserList(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegistration(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        try:
           fields = ['email', 'password', 'first_name', 'last_name'] 
           for field in fields:
               if request.data.get(field) is None:
                   raise ValidationError({ field : "The field is required" })
        except:
            raise ValidationError("Please fill all the fields")

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)