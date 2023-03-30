from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Users

from .models import Comments, Contributors, Issues, Projects
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    MyTokenObtainPairSerializer,
    ProjectSerializer,
    UserSerializer,
)


class UserViewset(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = Users.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProjectViewset(ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Contributors.objects.all()

    def get_queryset(self):
        return Projects.objects.filter(
            Q(author_user_id=self.request.user) | Q(project_contributor__user=self.request.user)
        )


class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Contributors.objects.all()

    def get_queryset(self):
        return Contributors.objects.filter(project_id=self.kwargs["project_pk"])


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Issues.objects.all()

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs["project_pk"])


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Comments.objects.all()

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs["issue_pk"])
