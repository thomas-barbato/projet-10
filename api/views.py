from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import Users

from .models import Comments, Contributors, Issues, Projects
from .permissions import IsAuthorOrReadOnly, IsContributorOrReadOnly
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
    queryset = Projects.objects.all()
    message = {"details": "You do not have permission to perform this action"}

    def get_queryset(self):
        return Projects.objects.filter(
            Q(author_user_id=self.request.user)
            | Q(project_contributor__user=self.request.user)
        )

    def retrieve(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["pk"], user=request.user
        ).exists():
            return super().retrieve(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if Projects.objects.filter(
            project=self.kwargs["pk"], author_user=request.user
        ).exists():
            return super().destroy(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        if Projects.objects.filter(
            project=self.kwargs["pk"], author_user=request.user
        ).exists():
            return super().update(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)


class ContributorViewset(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated, IsContributorOrReadOnly)
    queryset = Contributors.objects.all()
    message = {"details": "You do not have permission to perform this action"}

    def get_queryset(self):
        return Contributors.objects.filter(project_id=self.kwargs["project_pk"])

    def create(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["project_pk"], user=request.user
        ).exists():
            return super().create(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["project_pk"], user=request.user
        ).exists():
            return super().destroy(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)


class IssueViewset(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Issues.objects.all()
    message = {"details": "You do not have permission to perform this action"}

    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs["project_pk"])

    def retrieve(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["project_pk"], user=request.user
        ).exists():
            return super().retrieve(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["project_pk"], user=request.user
        ).exists():
            return super().create(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Comments.objects.all()
    message = {"details": "You do not have permission to perform this action"}

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs["issue_pk"])

    def list(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["project_pk"], user=request.user
        ).exists():
            return super().list(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["project_pk"], user=request.user
        ).exists():
            return super().retrieve(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        if Contributors.objects.filter(
            project=self.kwargs["project_pk"], user=request.user
        ).exists():
            return super().create(request, *args, **kwargs)
        return Response(self.message, status=status.HTTP_403_FORBIDDEN)
