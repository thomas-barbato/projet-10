from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import (
    UserSerializer,
    LoginUserSerializer,
    ProjectSerializer, ContributorSerializer, CommentSerializer, IssueSerializer,
    MyTokenObtainPairSerializer
)
from .models import Users, Projects, Issues, Comments, Contributors
from rest_framework import status, permissions
from rest_framework.generics import RetrieveAPIView
from .utils import get_tokens_for_user
from api.models import Users

# Rest Framework imports
from rest_framework_simplejwt.views import TokenObtainPairView


class UserViewset(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewset(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permissions = (IsAuthenticated,)
    queryset = Projects.objects.all()

class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permissions = (IsAuthenticated,)
    queryset = Contributors.objects.all()


class IssueViewset(viewsets.ViewSet):
    serializer_class = IssueSerializer
    permissions = (IsAuthenticated, )
    queryset = Issues.objects.all()


class CommentViewset(viewsets.ViewSet):
    serializer_class = CommentSerializer
    permissions = (IsAuthenticated, )
    queryset = Comments.objects.all()
