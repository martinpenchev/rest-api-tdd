from django.urls import path

from rest_framework_simplejwt.views import TokenVerifyView
from .views import UserLogin, UserRefresh, UserLogout, UserRegistration
from .views import UserList, UserDetail

app_name = 'core'
urlpatterns = [
    path('login/', UserLogin.as_view(), name='login'),
    path('refresh/', UserRefresh.as_view(), name='refresh'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
    path('logout/', UserLogout, name='logout'),
    path('user/', UserList.as_view(), name="user-list"),
    path('user/<int:pk>/', UserDetail.as_view(), name="user-detail"),
    path('signup/', UserRegistration.as_view(), name="signup"),
]