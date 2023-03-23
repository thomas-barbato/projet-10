from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action
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


class ProjectViewset(ModelViewSet):
    authorization_classes = []
    serializer_class = ProjectSerializer
    queryset = Projects.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = Projects(**serializer.data)
            project.save()
            Contributors(
                project_id=project.project,
                user_id=request.user.user_id
            ).save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [AllowAny]
    queryset = Contributors.objects.all()


class IssueViewset(viewsets.ViewSet):
    serializer_class = IssueSerializer
    permission_classes = [AllowAny]
    queryset = Issues.objects.all()


class CommentViewset(viewsets.ViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comments.objects.all()

    def list(self, request):
        print(request.user)
        queryset = Projects.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        queryset = Comments()
        serializer = CommentSerializer(self.queryset, many=False)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        contrib = Contributors.objects.filter(user_id=request.user.user_id).values('project_id')
        queryset = Projects.objects.all(project_id__in=contrib)
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
