from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Users

from .models import Comments, Contributors, Issues, Projects
from .permissions import (CommentsPermissions, ContributorPermissions,
                          IssuesPermissions, ProjectsPermissions)
from .serializers import (CommentSerializer, ContributorSerializer,
                          IssueSerializer, MyTokenObtainPairSerializer,
                          ProjectSerializer, UserSerializer)


class UserViewset(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, ProjectsPermissions)
    queryset = Projects.objects.all()


class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated, ContributorPermissions)
    queryset = Contributors.objects.all()


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated, IssuesPermissions)
    queryset = Issues.objects.all()


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, CommentsPermissions)
    queryset = Comments.objects.all()
