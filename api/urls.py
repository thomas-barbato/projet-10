from django.urls import path
from .views import RegisterUserAPIView, LoginAPIView, UserDetailsAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", RegisterUserAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/", UserDetailsAPIView.as_view())

]
